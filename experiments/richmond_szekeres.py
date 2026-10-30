"""
Section IV - Validation on the Richmond-Szekeres identity.

Product:  C(q) = (q^3, q^5 ; q^8)_inf / (q, q^7 ; q^8)_inf
Result :  C(4n + 3) = 0 for all n >= 0   (minimal class: 3 (mod 4))

Run:  python experiments/richmond_szekeres.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from qproducts import Factor, expand_product, minimal_vanishing_classes, verify_class

FACTORS = [
    Factor(3, 8,  1, False),   # (q^3; q^8)_inf
    Factor(5, 8,  1, False),   # (q^5; q^8)_inf
    Factor(1, 8, -1, False),   # 1 / (q;   q^8)_inf
    Factor(7, 8, -1, False),   # 1 / (q^7; q^8)_inf
]


def main():
    print("Richmond-Szekeres product: (q^3, q^5; q^8)_inf / (q, q^7; q^8)_inf")
    print("=" * 64)

    for N in [100, 500, 1000, 5000]:
        coeffs = expand_product(FACTORS, N)
        minimal = minimal_vanishing_classes(coeffs, max_mod=12)
        ok, tested = verify_class(coeffs, 4, 3)
        status = "Detected" if N == 100 else "Confirmed"
        print(f"  N = {N:5d}  |  minimal classes {minimal}  |  "
              f"C(4n+3)=0: {ok} ({tested} positions)  |  {status}")

    # First coefficients, for inspection.
    coeffs = expand_product(FACTORS, 30)
    print("\nFirst 20 coefficients:")
    for n in range(20):
        tag = "  <-- 4n+3" if n % 4 == 3 else ""
        print(f"  C({n:2d}) = {coeffs[n]:>6}{tag}")


if __name__ == "__main__":
    main()
