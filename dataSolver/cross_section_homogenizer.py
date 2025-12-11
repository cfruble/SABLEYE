import numpy as np
from scipy.integrate import trapezoid
from typing import Dict, Tuple, Optional
import os

try:
    import openmc.data
    OPENMC_AVAILABLE = True
except ImportError:
    OPENMC_AVAILABLE = False


class CrossSectionHomogenizer:
    """
    Single-group cross section homogenizer for nuclear data.
    """

    def __init__(self, energy_spectrum: Dict[str, np.ndarray] = None):
        if energy_spectrum is None:
            self.energy_spectrum = self._default_thermal_spectrum()
        else:
            self.energy_spectrum = energy_spectrum
        self.cache = {}
        self.loaded_nuclides = {}

    def _default_thermal_spectrum(self) -> Dict[str, np.ndarray]:
        """Create default thermal reactor spectrum."""
        energies = np.logspace(-2, 1, 500)  # 0.01 eV to 10 eV
        weights = 1 / np.sqrt(energies)
        return {'energy_bins': energies, 'weights': weights}

    @staticmethod
    def create_spectrum(spectrum_type='thermal', **kwargs):
        """Create different energy spectra."""
        if spectrum_type == 'thermal':
            energies = np.logspace(-2, 1, 500)
            weights = 1 / np.sqrt(energies)
        elif spectrum_type == 'fast':
            energies = np.logspace(4, 7, 500)  # 10 keV to 10 MeV
            weights = np.ones_like(energies)
        elif spectrum_type == 'custom':
            energies = kwargs['energies']
            weights = kwargs['weights']
        else:
            raise ValueError(f"Unknown spectrum type: {spectrum_type}")
        return {'energy_bins': energies, 'weights': weights}

    def load_nuclide_data(self, endf_file_path: str, nuclide: str) -> None:
        """Load ENDF data for a nuclide."""
        if nuclide in self.loaded_nuclides:
            return

        if not os.path.exists(endf_file_path):
            raise FileNotFoundError(f"ENDF file not found: {endf_file_path}")

        try:
            nuclear_data = openmc.data.IncidentNeutron.from_endf(endf_file_path)
            self.loaded_nuclides[nuclide] = nuclear_data
        except Exception as e:
            raise ValueError(f"Failed to load ENDF data for {nuclide}: {e}")

    def get_one_group_xs(self, endf_file_path: str, nuclide: str, mt_number: int) -> float:
        """
        Calculate one-group cross section.
        """
        cache_key = (nuclide, mt_number)
        if cache_key in self.cache:
            return self.cache[cache_key]

        if nuclide not in self.loaded_nuclides:
            self.load_nuclide_data(endf_file_path, nuclide)

        nuclear_data = self.loaded_nuclides[nuclide]

        if mt_number not in nuclear_data.reactions:
            available_mt = list(nuclear_data.reactions.keys())
            raise ValueError(f"MT {mt_number} not available for {nuclide}. Available: {available_mt}")

        reaction = nuclear_data.reactions[mt_number]
        xs_data = reaction.xs['0K']

        energies = self.energy_spectrum['energy_bins']
        weights = self.energy_spectrum['weights']

        xs_values = xs_data(energies)

        numerator = trapezoid(xs_values * weights, energies)
        denominator = trapezoid(weights, energies)

        one_group_xs = numerator / denominator
        self.cache[cache_key] = one_group_xs

        return one_group_xs

