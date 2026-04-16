import pytest
import numpy as np
from scipy.stats import norm
from sig_test import calculate_z_score, calculate_p_value


class TestCalculateZScore:
    def test_two_tailed_proportion_from_issue(self):
        """Validate z-score against the Excel formulas described in issue #1.

        Issue data: test=0.507, control=0.4728, n_test=25000, n_control=25000
        Pooled p* = (25000*0.507 + 25000*0.4728) / 50000 = 0.4899
        SE = sqrt(p*(1-p)*(1/n1+1/n2))
        z = (0.507 - 0.4728) / SE
        """
        z = calculate_z_score(0.507, 0.4728, 25000, 25000)
        pooled_p = (25000 * 0.507 + 25000 * 0.4728) / 50000
        se = np.sqrt(pooled_p * (1 - pooled_p) * (1 / 25000 + 1 / 25000))
        expected_z = (0.507 - 0.4728) / se
        assert abs(z - expected_z) < 1e-10

    def test_pooled_standard_error_formula(self):
        """SE with pooled proportion matches Excel SQRT((p*(1-p)*(N1+N2))/(N1*N2))."""
        z = calculate_z_score(0.3, 0.25, 1000, 1000)
        pooled_p = (1000 * 0.3 + 1000 * 0.25) / 2000
        # Excel formula: SQRT((p*(1-p)*(N1+N2))/(N1*N2)) == sqrt(p*(1-p)*(1/N1+1/N2))
        se = np.sqrt(pooled_p * (1 - pooled_p) * 2000 / (1000 * 1000))
        expected_z = (0.3 - 0.25) / se
        assert abs(z - expected_z) < 1e-10

    def test_unpooled_standard_error(self):
        """Non-pooled SE uses each group's own proportion."""
        z = calculate_z_score(0.3, 0.25, 1000, 1000, pooled=False)
        se = np.sqrt(0.3 * 0.7 / 1000 + 0.25 * 0.75 / 1000)
        expected_z = (0.3 - 0.25) / se
        assert abs(z - expected_z) < 1e-10

    def test_no_difference_gives_zero_z_score(self):
        z = calculate_z_score(0.5, 0.5, 1000, 1000)
        assert z == 0.0

    def test_negative_z_score_when_test_less_than_control(self):
        z = calculate_z_score(0.3, 0.5, 1000, 1000)
        assert z < 0

    def test_different_sample_sizes(self):
        z = calculate_z_score(0.4, 0.3, 500, 1500)
        pooled_p = (500 * 0.4 + 1500 * 0.3) / 2000
        se = np.sqrt(pooled_p * (1 - pooled_p) * (1 / 500 + 1 / 1500))
        expected_z = (0.4 - 0.3) / se
        assert abs(z - expected_z) < 1e-10


class TestCalculatePValue:
    def test_two_tailed_pvalue_from_issue(self):
        """p-value matches Excel =2*(1-NORMSDIST(ABS(z))) as described in issue #1."""
        z = calculate_z_score(0.507, 0.4728, 25000, 25000)
        p = calculate_p_value(z, "two")
        expected_p = 2 * (1 - norm.cdf(abs(z)))
        assert abs(p - expected_p) < 1e-10

    def test_two_tailed_significant_at_80pct_confidence(self):
        """Issue example is SIGNIFICANT at 80% confidence (alpha=0.20)."""
        z = calculate_z_score(0.507, 0.4728, 25000, 25000)
        p = calculate_p_value(z, "two")
        assert p < 0.20

    def test_two_tailed_symmetric(self):
        """Two-tailed p-value is the same for +z and -z."""
        p_pos = calculate_p_value(2.0, "two")
        p_neg = calculate_p_value(-2.0, "two")
        assert abs(p_pos - p_neg) < 1e-10

    def test_one_tailed_pvalue(self):
        z = 1.645
        p = calculate_p_value(z, "one")
        expected_p = 1 - norm.cdf(abs(z))
        assert abs(p - expected_p) < 1e-10

    def test_two_tailed_is_double_one_tailed(self):
        z = 1.96
        p_two = calculate_p_value(z, "two")
        p_one = calculate_p_value(z, "one")
        assert abs(p_two - 2 * p_one) < 1e-10

    def test_pvalue_between_zero_and_one(self):
        for z in [-3.0, -1.0, 0.0, 1.0, 3.0]:
            p = calculate_p_value(z, "two")
            assert 0.0 <= p <= 1.0

    def test_large_z_gives_small_pvalue(self):
        p = calculate_p_value(10.0, "two")
        assert p < 0.0001

    def test_zero_z_gives_pvalue_one(self):
        p = calculate_p_value(0.0, "two")
        assert abs(p - 1.0) < 1e-10
