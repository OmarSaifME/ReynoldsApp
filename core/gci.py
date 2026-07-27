# core/gci.py
"""
Grid Convergence Index (GCI) Calculator
Following NASA's recommended safety factor of 1.25 for 3+ meshes
"""

import numpy as np


def apparent_order(f1, f2, f3, r12, r23):
    """
    Calculate apparent order of accuracy.

    Parameters:
    f1: coarse mesh solution
    f2: medium mesh solution
    f3: fine mesh solution
    r12: refinement ratio coarse → medium
    r23: refinement ratio medium → fine

    Returns:
    float: apparent order of accuracy (p)
    """
    epsilon32 = f3 - f2
    epsilon21 = f2 - f1

    # Avoid division by zero
    if epsilon21 == 0:
        return 1.0

    ratio = epsilon32 / epsilon21
    p = abs(np.log(abs(ratio)) / np.log(r23))
    return p


def gci_fine(f2, f3, r23, p, Fs=1.25):
    """
    Calculate GCI for the fine mesh.

    Parameters:
    f2: medium mesh solution
    f3: fine mesh solution
    r23: refinement ratio medium → fine
    p: apparent order of accuracy
    Fs: safety factor (1.25 for 3+ meshes)

    Returns:
    float: GCI as percentage
    """
    epsilon32 = f3 - f2

    # Avoid division by zero
    if f3 == 0:
        return 100.0

    e_approx = abs(epsilon32 / f3)
    gci = Fs * e_approx / (r23 ** p - 1)
    return gci * 100  # percentage


def gci_fixed_p(f2, f3, r23, p=2.0, Fs=1.25):
    """
    Calculate GCI using fixed order of accuracy.

    Parameters:
    f2: medium mesh solution
    f3: fine mesh solution
    r23: refinement ratio medium → fine
    p: fixed order of accuracy (default 2.0)
    Fs: safety factor

    Returns:
    float: GCI as percentage
    """
    if f3 == 0:
        return 100.0

    e_approx = abs((f3 - f2) / f3)
    gci = Fs * e_approx / (r23 ** p - 1)
    return gci * 100


def calculate_gci(r12, r23, coarse_val, medium_val, fine_val,
                  safety_factor=1.25, fixed_p=None):
    """
    Complete GCI calculation for a single variable.

    Parameters:
    r12: refinement ratio coarse → medium
    r23: refinement ratio medium → fine
    coarse_val: solution on coarse mesh
    medium_val: solution on medium mesh
    fine_val: solution on fine mesh
    safety_factor: Fs (default 1.25)
    fixed_p: if provided, use fixed order instead of calculated p

    Returns:
    dict: Results ready for GUI display
    """
    # Calculate apparent order
    p = apparent_order(coarse_val, medium_val, fine_val, r12, r23)

    # Calculate GCI using calculated or fixed p
    if fixed_p is not None:
        p_used = fixed_p
        gci = gci_fixed_p(medium_val, fine_val, r23, fixed_p, safety_factor)
    else:
        p_used = p
        gci = gci_fine(medium_val, fine_val, r23, p, safety_factor)

    # Determine asymptotic range (simplified check)
    asymptotic_check = "Confirmed" if p_used > 1.5 else "Check refinement"

    return {
        'Apparent Order (p)': f"{p_used:.4f}",
        'GCI (Fine Mesh)': f"{gci:.4f}%",
        'Safety Factor (Fs)': f"{safety_factor}",
        'Refinement Ratio (r)': f"{r23:.3f}",
        'Asymptotic Range': asymptotic_check,
        'Extrapolated Value': f"{fine_val - (fine_val - medium_val) / (r23 ** p_used - 1):.8f}",
        'GCI (Low Estimate)': f"{gci * 0.5:.4f}%",
        'GCI (High Estimate)': f"{gci * 1.5:.4f}%"
    }