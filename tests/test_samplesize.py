import math
import pytest
from scipy.stats import norm
from samplesize import (
    calculate_sample_size_for_proportions,
    calculate_sample_size_for_means,
)


class TestCalculateSampleSizeForProportions:
    def test_two_tailed_basic(self):
        """Sample size calculation for two-tailed proportion test."""
        n = calculate_sample_size_for_proportions(
            baseline=0.10,
            effect_size=0.15,
            alpha=0.05,
            power=0.8,
            split_ratio=0.5,
            tail="two",
        )
        assert isinstance(n, int)
        assert n > 0

    def test_one_tailed_smaller_than_two_tailed(self):
        """One-tailed test requires smaller sample than two-tailed at same alpha."""
        n_two = calculate_sample_size_for_proportions(0.10, 0.15, 0.05, 0.8, 0.5, "two")
        n_one = calculate_sample_size_for_proportions(0.10, 0.15, 0.05, 0.8, 0.5, "one")
        assert n_one < n_two

    def test_larger_effect_requires_smaller_sample(self):
        n_small_effect = calculate_sample_size_for_proportions(
            0.10, 0.12, 0.05, 0.8, 0.5, "two"
        )
        n_large_effect = calculate_sample_size_for_proportions(
            0.10, 0.20, 0.05, 0.8, 0.5, "two"
        )
        assert n_small_effect > n_large_effect

    def test_higher_power_requires_larger_sample(self):
        n_low_power = calculate_sample_size_for_proportions(
            0.10, 0.15, 0.05, 0.8, 0.5, "two"
        )
        n_high_power = calculate_sample_size_for_proportions(
            0.10, 0.15, 0.05, 0.9, 0.5, "two"
        )
        assert n_high_power > n_low_power

    def test_returns_ceiling_integer(self):
        n = calculate_sample_size_for_proportions(0.10, 0.15, 0.05, 0.8, 0.5, "two")
        assert n == math.ceil(n)

    def test_known_value_two_tailed(self):
        """Validate against manually computed value for a well-known input."""
        n = calculate_sample_size_for_proportions(0.10, 0.15, 0.05, 0.8, 0.5, "two")
        # Computed: z_alpha=1.96, z_beta=0.842
        z_alpha = norm.ppf(0.975)
        z_beta = norm.ppf(0.8)
        raw = ((z_alpha + z_beta) ** 2) * ((0.10 * 0.90 + 0.15 * 0.85) / (0.05 ** 2))
        expected = math.ceil(raw / (0.5 * 0.5))
        assert n == expected


class TestCalculateSampleSizeForMeans:
    def test_two_tailed_basic(self):
        """Sample size for a two-tailed mean difference test."""
        n = calculate_sample_size_for_means(
            delta=5, sigma=20, alpha=0.05, power=0.8, split_ratio=0.5, tail="two"
        )
        assert isinstance(n, int)
        assert n > 0

    def test_one_tailed_smaller_than_two_tailed(self):
        n_two = calculate_sample_size_for_means(5, 20, 0.05, 0.8, 0.5, "two")
        n_one = calculate_sample_size_for_means(5, 20, 0.05, 0.8, 0.5, "one")
        assert n_one < n_two

    def test_larger_delta_requires_smaller_sample(self):
        n_small_delta = calculate_sample_size_for_means(2, 20, 0.05, 0.8, 0.5, "two")
        n_large_delta = calculate_sample_size_for_means(10, 20, 0.05, 0.8, 0.5, "two")
        assert n_small_delta > n_large_delta

    def test_higher_power_requires_larger_sample(self):
        n_low = calculate_sample_size_for_means(5, 20, 0.05, 0.8, 0.5, "two")
        n_high = calculate_sample_size_for_means(5, 20, 0.05, 0.9, 0.5, "two")
        assert n_high > n_low

    def test_returns_ceiling_integer(self):
        n = calculate_sample_size_for_means(5, 20, 0.05, 0.8, 0.5, "two")
        assert n == math.ceil(n)

    def test_known_value_two_tailed(self):
        """Validate against manually computed value."""
        n = calculate_sample_size_for_means(5, 20, 0.05, 0.8, 0.5, "two")
        z_alpha = norm.ppf(0.975)
        z_beta = norm.ppf(0.8)
        raw = (2 * (20 ** 2) * (z_alpha + z_beta) ** 2) / (5 ** 2)
        expected = math.ceil(raw / (0.5 * 0.5))
        assert n == expected
