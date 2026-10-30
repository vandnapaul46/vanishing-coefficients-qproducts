"""
Runtime benchmark (Table IV).

Measures wall-clock time to expand each product at increasing truncation
orders, using exact integer arithmetic. Reports the median of three runs.

Run:  python experiments/benchmark.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from qproducts import Factor, expand_product

RICHMOND_SZEKERES = [
    Factor(3, 8,  1, False),
    Factor(5, 8,  1, False),
    Factor(1, 8, -1, False),
    Factor(7, 8, -1, False),
]

BARUAH_KAUR = [
    Factor(1,  5, 1, True),
    Factor(4,  5, 1, True),
    Factor(4, 10, 3, False),
    Factor(6, 10, 3, False),
]


def median_time(factors, N, runs=3):
    times = []
    for _ in range(runs):
        t0 = time.perf_counter()
        expand_product(factors, N)
        times.append(time.perf_counter() - t0)
    return sorted(times)[len(times) // 2]


def main():
    print(f"{'N':>6}  {'Richmond-Szekeres (s)':>22}  {'Baruah-Kaur (s)':>16}")
    print("-" * 50)
    for N in [100, 500, 1000, 5000]:
        rs = median_time(RICHMOND_SZEKERES, N)
        bk = median_time(BARUAH_KAUR, N)
        print(f"{N:>6}  {rs:>22.3f}  {bk:>16.3f}")


if __name__ == "__main__":
    main()
