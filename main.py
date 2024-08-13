import streamlit as st
from sig_test import calculate_z_score, calculate_p_value
from samplesize import (
    calculate_sample_size_for_proportions,
    calculate_sample_size_for_means,
)
import numpy as np
import math


def main():
    st.title("Statistical Tools")

    tab1, tab2 = st.tabs(["Statistical Significance Test", "Sample Size Calculator"])

    with tab1:
        st.header("Statistical Significance Test Tool")

        st.sidebar.header("Test Configuration")

        test_type = st.sidebar.selectbox(
            "Select Test Type", ["proportion", "mean"], key="test_type"
        )
        tail_type = st.sidebar.selectbox(
            "Select Tail Type", ["one", "two"], key="tail_type"
        )
        test_value = st.sidebar.number_input(
            "Test Group Value", value=0.0, key="test_value"
        )
        control_value = st.sidebar.number_input(
            "Control Group Value", value=0.0, key="control_value"
        )
        n_test = st.sidebar.number_input("Test Group Size", value=0, key="n_test")
        n_control = st.sidebar.number_input(
            "Control Group Size", value=0, key="n_control"
        )
        confidence = st.sidebar.slider(
            "Confidence Level", 0.90, 0.99, 0.95, key="confidence"
        )

        std_test = std_control = None
        if test_type == "mean":
            std_test = st.sidebar.number_input(
                "Test Group Std Dev", value=0.0, key="std_test"
            )
            std_control = st.sidebar.number_input(
                "Control Group Std Dev", value=0.0, key="std_control"
            )

        if st.sidebar.button("Calculate", key="calculate_significance"):
            if test_type == "mean" and (std_test is None or std_control is None):
                st.error("Standard deviations must be provided for mean type tests.")
            else:
                if test_type == "proportion":
                    z_score = calculate_z_score(
                        test_value, control_value, n_test, n_control
                    )
                elif test_type == "mean":
                    std_err = np.sqrt(
                        (std_test**2 / n_test) + (std_control**2 / n_control)
                    )
                    z_score = (test_value - control_value) / std_err

                p_value = calculate_p_value(z_score, tail_type)
                significance = p_value < (1 - confidence)

                st.subheader("Results")
                st.write(f"**Test Type:** {test_type.capitalize()} Test")
                st.write(
                    f"**Tail Type:** {'Two-tailed' if tail_type == 'two' else 'One-tailed'}"
                )
                st.write(f"**Test Group Value:** {test_value}")
                st.write(f"**Control Group Value:** {control_value}")
                if test_type == "mean":
                    st.write(f"**Test Group Std Dev:** {std_test}")
                    st.write(f"**Control Group Std Dev:** {std_control}")
                st.write(f"**Test Group Size:** {n_test}")
                st.write(f"**Control Group Size:** {n_control}")
                st.write(f"**Confidence Level:** {confidence}")
                st.write(f"**Z-Score:** {z_score}")
                st.write(f"**P-Value:** {p_value:.4f}")
                st.write(f"**Significant:** {'Yes' if significance else 'No'}")

    with tab2:
        st.header("Sample Size Calculator")

        sample_type = st.selectbox(
            "Select Sample Type", ["proportion", "mean"], key="sample_type"
        )
        tail_type = st.selectbox(
            "Select Tail Type", ["one", "two"], key="sample_tail_type"
        )
        alpha = st.number_input("Significance Level (alpha)", value=0.05, key="alpha")
        power = st.number_input("Statistical Power", value=0.8, key="power")
        split_ratio = st.number_input(
            "Control Group Ratio",
            value=0.5,
            min_value=0.0,
            max_value=1.0,
            key="split_ratio",
        )

        if sample_type == "proportion":
            baseline = st.number_input("Baseline Proportion", value=0.0, key="baseline")
            effect_size = st.number_input(
                "Expected Proportion in Test Group", value=0.0, key="effect_size"
            )
            if st.button(
                "Calculate Sample Size", key="calculate_sample_size_proportion"
            ):
                sample_size = calculate_sample_size_for_proportions(
                    baseline, effect_size, alpha, power, split_ratio, tail_type
                )
                st.write("**Sample Size Calculation Results**")
                st.write(f"Total Sample Size Required: {sample_size}")
                st.write(
                    f"Control Group Sample Size: {math.ceil(sample_size * split_ratio)}"
                )
                st.write(
                    f"Test Group Sample Size: {math.ceil(sample_size * (1 - split_ratio))}"
                )

        elif sample_type == "mean":
            delta = st.number_input(
                "Desired Difference in Means (delta)", value=0.0, key="delta"
            )
            sigma = st.number_input(
                "Standard Deviation (sigma)", value=0.0, key="sigma"
            )
            if st.button("Calculate Sample Size", key="calculate_sample_size_mean"):
                sample_size = calculate_sample_size_for_means(
                    delta, sigma, alpha, power, split_ratio, tail_type
                )
                st.write("**Sample Size Calculation Results**")
                st.write(f"Total Sample Size Required: {sample_size}")
                st.write(
                    f"Control Group Sample Size: {math.ceil(sample_size * split_ratio)}"
                )
                st.write(
                    f"Test Group Sample Size: {math.ceil(sample_size * (1 - split_ratio))}"
                )


if __name__ == "__main__":
    main()
