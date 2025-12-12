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
    Provides single-group cross section homogenization for nuclear data.

    This class supports loading ENDF nuclear data files, building energy spectra,
    and calculating one-group cross sections.
    """

    def __init__(self, energy_spectrum: Dict[str, np.ndarray] = None):
        """
        Initialize the CrossSectionHomogenizer.

        Parameters
        ----------
        energy_spectrum : dict, optional
            Dictionary with 'energy_bins' (np.ndarray) and 'weights' (np.ndarray)
            representing the energy spectrum used for homogenization.
            If None, a default thermal spectrum is used.
        """
        if energy_spectrum is None:
            self.energy_spectrum = self._default_thermal_spectrum()
        else:
            self.energy_spectrum = energy_spectrum
        self.cache = {}
        self.loaded_nuclides = {}

    def _default_thermal_spectrum(self) -> Dict[str, np.ndarray]:
        """Create and return a default thermal reactor spectrum.
        
        Returns
        -------
        dict
            Dictionary containing 'energy_bins' and 'weights' arrays
            for a representative thermal energy spectrum.
        
        """
        energies = np.logspace(-2, 1, 500)  # 0.01 eV to 10 eV
        weights = 1 / np.sqrt(energies)
        return {'energy_bins': energies, 'weights': weights}

    @staticmethod
    def create_spectrum(spectrum_type='thermal', **kwargs):
        """
        Create various energy spectra.

        Parameters
        ----------
        spectrum_type : str, optional
            Type of spectrum: 'thermal', 'fast', or 'custom'.
        **kwargs
            For 'custom', supply 'energies' and 'weights' arrays.

        Returns
        -------
        dict
            Dictionary with 'energy_bins' and 'weights' arrays.

        Raises
        ------
        ValueError
            If an unknown spectrum type is specified, or required kwargs are missing.
        """
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
        """
        Load ENDF-format nuclear data for a nuclide.

        Tries several possible paths to locate the ENDF file. Loads the data
        into memory for subsequent cross section calculations.

        Parameters
        ----------
        endf_file_path : str
            Path to the ENDF file.
        nuclide : str
            Name of the nuclide to load (e.g., 'U235').

        Raises
        ------
        FileNotFoundError
            If the ENDF file cannot be found.
        ValueError
            If loading data fails (e.g., file corrupted).
        """
        if nuclide in self.loaded_nuclides:
            return

        if not os.path.exists(endf_file_path):

            possible_paths = [
            endf_file_path,
            f"../{endf_file_path}",
            f"../../{endf_file_path}",
            f"rawData/ENDF-B-VIII.0/neutrons/{os.path.basename(endf_file_path)}",
            f"../rawData/ENDF-B-VIII.0/neutrons/{os.path.basename(endf_file_path)}",
        ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    endf_file_path = path
                    break
            else:
                raise FileNotFoundError(f"ENDF file not found: {endf_file_path}. Tried: {possible_paths}")

        try:
            nuclear_data = openmc.data.IncidentNeutron.from_endf(endf_file_path)
            self.loaded_nuclides[nuclide] = nuclear_data
        except Exception as e:
            raise ValueError(f"Failed to load ENDF data for {nuclide}: {e}")

    def get_one_group_xs(self, endf_file_path: str, nuclide: str, mt_number: int) -> float:
        """
        Calculate single-group (homogenized) cross section for a nuclide and reaction.

        Loads nuclear data if not already loaded, interpolates the reaction cross section
        over the current energy spectrum, and performs spectrum-weighted averaging.

        Parameters
        ----------
        endf_file_path : str
            Path (or ENDF identifier) to the ENDF nuclear data file.
        nuclide : str
            Name of the nuclide to query (e.g., 'U235').
        mt_number : int
            ENDF reaction MT number (e.g., 18 for fission, 102 for n-gamma).

        Returns
        -------
        float
            Homogenized one-group cross section (barns).

        Raises
        ------
        ValueError
            If the specified reaction MT is not available for the nuclide
            or the ENDF data cannot be loaded.
        """

        if endf_file_path.isdigit() and len(endf_file_path) == 10:
            endf_file_path = f"../rawData/ENDF-B-VIII.0/neutrons/{endf_file_path}"

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

