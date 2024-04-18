import argparse
import scipy.stats as stats
import numpy as np


def calculate_z_score(test_prop, control_prop, n_test, n_control, pooled=True):
    if pooled:
        pooled_prop = (test_prop * n_test + control_prop * n_control) / (
            n_test + n_control
        )
        std_err = np.sqrt(
            pooled_prop * (1 - pooled_prop) * (1 / n_test + 1 / n_control)
        )
    else:
        std_err = np.sqrt(
            test_prop * (1 - test_prop) / n_test
            + control_prop * (1 - control_prop) / n_control
        )

    z_score = (test_prop - control_prop) / std_err
    return z_score


def calculate_p_value(z_score, tail_type):
    if tail_type == "two":
        p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
    elif tail_type == "one":
        p_value = 1 - stats.norm.cdf(abs(z_score))
    return p_value


def main():
    parser = argparse.ArgumentParser(
        description="""
        This tool evaluates the statistical significance of differences in either proportions or means, suitable for one-tailed or two-tailed tests. It's designed for use in fields such as marketing, clinical trials, or educational research.

        Specify whether you're testing differences in proportions (such as conversion rates) or means (such as average customer spend).

        Examples of usage:
        1. Proportion Test:
           - Assess if two different conversion rates are statistically significant with a sample size of 25000 each at a 95% confidence level.
           Command:
           python sig_test.py --test_type proportion --tail two --test_value 0.507 --control_value 0.4728 --n_test 25000 --n_control 25000 --confidence 0.95

        2. Mean Test:
           - Determine if the difference in average spend between two groups is significant, assuming a standard deviation of 10.
           Command:
           python sig_test.py --test_type mean --tail one --test_value 50 --control_value 45 --std_test 10 --std_control 10 --n_test 25000 --n_control 25000 --confidence 0.90
        """,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--test_type",
        type=str,
        choices=["proportion", "mean"],
        required=True,
        help="Specify the type of data: 'proportion' for rates or percentages, 'mean' for continuous outcomes.",
    )
    parser.add_argument(
        "--tail",
        type=str,
        choices=["one", "two"],
        required=True,
        help="Specify the type of test: 'one' for a one-tailed test or 'two' for a two-tailed test.",
    )
    parser.add_argument(
        "--test_value", type=float, required=True, help="Test group proportion or mean."
    )
    parser.add_argument(
        "--control_value",
        type=float,
        required=True,
        help="Control group proportion or mean.",
    )
    parser.add_argument(
        "--std_test",
        type=float,
        required=False,
        help="Standard deviation of the test group (required for mean type tests).",
    )
    parser.add_argument(
        "--std_control",
        type=float,
        required=False,
        help="Standard deviation of the control group (required for mean type tests).",
    )
    parser.add_argument(
        "--n_test", type=int, required=True, help="Sample size for the test group."
    )
    parser.add_argument(
        "--n_control",
        type=int,
        required=True,
        help="Sample size for the control group.",
    )
    parser.add_argument(
        "--confidence",
        type=float,
        default=0.95,
        help="Confidence level for the test (default is 0.95).",
    )

    args = parser.parse_args()

    if args.test_type == "mean" and (args.std_test is None or args.std_control is None):
        parser.error("Standard deviations must be provided for mean type tests.")

    if args.test_type == "proportion":
        z_score = calculate_z_score(
            args.test_value, args.control_value, args.n_test, args.n_control
        )
    elif args.test_type == "mean":
        std_err = np.sqrt(
            (args.std_test**2 / args.n_test) + (args.std_control**2 / args.n_control)
        )
        z_score = (args.test_value - args.control_value) / std_err

    p_value = calculate_p_value(z_score, args.tail)
    significance = p_value < (1 - args.confidence)

    print("\nResults:")
    print("----------------------------")
    print(f"Test Type: {args.test_type.capitalize()} Test")
    print(f"Tail Type: {'Two-tailed' if args.tail == 'two' else 'One-tailed'}")
    print(f"Test Group Value: {args.test_value}")
    print(f"Control Group Value: {args.control_value}")
    if args.test_type == "mean":
        print(f"Test Group Std Dev: {args.std_test}")
        print(f"Control Group Std Dev: {args.std_control}")
    print(f"Test Group Size: {args.n_test}")
    print(f"Control Group Size: {args.n_control}")
    print(f"Confidence Level: {args.confidence}")
    print(f"Z-Score: {z_score}")
    print(f"P-Value: {p_value:.4f}")
    print(f"Significant: {'Yes' if significance else 'No'}")


if __name__ == "__main__":
    main()
