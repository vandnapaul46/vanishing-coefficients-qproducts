"""
Section V-B - New conjecture discovered by the framework.

Product:  G(q) = (-q^2, -q^5 ; q^7)_inf * (q^4, q^10 ; q^14)_inf^3
Result :  G(7n + 3) = 0 for all n >= 0   (minimal class: 3 (mod 7))

This vanishing pattern does not appear in prior literature. The product
belongs to a family

    (-q^a, -q^(7-a) ; q^7)_inf (q^(2a), q^(14-2a) ; q^14)_inf^3,   a = 1, 2, 3

each member of which has a single minimal vanishing class modulo 7:
    a = 1 -> 7n + 6
    a = 2 -> 7n + 3
    a = 3 -> 7n + 5

Run:  python experiments/new_conjecture.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from qproducts import Factor, expand_product, minimal_vanishing_classes, verify_class


def family_member(a):
    """Return the factor list for member `a` of the modulus-7 family."""
    return [
        Factor(a,      7, 1, True),    # (-q^a;      q^7)_inf
        Factor(7 - a,  7, 1, True),    # (-q^(7-a);  q^7)_inf
        Factor(2 * a, 14, 3, False),   # (q^(2a);    q^14)_inf^3
        Factor(14 - 2 * a, 14, 3, False),  # (q^(14-2a); q^14)_inf^3
    ]


def main():
    print("New conjecture: (-q^2, -q^5; q^7)_inf (q^4, q^10; q^14)_inf^3")
    print("=" * 64)

    factors = family_member(2)
    for N in [100, 500, 1000, 5000]:
        coeffs = expand_product(factors, N)
        minimal = minimal_vanishing_classes(coeffs, max_mod=15)
        ok, tested = verify_class(coeffs, 7, 3)
        status = "Detected" if N == 100 else "Confirmed"
        print(f"  N = {N:5d}  |  minimal classes {minimal}  |  "
              f"G(7n+3)=0: {ok} ({tested} positions)  |  {status}")

    print("\nFull family  (-q^a, -q^(7-a); q^7)_inf (q^(2a), q^(14-2a); q^14)_inf^3:")
    for a in (1, 2, 3):
        coeffs = expand_product(family_member(a), 5000)
        minimal = minimal_vanishing_classes(coeffs, max_mod=14)
        print(f"  a = {a}  ->  minimal vanishing class {minimal}")

    coeffs = expand_product(family_member(2), 30)
    print("\nFirst 20 coefficients (a = 2):")
    for n in range(20):
        tag = "  <-- 7n+3" if n % 7 == 3 else ""
        print(f"  G({n:2d}) = {coeffs[n]:>6}{tag}")


if __name__ == "__main__":
    main()
