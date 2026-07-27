# core/angle_of_attack.py
import math


def calculate_aoa_components(angle_degrees, velocity):
    """
    Calculate velocity and force vector components for CFD boundary conditions.

    Parameters:
    angle_degrees (float): Angle of attack in degrees
    velocity (float): Freestream velocity in m/s

    Returns:
    dict: Dictionary containing all calculated values, ready for GUI display
    """
    # Convert angle to radians
    angle_rad = math.radians(angle_degrees)
    sin_val = math.sin(angle_rad)
    cos_val = math.cos(angle_rad)

    # Velocity components
    Vx = velocity * cos_val  # Velocity component along X-axis
    Vy = velocity * sin_val  # Velocity component along Y-axis

    # Force vector components (for Fluent boundary conditions)
    drag_x = cos_val
    drag_y = sin_val
    lift_x = -sin_val  # Negative for lift vector
    lift_y = cos_val

    # Return as a structured dictionary
    return {
        'Angle of Attack (deg)': f"{angle_degrees:.2f}",
        'Flow Velocity (m/s)': f"{velocity:.2f}",
        'Velocity Component for X (m/s)': f"{Vx:.10f}",
        'Velocity Component for Y (m/s)': f"{Vy:.10f}",
        'drag_x': f"{drag_x:.10f}",
        'drag_y': f"{drag_y:.10f}",
        'lift_x': f"{lift_x:.10f}",
        'lift_y': f"{lift_y:.10f}",
    }


# Optional: Keep a simple command-line version for testing
if __name__ == "__main__":
    # This only runs if you execute this file directly (not when imported)
    print("=== AOA Calculator (Command Line Test) ===")
    ad = float(input("Angle of Attack in Degrees: "))
    v = float(input("Velocity in m/s: "))

    results = calculate_aoa_components(ad, v)

    print("\n=== Results ===")
    for key, value in results.items():
        print(f"{key}: {value}")