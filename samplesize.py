import argparse
from scipy.stats import norm
import math


def calculate_sample_size_for_proportions(
    baseline, effect_size, alpha, power, split_ratio, tail
):
    """Calculate the sample size needed for comparing two proportions with specified significance and power."""
    if tail == "two":
        z_alpha = norm.ppf(1 - alpha / 2)
    else:
        z_alpha = norm.ppf(1 - alpha)
    z_beta = norm.ppf(power)
    p0 = baseline
    p1 = effect_size
    effect_size = abs(p1 - p0)
    sample_size = ((z_alpha + z_beta) ** 2) * (
        (p0 * (1 - p0) + p1 * (1 - p1)) / effect_size**2
    )
    control_share = split_ratio
    test_share = 1 - split_ratio
    adjusted_sample_size = sample_size / (control_share * test_share)
    return math.ceil(adjusted_sample_size)


def calculate_sample_size_for_means(delta, sigma, alpha, power, split_ratio, tail):
    """Calculate the sample size needed for detecting a specified difference in means with given variance, significance, and power."""
    if tail == "two":
        z_alpha = norm.ppf(1 - alpha / 2)
    else:
        z_alpha = norm.ppf(1 - alpha)
    z_beta = norm.ppf(power)
    sample_size = (2 * (sigma**2) * (z_alpha + z_beta) ** 2) / (delta**2)
    control_share = split_ratio
    test_share = 1 - split_ratio
    adjusted_sample_size = sample_size / (control_share * test_share)
    return math.ceil(adjusted_sample_size)


def main():
    parser = argparse.ArgumentParser(
        description="""
    This tool calculates the necessary sample size for a statistical experiment to detect differences in either proportions or means, suitable for one-tailed or two-tailed tests. It's specifically designed to support robust decision-making in various fields such as marketing, clinical trials, or education.

    The tool allows users to tailor their experiment design by specifying whether they're measuring proportions (such as conversion rates or click-through rates) or means (such as average spending or satisfaction scores).

    Examples of usage:
    1. Marketing Email Campaign:
       - You want to determine if a new email template increases the click-through rate from a baseline of 10% to an expected 15% with a 95% confidence level and 80% power. You plan to split your sample equally between the control and test groups.
       Command:
       python samplesize.py --type proportion --tail two --baseline 0.10 --effect_size 0.15 --alpha 0.05 --power 0.8 --split_ratio 0.5

    2. Pricing Strategy Evaluation:
       - Your company plans to test a new pricing strategy that is expected to increase average customer spending by $5. Assuming the standard deviation of spending is $20, you want to detect this change with a 95% confidence level and 80% power, using a one-tailed test.
       Command:
       python samplesize.py --type mean --tail one --delta 5 --sigma 20 --alpha 0.05 --power 0.8 --split_ratio 0.5
    """,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--type",
        choices=["proportion", "mean"],
        help="Specify the type of data: 'proportion' for rates or percentages, 'mean' for continuous outcomes.",
        required=True,
    )
    parser.add_argument(
        "--tail",
        choices=["one", "two"],
        help="Specify the type of test: 'one' for a one-tailed test or 'two' for a two-tailed test.",
        required=True,
    )
    parser.add_argument(
        "--delta",
        type=float,
        help="The desired difference in means for 'mean' type (e.g., a 5 point increase in customer satisfaction score).",
        required=False,
    )
    parser.add_argument(
        "--sigma",
        type=float,
        help="Standard deviation of the measurements for 'mean' type (e.g., standard deviation of spending amounts in dollars).",
        required=False,
    )
    parser.add_argument(
        "--baseline",
        type=float,
        help="Baseline value (control group rate) for proportion type experiments (e.g., a baseline click-through rate of 10 percent).",
        required=False,
    )
    parser.add_argument(
        "--effect_size",
        type=float,
        help="Expected outcome rate in the experimental group for proportion type experiments (e.g., expected click-through rate of 15 percent).",
        required=False,
    )
    parser.add_argument(
        "--alpha",
        type=float,
        help="Significance level (alpha) - the probability of a Type I error (false positive), commonly set at 0.05.",
        required=True,
    )
    parser.add_argument(
        "--power",
        type=float,
        help="Statistical power - the probability of a Type II error (false negative), commonly set at 0.8.",
        required=True,
    )
    parser.add_argument(
        "--split_ratio",
        type=float,
        help="The ratio of the sample size allocated to the control group versus the experimental group (e.g., 0.5 for a 50/50 split).",
        required=True,
    )

    args = parser.parse_args()

    if args.type == "proportion":
        if not all([args.baseline, args.effect_size]):
            parser.error(
                "Baseline and effect size must be provided for proportion type."
            )
        sample_size = calculate_sample_size_for_proportions(
            args.baseline,
            args.effect_size,
            args.alpha,
            args.power,
            args.split_ratio,
            args.tail,
        )
    elif args.type == "mean":
        if not all([args.delta, args.sigma]):
            parser.error("Delta and sigma must be provided for mean type.")
        sample_size = calculate_sample_size_for_means(
            args.delta, args.sigma, args.alpha, args.power, args.split_ratio, args.tail
        )

    # Generate a detailed report of the results
    print("\nSample Size Calculation Report")
    print("----------------------------")
    print(f"Experiment Type: {args.type.capitalize()} Difference")
    print(f"Test Type: {'Two-tailed' if args.tail == 'two' else 'One-tailed'}")
    if args.type == "proportion":
        print(f"Baseline Proportion: {args.baseline}")
        print(f"Desired Proportion: {args.effect_size}")
    else:
        print(f"Desired Mean Difference: {args.delta}")
        print(f"Standard Deviation: {args.sigma}")
    print(f"Significance Level (Alpha): {args.alpha}")
    print(f"Statistical Power: {args.power}")
    print(f"Control Group Ratio: {args.split_ratio}")
    print(f"Experimental Group Ratio: {1 - args.split_ratio}")
    print(f"Total Sample Size Required: {sample_size}")
    print(f"Control Group Sample Size: {math.ceil(sample_size * args.split_ratio)}")
    print(
        f"Experimental Group Sample Size: {math.ceil(sample_size * (1 - args.split_ratio))}\n"
    )


if __name__ == "__main__":
    main()
