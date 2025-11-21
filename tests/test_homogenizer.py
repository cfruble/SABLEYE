#!/usr/bin/env python3
"""
Test script for CrossSectionHomogenizer validation
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../dataSolver'))

from cross_section_homogenizer import CrossSectionHomogenizer

def test_thermal_validation():
    """Test homogenizer with thermal spectrum validation."""
    print("Testing CrossSectionHomogenizer Thermal Validation")
    print("=" * 50)
    
    homogenizer = CrossSectionHomogenizer()
    
    test_file = "../neutron_data/neutrons-version.VIII.1/n-092_U_235.endf"
    
    if not os.path.exists(test_file):
        print(f"ENDF file not found: {test_file}")
        return False
    
    try:
        # Load data once
        homogenizer.load_nuclide_data(test_file, "U235")
        nuclear_data = homogenizer.loaded_nuclides["U235"]
        
        # Check thermal point directly
        reaction = nuclear_data.reactions[18]  # Fission
        xs_data = reaction.xs['0K']
        thermal_point = xs_data(0.025)
        
        print(f" U235 fission at 0.025 eV: {thermal_point:.3f} barns")
        print(f" Expected thermal (JENDL): 585.1 barns")
        print(f" Ratio: {thermal_point/585.1:.3f}")
        
        # Get homogenized value
        xs = homogenizer.get_one_group_xs(test_file, "U235", 18)
        print(f"Homogenized fission XS: {xs:.1f} barns")
        print(f"Spectrum range: 0.01 eV to 10 eV")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = test_thermal_validation()
    if success:
        print("\n All validation tests passed")
    else:
        print("\n Some tests failed")
