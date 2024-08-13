# Experiments 🧪
A streamlit application that helps calculate relevant statistics before, during, and after an experiment is conducted. 

# Web Application 🌐

You can find the web application for this tool here: [testandlearn](https://testandlearn.streamlit.app/)

# Command Line Tools 🛠

## Installation
To clone a repository, create a virtual environment, install the requirements, and launch the Streamlit application, follow these steps:

1. Clone the repository using the following command:
    ```bash
    git clone https://github.com/espin086/Experiments.git
    ```

2. Change into the cloned repository directory:
    ```bash
    cd Experiments
    ```

3. Create a virtual environment using the following command:
    ```bash
    python -m venv .venv
    ```

4. Activate the virtual environment:
    - For Windows:
      ```bash
      .venv\Scripts\activate
      ```
    - For macOS/Linux:
      ```bash
      source .venv/bin/activate
      ```

5. Install the required packages from the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

6. Launch the Streamlit application using the following command:
    ```bash
    streamlit run main.py
    ```

## Statistical Significance Test Tool 📊

This tool is designed to evaluate the statistical significance of differences in either proportions or means, suitable for one-tailed or two-tailed tests. It supports decision-making in various fields such as marketing, clinical trials, or education by providing a clear indication of whether observed differences in data are statistically significant.

### Usage 📝

#### Proportion Test
For experiments involving rates or percentages:
```bash
python sig_test.py --test_type proportion --tail two --test_value 0.507 --control_value 0.4728 --n_test 25000 --n_control 25000 --confidence 0.95
```

#### Mean Test

For experiments involving continuous outcomes:

```bash
python sig_test.py --test_type mean --tail one --test_value 50 --control_value 45 --std_test 10 --std_control 10 --n_test 25000 --n_control 25000 --confidence 0.90
```

### Arguments 📚

- `--test_type`: Specify the type of data: 'proportion' for rates or percentages, 'mean' for continuous outcomes.
- `--tail`: Specify the type of test: 'one' for a one-tailed test or 'two' for a two-tailed test.
- `--test_value`: Value observed in the test group (proportion or mean).
- `--control_value`: Value observed in the control group (proportion or mean).
- `--std_test`: Standard deviation of the test group (required for mean type tests).
- `--std_control`: Standard deviation of the control group (required for mean type tests).
- `--n_test`: Sample size for the test group.
- `--n_control`: Sample size for the control group.
- `--confidence`: Confidence level for the test, typically set at 0.95.

### Results 📈

After running the tool, it will print a detailed report, including:

```bash
Results:
----------------------------
Test Type: Proportion Test
Tail Type: Two-tailed
Test Group Value: 0.507
Control Group Value: 0.4728
Test Group Size: 25000
Control Group Size: 25000
Confidence Level: 0.95
Z-Score: 2.556
P-Value: 0.0107
Significant: Yes

```





## Sample Size Calculator 🧮

This tool is designed to calculate the necessary sample size for a statistical experiment to detect differences in either proportions or means, suitable for one-tailed or two-tailed tests. It supports decision-making in various fields such as marketing, clinical trials, or education.

### Usage 📝

#### Proportion Type
For experiments involving rates or percentages:
```bash
python samplesize.py --type proportion --tail two --baseline 0.10 --effect_size 0.15 --alpha 0.05 --power 0.8 --split_ratio 0.5
```

#### Mean Type
For experiments involving continuous outcomes:
```bash
python samplesize.py --type mean --tail one --delta 5 --sigma 20 --alpha 0.05 --power 0.8 --split_ratio 0.5
```

### Arguments 📚
- `--type`: Specify the type of data: 'proportion' for rates or percentages, 'mean' for continuous outcomes.
- `--tail`: Specify the type of test: 'one' for a one-tailed test or 'two' for a two-tailed test.
- `--delta`: The desired difference in means for 'mean' type.
- `--sigma`: Standard deviation of the measurements for 'mean' type.
- `--baseline`: Baseline value (control group rate) for proportion type experiments.
- `--effect_size`: Expected outcome rate in the experimental group for proportion type experiments.
- `--alpha`: Significance level (alpha).
- `--power`: Statistical power.
- `--split_ratio`: The ratio of the sample size allocated to the control group versus the experimental group.

### Report 📄
After running the tool, a detailed report will be generated including:
```bash
Sample Size Calculation Report
----------------------------
Experiment Type: Proportion Difference
Test Type: Two-tailed
Baseline Proportion: 0.1
Desired Proportion: 0.15
Significance Level (Alpha): 0.05
Statistical Power: 0.8
Control Group Ratio: 0.5
Experimental Group Ratio: 0.5
Total Sample Size Required: 2732
Control Group Sample Size: 1366
Experimental Group Sample Size: 1366

```

🔍 **Important**: Make sure to input the correct values for your experiment. The results of the statistical tests and sample size calculations are highly dependent on the input parameters.