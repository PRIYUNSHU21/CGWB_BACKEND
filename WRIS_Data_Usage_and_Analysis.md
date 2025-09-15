# WRIS Data Usage and Analysis

## Overview
This document details the utilization of Water Resources Information System (WRIS) data in our groundwater evaluation system. WRIS, maintained by the Central Ground Water Board (CGWB) of India, provides comprehensive groundwater monitoring data across various districts. Our implementation processes this data locally using CSV files for efficient analysis, spatial interpolation via Inverse Distance Weighting (IDW), and trend analysis using polynomial regression.

## Data Storage and Employment

### WRIS Data Source
- **Source**: Central Ground Water Board (CGWB) WRIS portal
- **Data Types**: Historical groundwater levels, rainfall data, district-wise measurements
- **Coverage**: 23 districts in West Bengal, India
- **Time Period**: Multiple years of historical data

### CSV Storage Strategy
We employ WRIS data by storing it in local CSV files for the following reasons:
- **Offline Processing**: Eliminates dependency on external API calls, ensuring reliability
- **Performance**: Faster data access and manipulation using Pandas library
- **Version Control**: CSV files can be tracked in Git for data versioning
- **Flexibility**: Easy to update, filter, and preprocess data locally

**Files Used**:
- `groundwater_data.csv`: Contains historical groundwater levels with columns for district, year, month, water level (in meters)
- `rainfall_data.csv`: Contains rainfall data for 2024 with district-wise monthly measurements

**Data Structure**:
```csv
district,year,month,water_level
Kolkata,2023,January,5.2
Kolkata,2023,February,4.8
...
```

## Inverse Distance Weighting (IDW) Implementation

### Concept and Basis
IDW is a spatial interpolation method used to estimate values at unsampled locations based on measured values at nearby points. The fundamental assumption is that closer points have more influence on the interpolated value than distant points.

**Mathematical Basis**:
- **Spatial Similarity**: Assumes that groundwater levels are spatially correlated
- **Distance Decay**: Influence decreases with increasing distance
- **Local Variation**: Captures micro-scale variations in groundwater distribution

### IDW Formula
The IDW estimation for a point \( p \) is calculated as:

\[
\hat{z}(p) = \frac{\sum_{i=1}^{n} \frac{z_i}{d_i^p}}{\sum_{i=1}^{n} \frac{1}{d_i^p}}
\]

Where:
- \( \hat{z}(p) \): Estimated value at point \( p \)
- \( z_i \): Known value at point \( i \)
- \( d_i \): Euclidean distance from point \( p \) to point \( i \)
- \( p \): Power parameter (typically 2 for IDW²)
- \( n \): Number of neighboring points used

### Implementation Details
- **Power Parameter**: Set to 2 (IDW²) for balanced weighting
- **Distance Calculation**: Uses Haversine formula for geographic coordinates
- **Maximum Distance**: Limited to 5° (~500km) to ensure local relevance
- **Minimum Neighbors**: Requires at least 3 neighboring districts for estimation
- **Fallback**: Returns null if insufficient nearby data

### Citation Sources
- **Shepard, D. (1968)**: "A two-dimensional interpolation function for irregularly-spaced data." Proceedings of the 1968 ACM National Conference, pp. 517-524.
- **Lu, G.Y. and Wong, D.W. (2008)**: "An adaptive inverse-distance weighting spatial interpolation technique." Computers & Geosciences, 34(9), pp. 1044-1055.

## Trend Analysis Feature

### Overview
The trend analysis feature provides insights into groundwater level changes over time, including recharge/depletion rates, critical level detection, and future projections.

### Methodology
**Polynomial Regression with Regularization**:
- **Model Type**: Polynomial regression (degree 2-3) with Ridge regularization
- **Purpose**: Captures non-linear trends while preventing overfitting
- **Regularization**: L2 penalty (alpha=0.1) to stabilize coefficients

**Mathematical Formulation**:
For groundwater levels \( y \) over time \( t \):

\[
y = \beta_0 + \beta_1 t + \beta_2 t^2 + \beta_3 t^3 + \epsilon
\]

With Ridge regularization:

\[
\min_{\beta} \sum_{i=1}^{n} (y_i - X_i\beta)^2 + \alpha \sum_{j=1}^{p} \beta_j^2
\]

### Analysis Components

#### 1. Recharge/Depletion Rate Calculation
- **Method**: Derivative of the fitted polynomial at current date
- **Units**: Meters per year
- **Interpretation**: Positive = recharge, Negative = depletion

#### 2. Critical Level Detection
- **Threshold**: 5 meters below ground level (configurable)
- **Detection**: Compares current estimated level with critical threshold
- **Alert**: Flags districts approaching or below critical levels

#### 3. Historical Trend Projection
- **Projection**: Extends polynomial fit to future dates
- **Confidence**: Based on R² goodness-of-fit metric
- **Estimation Flag**: Indicates if projection uses estimated data

### Data Processing Pipeline
1. **Data Filtering**: Select district-specific historical data
2. **Missing Data Handling**: Use IDW for gaps in historical records
3. **Model Fitting**: Apply polynomial regression with cross-validation
4. **Validation**: Calculate R² and RMSE metrics
5. **Projection**: Generate future level estimates
6. **Rate Calculation**: Compute instantaneous rates from fitted curve

### Quality Metrics
- **R² Score**: Measures goodness-of-fit (0-1 scale)
- **RMSE**: Root Mean Square Error for prediction accuracy
- **Estimation Transparency**: Flags data points derived from IDW

### Integration with District Factors
- **Soil-Based Adjustment**: Multiplies rates by district-specific infiltration factors
- **Source**: Soil coefficient data from agricultural surveys
- **Impact**: Improves accuracy of recharge/depletion estimates

This comprehensive approach ensures reliable groundwater monitoring and forecasting for sustainable water resource management.