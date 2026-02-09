import math
from dataclasses import dataclass

# --- Normal CDF using erf (no SciPy needed) ---
def norm_cdf(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))

@dataclass
class PropZTestResult:
    n: int
    k: int
    p_hat: float
    p0: float
    z: float
    p_value: float
    alternative: str
    continuity_correction: bool

def one_sample_proportion_ztest(
    k: int,
    n: int,
    p0: float,
    alternative: str = "less",  # "less", "greater", "two-sided"
    continuity_correction: bool = False,
) -> PropZTestResult:
    """
    One-sample z-test for a proportion.
    - k successes out of n
    - test against p0
    - alternative: "less", "greater", or "two-sided"
    - continuity correction: adjusts p_hat by +/- 0.5/n in the direction of H1
    """
    if n <= 0:
        raise ValueError("n must be positive")
    if not (0 <= k <= n):
        raise ValueError("k must satisfy 0 <= k <= n")
    if not (0 < p0 < 1):
        raise ValueError("p0 must be in (0, 1)")
    if alternative not in {"less", "greater", "two-sided"}:
        raise ValueError('alternative must be one of: "less", "greater", "two-sided"')

    p_hat = k / n
    se = math.sqrt(p0 * (1 - p0) / n)

    # Continuity correction for proportions (common approximation):
    # Adjust p_hat by +/- 0.5/n toward the null boundary in the direction of the alternative.
    adj = 0.0
    if continuity_correction:
        if alternative == "less":
            adj = +0.5 / n   # makes z less negative (more conservative)
        elif alternative == "greater":
            adj = -0.5 / n   # makes z less positive (more conservative)
        else:
            # For two-sided, you can adjust toward p0 depending on which side p_hat is on.
            adj = -0.5 / n if p_hat > p0 else +0.5 / n

    z = (p_hat + adj - p0) / se

    if alternative == "less":
        p_value = norm_cdf(z)
    elif alternative == "greater":
        p_value = 1.0 - norm_cdf(z)
    else:  # two-sided
        p_value = 2.0 * min(norm_cdf(z), 1.0 - norm_cdf(z))

    return PropZTestResult(
        n=n,
        k=k,
        p_hat=p_hat,
        p0=p0,
        z=z,
        p_value=p_value,
        alternative=alternative,
        continuity_correction=continuity_correction,
    )

# ---- Your Section 6.1 numbers ----
n = 180
k = 131
p0 = 0.80

# One-sided (less): H1: p < 0.80  (this matches your paper's direction)
res_one = one_sample_proportion_ztest(k, n, p0, alternative="less", continuity_correction=False)
res_one_cc = one_sample_proportion_ztest(k, n, p0, alternative="less", continuity_correction=True)

# Two-sided: H1: p != 0.80
res_two = one_sample_proportion_ztest(k, n, p0, alternative="two-sided", continuity_correction=False)
res_two_cc = one_sample_proportion_ztest(k, n, p0, alternative="two-sided", continuity_correction=True)

print("=== One-sided (less), no CC ===")
print(f"p_hat={res_one.p_hat:.6f}, z={res_one.z:.4f}, p={res_one.p_value:.6g}")

print("=== One-sided (less), with CC ===")
print(f"p_hat={res_one_cc.p_hat:.6f}, z={res_one_cc.z:.4f}, p={res_one_cc.p_value:.6g}")

print("=== Two-sided, no CC ===")
print(f"p_hat={res_two.p_hat:.6f}, z={res_two.z:.4f}, p={res_two.p_value:.6g}")

print("=== Two-sided, with CC ===")
print(f"p_hat={res_two_cc.p_hat:.6f}, z={res_two_cc.z:.4f}, p={res_two_cc.p_value:.6g}")

# ---- Sensitivity sweep: at what p0 does p-value cross 0.05? ----
def find_threshold_crossing(k: int, n: int, alpha: float = 0.05,
                            alternative: str = "less",
                            continuity_correction: bool = False,
                            p0_min: float = 0.70, p0_max: float = 0.90,
                            step: float = 0.0005):
    """
    Sweeps p0 and finds the largest p0 such that p-value < alpha (i.e., still significant).
    For "less", as p0 increases, the test tends to become more significant (p decreases),
    so we report the approximate crossing point.
    """
    last_sig = None
    p0 = p0_min
    while p0 <= p0_max + 1e-12:
        r = one_sample_proportion_ztest(k, n, p0, alternative=alternative,
                                        continuity_correction=continuity_correction)
        if r.p_value < alpha:
            last_sig = p0
        p0 += step

    return last_sig

alpha = 0.05
cross_no_cc = find_threshold_crossing(k, n, alpha=alpha, alternative="less",
                                      continuity_correction=False, p0_min=0.70, p0_max=0.85)
cross_cc = find_threshold_crossing(k, n, alpha=alpha, alternative="less",
                                   continuity_correction=True, p0_min=0.70, p0_max=0.85)

print("\n=== Approx p0 where one-sided p < 0.05 starts (sweep) ===")
print(f"No CC: ~ p0 >= {cross_no_cc:.4f}" if cross_no_cc else "No CC: never significant in sweep range")
print(f"With CC: ~ p0 >= {cross_cc:.4f}" if cross_cc else "With CC: never significant in sweep range")
