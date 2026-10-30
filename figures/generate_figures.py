"""
Generate the coefficient plots used in the paper (Figures 2, 3 and 4).

Each plot shows the coefficients of a product up to n = 100, with the
vanishing residue class highlighted.

Output PNGs are written to results/.

Run:  python figures/generate_figures.py
"""

import os
import sys

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from qproducts import Factor, expand_product

RESULTS = os.path.join(os.path.dirname(__file__), "..", "results")

BLUE = "#2B579A"
ORANGE = "#E65100"


def coeff_plot(factors, modulus, residue, ylabel, func, other_classes,
               filename, title):
    coeffs = expand_product(factors, 100)
    vanishing = [n for n in range(101) if n % modulus == residue]
    other = [n for n in range(101) if n % modulus != residue]

    fig, ax = plt.subplots(figsize=(7, 3.2), dpi=300)
    for n in other:
        ax.plot([n, n], [0, coeffs[n]], color=BLUE, lw=0.7)
        ax.plot(n, coeffs[n], "o", color=BLUE, markersize=2.0)
    for n in vanishing:
        ax.plot(n, 0, "o", color=ORANGE, markersize=3.5, zorder=5)
    ax.axhline(y=0, color="#999999", lw=0.4, zorder=0)

    ax.set_xlabel("$n$", fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.set_xlim(-1, 101)

    legend = [
        Line2D([0], [0], marker="o", color=BLUE, lw=0.7, markersize=4,
               label=f"{ylabel}: residue classes {other_classes} (mod {modulus})"),
        Line2D([0], [0], marker="o", color=ORANGE, lw=0, markersize=5,
               label=f"${func}({modulus}n+{residue}) = 0$: "
                     f"residue class {residue} (mod {modulus})"),
    ]
    ax.legend(handles=legend, fontsize=7.2, loc="upper left",
              framealpha=0.9, edgecolor="#cccccc")
    ax.tick_params(labelsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    out = os.path.join(RESULTS, filename)
    plt.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.1,
                facecolor="white", edgecolor="none")
    plt.close()
    print(f"  wrote {out}")


def main():
    os.makedirs(RESULTS, exist_ok=True)
    print("Generating figures...")

    # Figure 2 - Richmond-Szekeres, C(4n+3) = 0
    coeff_plot(
        [Factor(3, 8, 1, False), Factor(5, 8, 1, False),
         Factor(1, 8, -1, False), Factor(7, 8, -1, False)],
        modulus=4, residue=3, ylabel="$C(n)$", func="C",
        other_classes="0, 1, 2", filename="Figure2_RichmondSzekeres.png",
        title="Richmond-Szekeres")

    # Figure 3 - Baruah-Kaur, Phi(5n+3) = 0
    coeff_plot(
        [Factor(1, 5, 1, True), Factor(4, 5, 1, True),
         Factor(4, 10, 3, False), Factor(6, 10, 3, False)],
        modulus=5, residue=3, ylabel=r"$\phi(n)$", func=r"\phi",
        other_classes="0, 1, 2, 4", filename="Figure3_BaruahKaur.png",
        title="Baruah-Kaur")

    # Figure 4 - new conjecture, G(7n+3) = 0
    coeff_plot(
        [Factor(2, 7, 1, True), Factor(5, 7, 1, True),
         Factor(4, 14, 3, False), Factor(10, 14, 3, False)],
        modulus=7, residue=3, ylabel="$G(n)$", func="G",
        other_classes="0, 1, 2, 4, 5, 6", filename="Figure4_NewConjecture.png",
        title="New conjecture")

    print("Done.")


if __name__ == "__main__":
    main()
