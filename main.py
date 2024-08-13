import streamlit as st
from sig_test import calculate_z_score, calculate_p_value
import numpy as np


def main():
    st.title("Statistical Significance Test Tool")

    st.sidebar.header("Test Configuration")

    test_type = st.sidebar.selectbox("Select Test Type", ["proportion", "mean"])
    tail_type = st.sidebar.selectbox("Select Tail Type", ["one", "two"])
    test_value = st.sidebar.number_input("Test Group Value", value=0.0)
    control_value = st.sidebar.number_input("Control Group Value", value=0.0)
    n_test = st.sidebar.number_input("Test Group Size", value=0)
    n_control = st.sidebar.number_input("Control Group Size", value=0)
    confidence = st.sidebar.slider("Confidence Level", 0.90, 0.99, 0.95)

    std_test = std_control = None
    if test_type == "mean":
        std_test = st.sidebar.number_input("Test Group Std Dev", value=0.0)
        std_control = st.sidebar.number_input("Control Group Std Dev", value=0.0)

    if st.sidebar.button("Calculate"):
        if test_type == "mean" and (std_test is None or std_control is None):
            st.error("Standard deviations must be provided for mean type tests.")
        else:
            if test_type == "proportion":
                z_score = calculate_z_score(
                    test_value, control_value, n_test, n_control
                )
            elif test_type == "mean":
                std_err = np.sqrt((std_test**2 / n_test) + (std_control**2 / n_control))
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


if __name__ == "__main__":
    main()
