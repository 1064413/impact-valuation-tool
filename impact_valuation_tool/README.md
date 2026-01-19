# Financial Impact Tool for Lifestyle Coaches

A comprehensive Streamlit application for calculating and visualizing the potential healthcare cost savings from lifestyle coaching interventions.

## Project Structure

The application follows a modular architecture for better maintainability and scalability:

```
project_root/
├── app.py                          # Main application entry point
├── insurance_dataset.xlsx          # Healthcare cost data (required)
├── impact_tool_env.yml            # Conda environment file
├── README.md                        # This file
│
├── src/                           # Core business logic
│   ├── __init__.py
│   └── models.py                  # HealthcareCostModel & ImpactTool classes
│
└── utils/                         # Utility functions & components
    ├── __init__.py
    ├── data_loader.py            # Excel data loading & preprocessing
    ├── styling.py                # Streamlit styling & theme management
    └── components.py             # Streamlit UI components
```

## Module Overview

### `src/models.py`
Core business logic classes:
- **HealthcareCostModel**: Manages healthcare costs and maps conditions to healthcare services
- **ImpactTool**: Main calculation engine for financial impact analysis

### `utils/data_loader.py`
Data loading utilities:
- `load_data()`: Load data from Excel files
- `load_and_prepare_healthcare_data()`: Load, validate, and preprocess healthcare data

### `utils/styling.py`
UI styling and theme management:
- `get_theme_css()`: Returns CSS for light/dark themes
- `get_sticky_header_style()`: Returns theme-specific header styling

### `utils/components.py`
Reusable Streamlit UI components:
- `render_sidebar()`: Sidebar with information, methodology, and theme toggle
- `render_patient_input_section()`: Patient data input forms

## Running the Application

### Prerequisites
- Python 3.8+
- Conda (optional, for environment management)
- Excel file: `insurance_dataset.xlsx` with sheet named `niveau2`

### Setup

1. **Create and activate environment:**
```bash
conda env create -f impact_tool_env.yml
conda activate impact_tool_env
```

Or install dependencies manually:
```bash
pip install streamlit pandas plotly openpyxl
```

2. **Run the application:**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8502`

## Features

### Core Functionality
- **Patient Data Input**: Enter total patient count and distribution across health conditions
- **Cost Calculation**: Automatic calculation of healthcare costs based on 2024 Dutch healthcare data
- **Custom Costs**: Override default costs with your own estimates
- **Impact Assessment**: Track impact levels (Low, Medium, High, Critical) for each condition

### Health Conditions
Supports 20+ predefined health conditions organized by category:
- Mental Health and Stress Management
- Physical Wellbeing and Health
- Diet and Lifestyle Choices
- Sleep and Recovery
- Behavioral Change and Motivational Coaching

### Scenario Analysis
- **Prevalence Reduction**: Simulate cost savings from reducing patient prevalence (1-100%)
- **Visual Metrics**: Compare base vs. scenario costs
- **Detailed Breakdown**: See impact per condition

### User Experience
- **Light/Dark Theme Toggle**: Choose your preferred interface style
- **Responsive Design**: Works on desktop and tablet
- **Detailed Expandable Sections**: Organized information display

### Export & Reporting
- **CSV Export**: Download scenario results for spreadsheet analysis
- **Text Reports**: Generate comprehensive analysis summaries
- **Data Visualization**: Plotly charts for cost breakdown analysis

### Detailed Analysis
- **Healthcare Services Breakdown**: See which services contribute to condition costs
- **Condition Details**: View description, chance, and impact level per condition
- **Custom Conditions**: Add and track custom health conditions with manual costs

## Data Source

All healthcare costs are based on:
- **Year**: 2024
- **Source**: Dutch healthcare insurance data
- **Currency**: Euros (€)
- **Per Capita**: Annual costs per insured person

Includes comprehensive coverage:
- GP visits & consultations
- Specialist care
- Medications & pharmaceutical care
- Physical, occupational, and speech therapies
- Hospital care & procedures

## Key Changes (Latest Version)

### Refactoring
- ✅ Modularized codebase into separate concerns (models, utilities, components)
- ✅ Cleaned up main app.py file for better readability
- ✅ Moved UI components to `utils/components.py`
- ✅ Centralized styling and theme management

### New Features
- ✅ Improved patient chance slider (1-5 scale per condition)
- ✅ Added health conditions detail expanders
- ✅ Custom conditions support with full details display
- ✅ Enhanced scenario analysis with 1-100% reduction slider
- ✅ Detailed cost calculation breakdown showing all healthcare services
- ✅ Export functionality (CSV & TXT)

### UI Improvements
- ✅ Single-page application (removed multi-page navigation)
- ✅ Better organized input sections with collapsible categories
- ✅ Improved styling with light/dark theme support
- ✅ Responsive layout with proper spacing

## Usage Example

1. **Enter Patient Data**
   - Input total number of patients
   - Specify how many patients per condition
   - Set custom costs if desired

2. **Add Chance & Impact**
   - Set chance level (1-5) for each condition
   - Assign impact level (Low/Medium/High/Critical)
   - Add notes/descriptions

3. **Calculate Impact**
   - Click "Calculate Impact" button
   - View total healthcare costs
   - See detailed breakdown by condition

4. **Analyze Scenarios**
   - Set prevalence reduction percentage (1-100%)
   - Compare base vs. scenario costs
   - Identify potential savings

5. **Export Results**
   - Download CSV for spreadsheet analysis
   - Generate text report for documentation

## Technical Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas
- **Visualization**: Plotly
- **Data Source**: Excel (openpyxl)
- **Language**: Python 3.8+

## Notes

- All costs are estimates for informational purposes
- Results should be validated with healthcare professionals
- Data is based on 2024 Dutch healthcare system
- Session state persists during user interaction
- Light/Dark theme preference is preserved during session

## Troubleshooting

**Missing data file**
- Ensure `insurance_dataset.xlsx` is in the project root
- Verify the sheet name is `niveau2`

**Streamlit warnings**
- Deprecation warnings about `use_container_width` can be ignored
- Will be updated in future Streamlit versions

**Import errors**
- Ensure all packages are installed: `pip install -r requirements.txt`
- Check Python version is 3.8 or higher

## Future Enhancements

- [ ] Multi-language support
- [ ] Database integration for data storage
- [ ] Advanced statistical analysis
- [ ] Integration with healthcare systems
- [ ] Mobile app version
- [ ] API endpoint for integration

## License

© 2025 Financial Impact Tool
Developed for lifestyle coaches and healthcare professionals

## Support

For questions or issues, please contact your healthcare institution's implementation team.
