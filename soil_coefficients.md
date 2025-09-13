# Soil Coefficients for Infiltration Factor

This file documents scientifically-derived infiltration coefficients for groundwater recharge calculation, based on soil types in India. Coefficients are estimated from hydrological literature (e.g., USDA infiltration rates, CGWB reports) and adjusted for typical soil properties like texture, permeability, and moisture retention. Values range from 0.05 (low infiltration, e.g., clayey/saline soils) to 0.6 (high, e.g., sandy soils). These are hardcoded for prototyping; refine with local field data or APIs for accuracy.

- **Units**: Dimensionless (multiplier for rainfall to recharge).
- **Assumptions**: Based on average conditions; actual rates vary by depth, rainfall intensity, and land use.
- **Sources**: Derived from soil facts and standard infiltration curves (e.g., Alluvial: loamy, moderate; Black: clayey, low).

## Coefficient Table

| Sl.No | Soil Type      | Typical Coefficient | Range | Key Facts/States | Rationale |
|-------|----------------|---------------------|-------|------------------|-----------|
| 1     | Alluvial Soil | 0.35               | 0.25-0.4 | Rich in nutrients; Uttar Pradesh, Bihar, West Bengal, Punjab, Haryana | Loamy texture allows moderate infiltration; ideal for agriculture. |
| 2     | Black Soil    | 0.15               | 0.1-0.2  | Retains moisture; Maharashtra, Gujarat, Madhya Pradesh, Karnataka | Clayey (regur) soil has low permeability. |
| 3     | Red Soil      | 0.4                | 0.3-0.5  | Well-drained; Tamil Nadu, Karnataka, Andhra Pradesh, Odisha | Sandy, iron-rich; high infiltration but low fertility. |
| 4     | Laterite Soil | 0.25               | 0.2-0.4  | Weathered; Kerala, Karnataka, Maharashtra, Odisha | Variable due to iron/aluminum; moderate in humid areas. |
| 5     | Desert Soil   | 0.5                | 0.4-0.6  | Sandy; Rajasthan, Gujarat | High potential but reduced by aridity and low organic matter. |
| 6     | Mountain Soil | 0.25               | 0.2-0.3  | Thin/acidic; Uttarakhand, Himachal Pradesh, Arunachal Pradesh | Prone to erosion; moderate in hilly regions. |
| 7     | Peat Soil     | 0.12               | 0.1-0.2  | Organic-rich; West Bengal, Assam, Kerala | High water-holding but low infiltration due to saturation. |
| 8     | Saline Soil   | 0.08               | 0.05-0.15| High salt; Gujarat, Maharashtra, Tamil Nadu | Poor structure; unsuitable for most crops. |
| 9     | Alkaline Soil | 0.08               | 0.05-0.15| High pH; Rajasthan, Gujarat, Haryana | Limited nutrients; arid regions. |
| 10    | Forest Soil   | 0.4                | 0.3-0.5  | Humus-rich; Arunachal Pradesh, Assam, Meghalaya | Supports diverse life; good infiltration. |

## Usage in Code
- Map these to states/districts in `app/services/analysis_service.py` (e.g., update `SOIL_COEFFICIENT_MAP` with state-specific averages).
- Example: For Odisha (Red/Laterite), use 0.35 average.
- For districts, use soil type prevalence; fallback to state average.

Read more at: https://www.oneindia.com/major-types-of-soil-in-india-complete-list/