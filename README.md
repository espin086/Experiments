# Experiments
A streamlit application that helps calculate relevant statistics before, during, and after an experiment is conducted.


## Sample Size Calculator

This tool is designed to calculate the necessary sample size for a statistical experiment to detect differences in either proportions or means, suitable for one-tailed or two-tailed tests. It supports decision-making in various fields such as marketing, clinical trials, or education.

### Usage

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

### Arguments
- `--type`: Specify the type of data: 'proportion' for rates or percentages, 'mean' for continuous outcomes.
- `--tail`: Specify the type of test: 'one' for a one-tailed test or 'two' for a two-tailed test.
- `--delta`: The desired difference in means for 'mean' type.
- `--sigma`: Standard deviation of the measurements for 'mean' type.
- `--baseline`: Baseline value (control group rate) for proportion type experiments.
- `--effect_size`: Expected outcome rate in the experimental group for proportion type experiments.
- `--alpha`: Significance level (alpha).
- `--power`: Statistical power.
- `--split_ratio`: The ratio of the sample size allocated to the control group versus the experimental group.

### Report
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