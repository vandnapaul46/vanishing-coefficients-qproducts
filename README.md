# Vanishing Coefficients in Infinite q-Product Expansions

A general-purpose computational framework, written in Python, for detecting
**vanishing coefficients** in infinite q-product expansions. Given a q-product,
the framework expands it to a high truncation order using exact integer
arithmetic, extracts its power-series coefficients, and scans residue classes
`r (mod m)` to find arithmetic progressions on which every coefficient is zero.

## Workflow

For a product written as a list of factors `(q^s ; q^m)_inf^b`, the framework:

1. expands the product into coefficients `c(0), c(1), ..., c(N)`, truncated at
   order `N`, using **NumPy arrays with `dtype=object`** so that every
   coefficient is an exact arbitrary-precision integer;
2. scans every residue class `r (mod m)` for `2 <= m <= M` and reports the
   **minimal** vanishing classes (those not already contained in a vanishing
   class of a smaller modulus);
3. confirms a detected pattern by re-running at increasing truncation orders
   `N = 100, 500, 1000, 5000`.

Exact integer arithmetic is essential: with floating-point storage the
coefficients (which grow quickly) lose precision and the scan reports spurious
non-zeros at high `N`.

## Results reproduced

| Script | Product | Vanishing identity |
|---|---|---|
| `experiments/richmond_szekeres.py` | `(q^3, q^5; q^8) / (q, q^7; q^8)` | `C(4n+3) = 0` |
| `experiments/baruah_kaur.py` | `(-q, -q^4; q^5)(q^4, q^6; q^10)^3` | `Phi(5n+3) = 0` |
| `experiments/new_conjecture.py` | `(-q^2, -q^5; q^7)(q^4, q^10; q^14)^3` | `G(7n+3) = 0` *(new)* |

The third identity is a **new conjecture discovered by the framework** and does
not appear in prior literature. It belongs to a modulus-7 family

```
(-q^a, -q^(7-a); q^7)_inf (q^(2a), q^(14-2a); q^14)_inf^3 ,   a = 1, 2, 3
```

whose members vanish on `7n+6`, `7n+3`, and `7n+5` respectively.

## Installation

Requires Python 3.8+.

```bash/terminal
git clone https://github.com/<your-username>/vanishing-coefficients-qproducts.git
cd vanishing-coefficients-qproducts
pip install -r requirements.txt
```

## Usage

Run any experiment directly:

```bash/terminal
python experiments/richmond_szekeres.py
python experiments/baruah_kaur.py
python experiments/new_conjecture.py
python experiments/exploration_scan.py
python experiments/benchmark.py
python figures/generate_figures.py
```

Or use the core engine on your own product:

```python
from src.qproducts import Factor, expand_product, minimal_vanishing_classes

# Richmond-Szekeres:  (q^3, q^5; q^8) / (q, q^7; q^8)
factors = [
    Factor(3, 8,  1, False),   # (q^3; q^8)_inf
    Factor(5, 8,  1, False),   # (q^5; q^8)_inf
    Factor(1, 8, -1, False),   # 1 / (q;   q^8)_inf
    Factor(7, 8, -1, False),   # 1 / (q^7; q^8)_inf
]

coeffs = expand_product(factors, N=5000)
print(minimal_vanishing_classes(coeffs, max_mod=12))   # -> [(4, 3)]
```

A `Factor(s, m, b, plus)` represents `(-q^s; q^m)_inf^b` when `plus=True` and
`(q^s; q^m)_inf^b` when `plus=False`. A positive exponent `b` is a numerator
factor; a negative `b` is a denominator factor.
