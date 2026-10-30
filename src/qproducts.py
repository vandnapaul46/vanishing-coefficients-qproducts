"""
qproducts.py
============

Core engine for the computational framework described in:

    "Computational Framework for Detecting Vanishing Coefficients
     in Infinite q-Product Expansions"

The module provides two things:

1. `expand_product`  - expands a finite or infinite q-product into its
   power-series coefficients, truncated at a chosen order N, using EXACT
   integer arithmetic (Python arbitrary-precision integers). Floating-point
   arithmetic is deliberately avoided because coefficients grow large and
   rounding error produces spurious non-zeros at high N.

2. `minimal_vanishing_classes` - scans the computed coefficients for
   arithmetic progressions r (mod m) on which every coefficient is zero,
   and returns only the MINIMAL such classes (those not already contained
   in a vanishing class of a smaller modulus).

A q-product is written as a list of factors. Each factor is a `Factor`:

    Factor(s, m, b, plus)

representing

    ( -q^s ; q^m )_inf ^ b     if plus = True        [ product of (1 + q^(s+mk)) ]
    (  q^s ; q^m )_inf ^ b     if plus = False       [ product of (1 - q^(s+mk)) ]

A positive exponent b places the factor in the numerator; a negative b
places it in the denominator (i.e. the series is divided by that factor).

Example
-------
Richmond-Szekeres product  (q^3, q^5 ; q^8)_inf / (q, q^7 ; q^8)_inf :

    factors = [
        Factor(3, 8,  1, False),
        Factor(5, 8,  1, False),
        Factor(1, 8, -1, False),
        Factor(7, 8, -1, False),
    ]
    coeffs = expand_product(factors, N=5000)
    print(minimal_vanishing_classes(coeffs, max_mod=12))   # -> [(4, 3)]
"""

from collections import namedtuple

import numpy as np

Factor = namedtuple("Factor", ["s", "m", "b", "plus"])


def expand_product(factors, N):
    """
    Expand a q-product into power-series coefficients c(0..N).

    Coefficients are stored in a NumPy array with dtype=object, so every
    entry is a Python arbitrary-precision integer. This is essential:
    with a floating-point dtype the coefficients (which grow rapidly) lose
    precision and the scan reports spurious non-zeros at high N.

    Parameters
    ----------
    factors : list[Factor]
        The factors of the product (see module docstring).
    N : int
        Truncation order. Coefficients of q^0 .. q^N are returned.

    Returns
    -------
    numpy.ndarray (dtype=object)
        Exact integer coefficients c(0), c(1), ..., c(N).
    """
    coeffs = np.zeros(N + 1, dtype=object)
    coeffs[0] = 1

    for s, m, b, plus in factors:
        if b == 0:
            continue
        reps = abs(b)
        numerator = b > 0
        k = 0
        exps = []
        while s + m * k <= N:
            exps.append(s + m * k)
            k += 1
        for _ in range(reps):
            for e in exps:
                if numerator:
                    # Multiply the series by (1 +/- q^e).
                    if plus:                       # (1 + q^e)
                        for n in range(N, e - 1, -1):
                            coeffs[n] = coeffs[n] + coeffs[n - e]
                    else:                          # (1 - q^e)
                        for n in range(N, e - 1, -1):
                            coeffs[n] = coeffs[n] - coeffs[n - e]
                else:
                    # Divide the series by (1 +/- q^e).
                    if plus:                       # 1 / (1 + q^e)
                        for n in range(e, N + 1):
                            coeffs[n] = coeffs[n] - coeffs[n - e]
                    else:                          # 1 / (1 - q^e)
                        for n in range(e, N + 1):
                            coeffs[n] = coeffs[n] + coeffs[n - e]
    return coeffs


def all_vanishing_classes(coeffs, max_mod, min_terms=3):
    """
    Return every arithmetic progression r (mod m), 2 <= m <= max_mod,
    on which all available coefficients are zero.

    A class is reported only if it contains at least `min_terms` tested
    positions, to avoid declaring a class "vanishing" on the strength of
    one or two zeros.
    """
    N = len(coeffs) - 1
    found = []
    for m in range(2, max_mod + 1):
        for r in range(m):
            idx = range(r, N + 1, m)
            tested = 0
            is_zero = True
            for i in idx:
                tested += 1
                if coeffs[i] != 0:
                    is_zero = False
                    break
            if is_zero and tested >= min_terms:
                found.append((m, r))
    return found


def _contained(m2, r2, classes):
    """True if class r2 (mod m2) is contained in a smaller-modulus class."""
    for m1, r1 in classes:
        if m1 < m2 and m2 % m1 == 0 and r2 % m1 == r1:
            return True
    return False


def minimal_vanishing_classes(coeffs, max_mod=15, min_terms=3):
    """
    Return the MINIMAL vanishing classes: those not already contained in a
    vanishing class of a smaller modulus.

    For example, if 3 (mod 4) vanishes then 3 (mod 8) and 7 (mod 8) also
    vanish, but they are not reported because they are contained in 3 (mod 4).
    """
    classes = all_vanishing_classes(coeffs, max_mod, min_terms)
    return [(m, r) for (m, r) in classes if not _contained(m, r, classes)]


def verify_class(coeffs, m, r):
    """
    Verify that every coefficient at position r (mod m) is zero.

    Returns (all_zero, positions_tested).
    """
    N = len(coeffs) - 1
    idx = list(range(r, N + 1, m))
    return all(coeffs[i] == 0 for i in idx), len(idx)
