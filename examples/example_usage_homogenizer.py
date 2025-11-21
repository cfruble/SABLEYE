#!/usr/bin/env python3
"""
Example usage of CrossSectionHomogenizer
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../dataSolver'))

from cross_section_homogenizer import CrossSectionHomogenizer

def example():
    """Example of using the homogenizer."""
    print("CrossSectionHomogenizer Example Usage")
    print("=" * 40)
    
    # Example 1: Default thermal spectrum
    print("1. Using default thermal spectrum:")
    homogenizer1 = CrossSectionHomogenizer()
    xs1 = homogenizer1.get_one_group_xs(
        "../neutron_data/neutrons-version.VIII.1/n-092_U_235.endf",
        "U235", 18
    )
    print(f"   U235 fission: {xs1:.1f} barns")
    
    # Example 2: Custom fast spectrum
    print("\n2. Using fast spectrum:")
    fast_spectrum = CrossSectionHomogenizer.create_spectrum('fast')
    homogenizer2 = CrossSectionHomogenizer(fast_spectrum)
    xs2 = homogenizer2.get_one_group_xs(
        "../neutron_data/neutrons-version.VIII.1/n-092_U_235.endf", 
        "U235", 18
    )
    print(f"   U235 fission: {xs2:.1f} barns")
    
    # Example 3: Multiple reactions
    print("\n3. Multiple reactions for U235:")
    reactions = [(18, 'fission'), (102, 'capture'), (2, 'elastic')]
    for mt, desc in reactions:
        xs = homogenizer1.get_one_group_xs(
            "../neutron_data/neutrons-version.VIII.1/n-092_U_235.endf",
            "U235", mt
        )
        print(f"   {desc:10}: {xs:.1f} barns")

if __name__ == "__main__":
    example()
