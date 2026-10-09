"""
Exploratory Data Analysis — Psychometric Data
Smartick Dataset (OpenNeuro ds006260)

Loads 01_Psychometric_Data.xlsx (READING + MATH sheets),
computes descriptive stats, plots distributions, change scores,
correlations, and baseline group comparisons.
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

# ── Paths ──────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "01_Psychometric_Data.xlsx"
OUT = Path(__file__).resolve().parent / "results" / "eda"
OUT.mkdir(parents=True, exist_ok=True)

# ── Load ───────────────────────────────────────────────────────────────
df_reading = pd.read_excel(DATA, sheet_name="READING")
df_math = pd.read_excel(DATA, sheet_name="MATH")

# Rename GROUP column for consistency
df_reading.rename(columns={"GROUP": "Subgroup"}, inplace=True)
df_math.rename(columns={"GROUP": "Subgroup"}, inplace=True)

# ── Helper: descriptive table ──────────────────────────────────────────
def desc_table(df, dvs, group_col="Subgroup"):
    rows = []
    for grp in sorted(df[group_col].unique()):
        for session in ["PRE", "POST"]:
            for dv in dvs:
                col = f"{dv}_{session}"
                sub = df[df[group_col] == grp]
                rows.append({
                    "Group": grp,
                    "Session": session,
                    "DV": dv,
                    "Mean": sub[col].mean(),
                    "SD": sub[col].std(),
                    "Median": sub[col].median(),
                    "Min": sub[col].min(),
                    "Max": sub[col].max(),
                    "n": len(sub),
                })
    return pd.DataFrame(rows)


# =====================================================================
# 1. COHORT OVERVIEW
# =====================================================================
print("=" * 60)
print("COHORT OVERVIEW")
print("=" * 60)

for name, df in [("READING", df_reading), ("MATH", df_math)]:
    print(f"\n--- {name} group ---")
    print(f"  N = {len(df)}")
    for grp in sorted(df.Subgroup.unique()):
        sub = df[df.Subgroup == grp]
        print(f"  Subgroup {grp}: n = {len(sub)}")
        print(f"    Gender: {sub.GENDER.value_counts().to_dict()}")
        print(f"    Age: {sub.AGE.describe()[['mean','std','min','max']]}")
        print(f"    IQ:  {sub.IQ.describe()[['mean','std','min','max']]}")

# =====================================================================
# 2. DESCRIPTIVE STATISTICS
# =====================================================================
print("\n" + "=" * 60)
print("DESCRIPTIVE STATISTICS")
print("=" * 60)

reading_dvs = [
    "Orthographic_ERR", "Phonological_ERR", "Selective_Attention",
    "Reading_Speed", "Comprehension"
]
math_dvs = [
    "WRAT4", "hits", "RT", "Selective_Attention"
]

print("\n--- READING DVs ---")
tbl_r = desc_table(df_reading, reading_dvs)
print(tbl_r.to_string(index=False))
tbl_r.to_csv(OUT / "descriptives_reading.csv", index=False)

print("\n--- MATH DVs ---")
tbl_m = desc_table(df_math, math_dvs)
print(tbl_m.to_string(index=False))
tbl_m.to_csv(OUT / "descriptives_math.csv", index=False)

# =====================================================================
# 3. BASELINE EQUIDANCE  (E vs C on PRE scores + age + IQ)
# =====================================================================
print("\n" + "=" * 60)
print("BASELINE COMPARISON (E vs C)")
print("=" * 60)

baseline_checks = ["AGE", "IQ"] + [f"{dv}_PRE" for dv in reading_dvs]
baseline_checks_m = ["AGE", "IQ"] + [f"{dv}_PRE" for dv in math_dvs]


def baseline_comparison(df, dvs, label):
    rows = []
    grp_e = df[df.Subgroup == "E"]
    grp_c = df[df.Subgroup == "C"]
    for dv in ["AGE", "IQ"] + [f"{dv}_PRE" for dv in dvs]:
        vals_e = grp_e[dv].dropna()
        vals_c = grp_c[dv].dropna()
        if len(vals_e) < 2 or len(vals_c) < 2:
            continue
        stat, p = stats.mannwhitneyu(vals_e, vals_c, alternative="two-sided")
        rows.append({"Variable": dv,
                      "Mean_E": vals_e.mean(), "Mean_C": vals_c.mean(),
                      "U": stat, "p": p})
    res = pd.DataFrame(rows)
    # Gender chi-square
    tbl = pd.crosstab(df.Subgroup, df.GENDER)
    chi2, p_g, _, _ = stats.chi2_contingency(tbl)
    print(f"\n--- {label} gender chi² = {chi2:.3f}, p = {p_g:.4f} ---")
    print(res.to_string(index=False))
    res.to_csv(OUT / f"baseline_{label.lower()}.csv", index=False)

baseline_comparison(df_reading, reading_dvs, "Reading")
baseline_comparison(df_math, math_dvs, "Math")


# =====================================================================
# 4. PAIRED BOX + STRIP PLOTS  (PRE vs POST by group)
# =====================================================================
sns.set_style("whitegrid")
sns.set_context("talk")

for name, df, dvs in [
    ("reading", df_reading, reading_dvs),
    ("math", df_math, math_dvs),
]:
    for dv in dvs:
        fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
        for i, grp in enumerate(["E", "C"]):
            ax = axes[i]
            sub = df[df.Subgroup == grp].copy()
            melted = sub.melt(
                id_vars=["Subject"],
                value_vars=[f"{dv}_PRE", f"{dv}_POST"],
                var_name="Session", value_name=dv,
            )
            melted["Session"] = melted["Session"].str.extract(r"(PRE|POST)")
            sns.boxplot(
                data=melted, x="Session", y=dv, ax=ax,
                palette={"PRE": "#5B9BD5", "POST": "#ED7D31"},
                width=0.4, fliersize=0,
            )
            sns.stripplot(
                data=melted, x="Session", y=dv, ax=ax,
                palette={"PRE": "#5B9BD5", "POST": "#ED7D31"},
                size=5, alpha=0.6, jitter=0.15, edgecolor="gray", linewidth=0.5,
            )
            # connecting lines per subject
            for _, row in sub.iterrows():
                ax.plot(
                    [0, 1], [row[f"{dv}_PRE"], row[f"{dv}_POST"]],
                    color="gray", alpha=0.25, linewidth=0.8,
                )
            ax.set_title(f"Group {grp}", fontsize=13)
            ax.set_ylabel(dv.replace("_", " "))
        fig.suptitle(f"{name.upper()} — {dv}", fontsize=14, y=1.02)
        fig.tight_layout()
        fig.savefig(OUT / f"boxplot_{name}_{dv}.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

# =====================================================================
# 5. CHANGE-SCORE (POST − PRE) DISTRIBUTIONS
# =====================================================================
for name, df, dvs in [
    ("reading", df_reading, reading_dvs),
    ("math", df_math, math_dvs),
]:
    for dv in dvs:
        fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
        for i, grp in enumerate(["E", "C"]):
            ax = axes[i]
            sub = df[df.Subgroup == grp]
            delta = sub[f"{dv}_POST"] - sub[f"{dv}_PRE"]
            sns.histplot(delta, kde=True, ax=ax, color="#70AD47", edgecolor="white")
            ax.axvline(delta.mean(), color="red", ls="--", lw=1.5,
                       label=f"mean={delta.mean():.2f}")
            ax.legend(fontsize=10)
            ax.set_title(f"Group {grp}", fontsize=13)
            ax.set_xlabel(f"{dv} change (POST−PRE)")
        fig.suptitle(f"Change Scores — {name.upper()} — {dv}", fontsize=14, y=1.02)
        fig.tight_layout()
        fig.savefig(OUT / f"change_{name}_{dv}.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

# =====================================================================
# 6. CORRELATION HEATMAPS  (PRE scores)
# =====================================================================
for name, df, dvs in [
    ("reading", df_reading, reading_dvs),
    ("math", df_math, math_dvs),
]:
    corr_cols = [f"{dv}_PRE" for dv in dvs]
    fig, ax = plt.subplots(figsize=(8, 6))
    corr = df[corr_cols].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r",
                center=0, vmin=-1, vmax=1, ax=ax,
                xticklabels=[c.replace("_PRE", "").replace("_", " ") for c in corr_cols],
                yticklabels=[c.replace("_PRE", "").replace("_", " ") for c in corr_cols])
    ax.set_title(f"{name.upper()} — PRE scores correlation", fontsize=13)
    fig.tight_layout()
    fig.savefig(OUT / f"corr_{name}_pre.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

# =====================================================================
# 7. AGE / IQ SCATTER WITH DVs
# =====================================================================
for name, df, dvs in [
    ("reading", df_reading, reading_dvs),
    ("math", df_math, math_dvs),
]:
    for cov in ["AGE", "IQ"]:
        n_dvs = len(dvs)
        fig, axes = plt.subplots(1, n_dvs, figsize=(4 * n_dvs, 4), sharey=False)
        if n_dvs == 1:
            axes = [axes]
        for j, dv in enumerate(dvs):
            ax = axes[j]
            sns.scatterplot(
                data=df, x=cov, y=f"{dv}_PRE", hue="Subgroup",
                style="Subgroup", s=60, ax=ax, alpha=0.7,
            )
            ax.set_ylabel(f"{dv} (PRE)")
            ax.set_xlabel(cov)
        fig.suptitle(f"{name.upper()} — {cov} vs PRE DVs", fontsize=14, y=1.02)
        fig.tight_layout()
        fig.savefig(OUT / f"scatter_{name}_{cov.lower()}_pre.png",
                    dpi=150, bbox_inches="tight")
        plt.close(fig)

# =====================================================================
# SUMMARY
# =====================================================================
print("\n" + "=" * 60)
print(f"EDA complete — figures saved to {OUT}")
print("=" * 60)
