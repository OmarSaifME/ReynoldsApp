
# test_gci.py
from core.gci import calculate_gci

# Test with your Cl values
results = calculate_gci(
    r12=1.29,
    r23=1.29,
    coarse_val=0.20029015,
    medium_val=0.19318061,
    fine_val=0.18591231,
    safety_factor=1.25,
    fixed_p=None
)

print("=== GCI Test Results ===")
for key, value in results.items():
    print(f"{key}: {value}")