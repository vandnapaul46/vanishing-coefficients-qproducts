"""
Systematic exploration scan.

Scans several families of q-products for minimal vanishing classes. This is
the search that produced the new modulus-7 conjecture reported in Section V-B.

Families scanned:
  1. Hirschhorn-type, modulus 7/14 : (-q^a, -q^(7-a); q^7)(q^c, q^(14-c); q^14)^3
  2. Hirschhorn-type, modulus 6/12 : (-q^a, -q^(6-a); q^6)(q^c, q^(12-c); q^12)^3
  3. Pure quotients,  modulus 10   : (q^a, q^(10-a); q^10) / (q^c, q^(10-c); q^10)
  4. Pure quotients,  modulus 12   : (q^a, q^(12-a); q^12) / (q^c, q^(12-c); q^12)

A fast truncation (N = 500) is used for scanning; promising hits should be
re-verified at N = 5000 with the relevant experiment script.

Run:  python experiments/exploration_scan.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from qproducts import Factor, expand_product, minimal_vanishing_classes

N = 500


def scan_family_hirschhorn(mod):
    """(-q^a, -q^(mod-a); q^mod)(q^c, q^(2mod-c); q^2mod)^3"""
    hits = []
    dmod = 2 * mod
    for a in range(1, mod // 2 + 1):
        b = mod - a
        if a == b:
            continue
        for c in range(1, dmod):
            d = dmod - c
            if c >= d:
                continue
            factors = [
                Factor(a, mod, 1, True),
                Factor(b, mod, 1, True),
                Factor(c, dmod, 3, False),
                Factor(d, dmod, 3, False),
            ]
            coeffs = expand_product(factors, N)
            minimal = minimal_vanishing_classes(coeffs, max_mod=mod + 2)
            if minimal:
                desc = (f"(-q^{a}, -q^{b}; q^{mod})"
                        f"(q^{c}, q^{d}; q^{dmod})^3")
                hits.append((desc, minimal))
    return hits


def scan_family_quotient(mod):
    """(q^a, q^(mod-a); q^mod) / (q^c, q^(mod-c); q^mod)"""
    hits = []
    for a in range(1, mod // 2 + 1):
        b = mod - a
        if a == b:
            continue
        for c in range(1, mod // 2 + 1):
            d = mod - c
            if c == d or a == c:
                continue
            factors = [
                Factor(a, mod,  1, False),
                Factor(b, mod,  1, False),
                Factor(c, mod, -1, False),
                Factor(d, mod, -1, False),
            ]
            coeffs = expand_product(factors, N)
            minimal = minimal_vanishing_classes(coeffs, max_mod=mod + 2)
            if minimal:
                desc = (f"(q^{a}, q^{b}; q^{mod}) / "
                        f"(q^{c}, q^{d}; q^{mod})")
                hits.append((desc, minimal))
    return hits


def main():
    print(f"Exploration scan (N = {N})")
    print("=" * 64)

    families = [
        ("Hirschhorn 7/14", lambda: scan_family_hirschhorn(7)),
        ("Hirschhorn 6/12", lambda: scan_family_hirschhorn(6)),
        ("Quotients mod 10", lambda: scan_family_quotient(10)),
        ("Quotients mod 12", lambda: scan_family_quotient(12)),
    ]

    total = 0
    for label, fn in families:
        print(f"\n--- {label} ---")
        hits = fn()
        total += len(hits)
        if not hits:
            print("  (no vanishing classes found)")
        for desc, minimal in hits:
            print(f"  {desc}  ->  {minimal}")

    print("\n" + "=" * 64)
    print(f"Total products with a minimal vanishing class: {total}")


if __name__ == "__main__":
    main()
