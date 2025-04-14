
# Exploratory Data Analysis - Heart Disease Dataset

This document summarizes the EDA conducted on the UCI Heart Disease dataset, focusing on the relationship between features and the `num` variable, which encodes the presence and severity of heart disease.

## Dataset Overview

- **Samples**: 303
- **Features**: 13 (excluding the target `num`)
- **Target Variable**: `num` (0 = no disease, 1–4 = varying severity)
- **Missing Values**: Present in `ca` (4 missing) and `thal` (2 missing)

---

## Target Variable Distribution

![Target Distribution](image/eda_target_distribution.png)

- Majority class: `num = 0` (no disease)
- Class imbalance exists; higher severity classes have fewer instances.

---

## Missing Values

- Only `ca` and `thal` contain missing values.
- Should be imputed or removed before modeling.

### Missing Data Visualizations
- Bar chart: ![Missing Bar](image/eda_missing_values_bar.png)
- Matrix: ![Missing Matrix](image/eda_missing_values_matrix.png)

---

## Feature-wise Visualizations vs Heart Disease Stage (`num`)

### Age
![Age](image/eda_age_vs_num.png)  
- Older patients generally show higher heart disease severity.

### Sex
![Sex](image/eda_sex_vs_num_normalized.png)  
- Males (`sex=1`) more represented in higher severity stages.

### Chest Pain Type (`cp`)
![CP](image/eda_cp_vs_num_normalized.png)  
- `cp=4` (asymptomatic) is most common among patients with disease.

### Resting Blood Pressure (`trestbps`)
![Trestbps](image/eda_trestbps_vs_num.png)  
- No strong trend; slight increase in medians with severity.

### Serum Cholesterol (`chol`)
![Chol](image/eda_chol_vs_num.png)  
- High variance across all stages; not a clear indicator.

### Fasting Blood Sugar (`fbs`)
![FBS](image/eda_fbs_vs_num_normalized.png)  
- Mostly `fbs=0`. No meaningful variation in fasting blood sugar across disease stages, indicating limited predictive value.

### Resting ECG (`restecg`)
![RestECG](image/eda_restecg_vs_num_normalized.png)  
-  `restecg=1` becomes more common as heart disease severity increases. `restecg=2` does not show a clear trend.

### Max Heart Rate Achieved (`thalach`)
![Thalach](image/eda_thalach_vs_num.png)  
- Inversely correlated with disease severity.

### Exercise-Induced Angina (`exang`)
![Exang](image/eda_exang_vs_num_normalized.png)  
- Strong association: `exang=1` (yes) more common with `num > 0`.

### ST Depression (`oldpeak`)
![Oldpeak](image/eda_oldpeak_vs_num.png)  
- Clear upward trend with disease severity.

### Slope of ST Segment (`slope`)
![Slope](image/eda_slope_vs_num_normalized.png)  
- Flat (`2`) and downsloping (`3`) more frequent in disease.

### Number of Vessels Colored (`ca`)
![CA](image/eda_ca_vs_num_normalized.png)  
- Strongly correlated with disease. Higher `ca` values associated with higher `num`.

### Thalassemia (`thal`)
![Thal](image/eda_thal_vs_num_normalized.png)  
- Fixed (6) and reversible (7) defects more frequent with disease.

---

## Correlation Matrix

![Correlation Matrix](image/eda_correlation_matrix.png)

**Top positively correlated with `num`:**
- `ca`: 0.52
- `thal`: 0.51
- `oldpeak`: 0.50
- `thalach`: -0.42 (inverse)
- `cp` : 0.41
- `exang`: 0.40

---

## PCA Analysis

Principal Component Analysis (PCA) was conducted to understand feature interactions and reduce dimensionality.

### Explained Variance
![Explained Variance Ratio](image/pca.png)  
- PC1 explains ~23% of variance, PC2 ~12%, PC3 ~9.5%.
- First 5–6 PCs explain most of the variance and therefore dimensionality reduction is possible.

### Component Loadings
![Loadings Heatmap](image/pca2.png)

Key Insights:
- **PC1**: Influenced by  `oldpeak` and `thal`, and reversely by `thalarch`.
- **PC2**: Dominated by `sex`, `thal`, and reversely by `chol`, `tresecg` and `age`
- **PC5/PC6**: High influence from `restecg`, `fbs`, and `slope`.

###  About PCA?
- It reveals correlated variable groups.
- Helps with decorrelation and reducing redundancy.
- and aids in faster model training and visualization.

---

## Summary

- **Class imbalance** exists.
- Features most associated with disease: `ca`, `thal`, `oldpeak`, `cp`, `exang`.
- PCA confirms structure and redundancy in the data.
- Visualizations guide feature selection and preprocessing before modeling.


# Missing Value Handling Strategies

Different techniques can be used to handle missing values depending on the missingness pattern and feature importance:

### 1. Deletion
- **Pros**: Simple; preserves data integrity.
- **Cons**: Reduces sample size, It can introduce bias if data is not missing completely at random (MCAR).

**Use when**: Missingness is minimal and truly random.

### 2. Simple Imputation
- **Mean / Median (Numeric)**: Replaces missing values with a central value.
- **Mode (Categorical)**: Fills in with the most frequent category.

**Use when**: Feature is important and missingness is low to moderate.

### 3. Advanced Statistical Methods
- **Multiple Imputation**: Accounts for uncertainty by creating multiple datasets.
- **Model-based Imputation**: Uses machine learning (e.g., Random Forests) to predict missing values.

**Use when**: Feature is predictive but missingness is moderate to high.

### 4. Missingness Indicator Features
- Adds a new binary column to indicate whether the value was missing.

**Use when**: Missingness itself could be informative (e.g., `thal`, `ca`).

Since missing values are only a few in just 2 of the features, opting for either deletion or simple imputation plus indicator should be enough. For this project, simple imputation strategies were chosen but the code is flexible for advances imputation metrics: KNN.