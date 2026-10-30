"""
Section V-A - Extended exploration: the Baruah-Kaur product.

Product:  Phi(q) = (-q, -q^4 ; q^5)_inf * (q^4, q^6 ; q^10)_inf^3
Result :  Phi(5n + 3) = 0 for all n >= 0   (minimal class: 3 (mod 5))

Run:  python experiments/baruah_kaur.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from qproducts import Factor, expand_product, minimal_vanishing_classes, verify_class

FACTORS = [
    Factor(1,  5, 1, True),    # (-q;    q^5)_inf
    Factor(4,  5, 1, True),    # (-q^4;  q^5)_inf
    Factor(4, 10, 3, False),   # (q^4;   q^10)_inf^3
    Factor(6, 10, 3, False),   # (q^6;   q^10)_inf^3
]


def main():
    print("Baruah-Kaur product: (-q, -q^4; q^5)_inf (q^4, q^6; q^10)_inf^3")
    print("=" * 64)

    for N in [100, 500, 1000, 5000]:
        coeffs = expand_product(FACTORS, N)
        minimal = minimal_vanishing_classes(coeffs, max_mod=15)
        ok, tested = verify_class(coeffs, 5, 3)
        status = "Detected" if N == 100 else "Confirmed"
        print(f"  N = {N:5d}  |  minimal classes {minimal}  |  "
              f"Phi(5n+3)=0: {ok} ({tested} positions)  |  {status}")

    coeffs = expand_product(FACTORS, 30)
    print("\nFirst 20 coefficients:")
    for n in range(20):
        tag = "  <-- 5n+3" if n % 5 == 3 else ""
        print(f"  Phi({n:2d}) = {coeffs[n]:>6}{tag}")


if __name__ == "__main__":
    main()
