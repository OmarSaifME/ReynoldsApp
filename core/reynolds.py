# core/reynolds.py
"""
Reynolds Number Calculator Module
Modes: Re → Velocity | Velocity → Re
"""


def re_to_velocity(reynolds_number, length, density, viscosity):
    """
    Calculate flow velocity from Reynolds number.

    Parameters:
    reynolds_number (float): Target Reynolds number
    length (float): Characteristic length (m)
    density (float): Fluid density (kg/m³)
    viscosity (float): Dynamic viscosity (Pa·s)

    Returns:
    dict: Results ready for GUI display
    """
    velocity = (reynolds_number * viscosity) / (density * length)

    # Determine flow regime
    if reynolds_number < 2300:
        regime = "Laminar"
    elif reynolds_number < 4000:
        regime = "Transition"
    else:
        regime = "Turbulent"

    return {
        'Mode': 'Re → Velocity',
        'Reynolds Number': f"{reynolds_number:.2e}",
        'Flow Velocity (m/s)': f"{velocity:.4f}",
        'Characteristic Length (m)': f"{length:.3f}",
        'Fluid Density (kg/m³)': f"{density:.3f}",
        'Dynamic Viscosity (Pa·s)': f"{viscosity:.2e}",
        'Flow Regime': regime
    }


def velocity_to_re(velocity, length, density, viscosity):
    """
    Calculate Reynolds number from flow velocity.

    Parameters:
    velocity (float): Flow velocity (m/s)
    length (float): Characteristic length (m)
    density (float): Fluid density (kg/m³)
    viscosity (float): Dynamic viscosity (Pa·s)

    Returns:
    dict: Results ready for GUI display
    """
    reynolds_number = (density * velocity * length) / viscosity

    # Determine flow regime
    if reynolds_number < 2300:
        regime = "Laminar"
    elif reynolds_number < 4000:
        regime = "Transition"
    else:
        regime = "Turbulent"

    return {
        'Mode': 'Velocity → Re',
        'Reynolds Number': f"{reynolds_number:.2e}",
        'Flow Velocity (m/s)': f"{velocity:.4f}",
        'Characteristic Length (m)': f"{length:.3f}",
        'Fluid Density (kg/m³)': f"{density:.3f}",
        'Dynamic Viscosity (Pa·s)': f"{viscosity:.2e}",
        'Flow Regime': regime
    }

"""
# Optional: Quick test if run directly
if __name__ == "__main__":
    print("=== Reynolds Calculator Test ===")

    # Test Re → Velocity
    print("\nTest 1: Re = 100000 → Velocity")
    result1 = re_to_velocity(100000, 0.5, 1.225, 1.8e-5)
    for k, v in result1.items():
        print(f"{k}: {v}")

    # Test Velocity → Re
    print("\nTest 2: Velocity = 10 m/s → Re")
    result2 = velocity_to_re(10, 0.5, 1.225, 1.8e-5)
    for k, v in result2.items():
        print(f"{k}: {v}")
"""