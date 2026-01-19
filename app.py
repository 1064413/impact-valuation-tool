"""
Financial Impact Tool for Lifestyle Coaches - Main Application

"""

import pandas as pd
import streamlit as st
import time
import plotly.express as px

from src.models import HealthcareCostModel, ImpactTool
from utils.data_loader import load_and_prepare_healthcare_data
from utils.styling import get_theme_css, get_sticky_header_style
from utils.components import render_sidebar, render_patient_input_section


def initialize_session_state():
    if 'total_patients' not in st.session_state:
        st.session_state.total_patients = 0
    if 'patients_per_condition' not in st.session_state:
        st.session_state.patients_per_condition = {}
    if 'results_calculated' not in st.session_state:
        st.session_state.results_calculated = False
    if 'results_df' not in st.session_state:
        st.session_state.results_df = None
    if 'total_cost' not in st.session_state:
        st.session_state.total_cost = 0.0
    if 'scenario_results_df' not in st.session_state:
        st.session_state.scenario_results_df = None
    if 'scenario_total_cost' not in st.session_state:
        st.session_state.scenario_total_cost = 0.0
    if 'scenario_savings' not in st.session_state:
        st.session_state.scenario_savings = 0.0
    if 'scenario_pct' not in st.session_state:
        st.session_state.scenario_pct = 1
    if 'calculated_total_patients' not in st.session_state:
        st.session_state.calculated_total_patients = 0
    if 'calculated_entered_patients' not in st.session_state:
        st.session_state.calculated_entered_patients = 0
    if 'custom_conditions' not in st.session_state:
        st.session_state.custom_conditions = []
    if 'condition_details' not in st.session_state:
        st.session_state.condition_details = {}
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'


def configure_page():
    st.set_page_config(
        page_title="Financial Impact Tool for Lifestyle Coaches",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'About': "Financial Impact Tool - Calculate healthcare cost savings from lifestyle coaching interventions."
        }
    )


def apply_styles():
    theme_css = get_theme_css(st.session_state.theme)
    
    st.markdown(f"""
    <style>
    html, body {{
        scroll-behavior: smooth;
    }}
    
    {theme_css}
    
    /* Sticky header container */
    .sticky-header {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 999;
        padding: 0.5rem 1rem;
        text-align: center;
        font-size: 1.2rem;
        font-weight: 700;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        opacity: 0;
        transform: translateY(-100%);
        transition: all 0.3s ease;
        pointer-events: none;
    }}
    
    .sticky-header.visible {{
        opacity: 1;
        transform: translateY(0);
        pointer-events: auto;
    }}
    
    /* Header styling */
    .main-header {{
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        margin: 2rem 0 1.5rem 0;
        letter-spacing: -0.5px;
    }}
    
    .sub-header {{
        font-size: 1.6rem;
        font-weight: 700;
        margin-top: 2.5rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
    }}
    
    /* Metric card - improved */
    .metric-card {{
        padding: 1.5rem;
        border-radius: 12px;
        margin: 0.75rem 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}
    
    .metric-card:hover {{
        transform: translateY(-2px);
    }}
    
    /* Result highlight */
    .result-highlight {{
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
    }}
    
    /* Chart container */
    .chart-container {{
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
    }}
    
    /* Debug/service styling */
    .debug-condition {{
        padding: 1rem;
        margin: 0.75rem 0;
        border-radius: 8px;
    }}
    
    .debug-service-success {{
        color: #4caf50;
        font-weight: 600;
    }}
    
    .debug-service-error {{
        color: #f44336;
        font-weight: 600;
    }}
    
    .debug-service-warning {{
        color: #ff9800;
        font-weight: 600;
    }}
    
    /* Button styling */
    .stButton > button {{
        border: none;
        padding: 0.6rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
    }}
    
    /* Input styling */
    .stNumberInput input, .stTextInput input {{
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }}
    
    .stNumberInput input:focus, .stTextInput input:focus {{
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }}
    
    /* Expander styling */
    .streamlit-expanderHeader {{
        background-color: #f8f9ff;
        border-radius: 8px;
    }}
    
    .streamlit-expanderHeader:hover {{
        background-color: #f0f2ff;
    }}
    
    /* Footer styling */
    .footer {{
        text-align: center;
        padding: 2rem;
        color: #666;
        border-top: 2px solid #e0e0e0;
        margin-top: 2rem;
    }}
    
    /* Dataframe styling */
    .stDataFrame {{
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    }}
    
    /* Smooth scrolling */
    .stApp {{
        scroll-behavior: smooth !important;
    }}
    
    /* Info box styling */
    .stAlert {{
        border-radius: 8px;
        border-left: 4px solid;
    }}
    </style>
    """, unsafe_allow_html=True)


def render_header():
    sticky_bg, sticky_color = get_sticky_header_style(st.session_state.theme)
    
    st.markdown(f"""
    <div class="sticky-header" id="stickyHeader" style="{sticky_bg} {sticky_color}">
        💰 Financial Impact Tool for Lifestyle Coaches
    </div>
    <script>
        window.addEventListener('scroll', function() {{
            var header = document.getElementById('stickyHeader');
            if (window.pageYOffset > 300) {{
                header.classList.add('visible');
            }} else {{
                header.classList.remove('visible');
            }}
        }});
    </script>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-header">💰 Financial Impact Tool for Lifestyle Coaches</div>', unsafe_allow_html=True)

    if st.session_state.theme == 'light':
        welcome_bg = "background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);"
        welcome_border = "border-left: 5px solid #667eea;"
        welcome_title_color = "color: #667eea;"
        welcome_text_color = "color: #333;"
        welcome_caption_color = "color: #666;"
    else:
        welcome_bg = "background: linear-gradient(135deg, #252b42 0%, #1e2235 100%);"
        welcome_border = "border-left: 5px solid #00d4ff;"
        welcome_title_color = "color: #00d4ff;"
        welcome_text_color = "color: #e0e0e0;"
        welcome_caption_color = "color: #b0b0b0;"
    
    st.markdown(f"""
    <div style="{welcome_bg} padding: 2rem; border-radius: 12px; {welcome_border} margin-bottom: 2rem;">
        <h3 style="{welcome_title_color} margin-top: 0;">Welcome! 👋</h3>
        <p style="font-size: 1.05rem; line-height: 1.6; {welcome_text_color}">
        This interactive tool helps <strong>lifestyle coaches</strong> quantify the potential <strong>societal healthcare cost savings</strong> from their interventions. 
        By inputting your patient data, you can estimate the costs the healthcare system might incur if patients required full treatment for their conditions.
        </p>
        <p style="font-size: 1.05rem; line-height: 1.6; {welcome_text_color}">
        <strong>📊 Quick Start:</strong><br>
        1️⃣ Specify how many patients you treat for each health condition<br>
        2️⃣ Add any custom conditions if needed<br>
        3️⃣ Click <strong>"Calculate Impact"</strong> to see detailed cost breakdowns<br>
        4️⃣ Explore scenarios to estimate savings from prevalence reduction
        </p>
        <p style="font-size: 0.95rem; {welcome_caption_color} margin-bottom: 0;"><em>💡<strong>Disclaimer:</strong> if no costs are entered, the default costs will be used*. All calculations are based on <a href="https://www.zorgcijfersdatabank.nl/" target="_blank">2024 Dutch healthcare cost data</a></p></em>
        <p style="font-size: 0.75rem; {welcome_caption_color} margin-bottom: 0;"><em>*Calculations of costs per condition are estimated and should be used for informational purposes only.
    </div>
    """, unsafe_allow_html=True)


def render_reset_button():
    col_reset, col_spacer = st.columns([1, 4])
    with col_reset:
        if st.button(" Reset All", help="Clear all inputs and start fresh"):
            st.session_state.total_patients = 0
            st.session_state.patients_per_condition = {}
            st.session_state.results_calculated = False
            st.session_state.results_df = None
            st.session_state.total_cost = 0.0
            st.session_state.scenario_results_df = None
            st.session_state.scenario_total_cost = 0.0
            st.session_state.scenario_savings = 0.0
            st.session_state.scenario_pct = 1
            st.session_state.calculated_total_patients = 0
            st.session_state.calculated_entered_patients = 0
            st.session_state.last_calculation_time = 0
            st.session_state.custom_conditions = []
            st.rerun()


def render_footer():
    st.markdown("""
    <div class="footer">
    <p> Developed with ❤️ for lifestyle coaches | Data based on 2024 healthcare costs</p>
    <p><em>Results are estimated and should be used for informational purposes only.</em></p>
    </div>
    """, unsafe_allow_html=True)


def main():
    initialize_session_state()
    configure_page()
    apply_styles()
    
    # Sidebar
    render_sidebar(st.session_state)
    
    # Header
    render_header()
    render_reset_button()
    
    # Load data
    try:
        master_costs_df = load_and_prepare_healthcare_data('insurance_dataset.xlsx')
        cost_model = HealthcareCostModel(master_costs_df)
        impact_tool = ImpactTool(cost_model)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

    # Patient Input Section
    total_patients, patients_per_condition, total_entered_patients = render_patient_input_section(
        impact_tool, st.session_state
    )

    # Custom conditions section
    st.markdown('<div class="sub-header"> Other health conditions (manual)</div>', unsafe_allow_html=True)
    with st.expander(" Other health conditions", expanded=False):
        if st.button(" Add custom condition", key="add_custom_condition"):
            st.session_state.custom_conditions.append({
                "name": "", 
                "description": "", 
                "patients": 0, 
                "cost": 0.0
            })

        for idx, cond in enumerate(list(st.session_state.custom_conditions)):
            st.markdown(f"**Custom Condition {idx + 1}**")
            
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input(
                    "Condition name",
                    value=cond.get("name", ""),
                    key=f"custom_name_{idx}",
                    help="Fill in the name of the condition (e.g. Addiction, Anxiety, etc.)"
                )
            with col2:
                patients_val = int(cond.get("patients", 0)) if cond.get("patients") is not None else 0
                patients = st.number_input(
                    "Number of patients",
                    min_value=0,
                    step=1,
                    value=patients_val,
                    key=f"custom_patients_{idx}",
                    help="Amount of patients with this condition"
                )
            
            description = st.text_area(
                "Description",
                value=cond.get("description", ""),
                key=f"custom_desc_{idx}",
                height=100,
                help="Description on the condition and/or what your organization does to make an impact on the patients with the condition"
            )
            
            col3, col_spacer = st.columns([1, 1])
            with col3:
                cost_val = float(cond.get("cost", 0.0)) if cond.get("cost") is not None else 0.0
                cost = st.number_input(
                    "Cost per patient (€)",
                    min_value=0.0,
                    step=10.0,
                    value=cost_val,
                    key=f"custom_cost_{idx}",
                    help="Yearly health insurance costs per patient (estimated in euros)"
                )
            
            if st.button(" Remove this condition", key=f"custom_remove_{idx}"):
                st.session_state.custom_conditions.pop(idx)
                st.rerun()

            st.session_state.custom_conditions[idx] = {
                "name": name.strip(), 
                "description": description.strip(),
                "patients": patients, 
                "cost": cost
            }
            
            st.markdown("---")

    # Include custom conditions in total
    for cond in st.session_state.custom_conditions:
        try:
            total_entered_patients += int(cond.get("patients", 0))
        except Exception:
            pass

    # Calculate button
    if st.button(" Calculate Impact", type="primary", disabled=total_entered_patients == 0):
        if 'last_calculation_time' not in st.session_state:
            st.session_state.last_calculation_time = 0
        
        current_time = time.time()
        if current_time - st.session_state.last_calculation_time > 0.5:
            st.session_state.last_calculation_time = current_time
            
            with st.spinner("Calculating impact..."):
                time.sleep(0.5)
                
                impact_tool.total_patients_coach = total_patients
                impact_tool.patients_per_condition = patients_per_condition

                custom_costs = {}
                for condition, details in st.session_state.condition_details.items():
                    if details.get("custom_cost") is not None:
                        custom_costs[condition] = details["custom_cost"]

                impact_tool.calculate_impact(custom_costs=custom_costs)

                custom_rows = []
                for cond in st.session_state.custom_conditions:
                    name = cond.get("name", "").strip()
                    try:
                        patients_custom = int(cond.get("patients", 0))
                        cost_custom = float(cond.get("cost", 0.0))
                    except Exception:
                        continue
                    if name and patients_custom > 0 and cost_custom > 0:
                        custom_rows.append({
                            'Condition': name,
                            'Patient_Count': patients_custom,
                            'Costs per patient': cost_custom,
                            'Total societal costs': patients_custom * cost_custom
                        })
                
                results_df = impact_tool.results_df
                total_cost = impact_tool.total_societal_cost

                if custom_rows:
                    custom_df = pd.DataFrame(custom_rows)
                    if results_df is None:
                        results_df = custom_df
                    else:
                        results_df = pd.concat([results_df, custom_df], ignore_index=True)
                    total_cost += sum(row['Total societal costs'] for row in custom_rows)

                st.session_state.results_calculated = True
                st.session_state.results_df = results_df
                st.session_state.total_cost = total_cost
                st.session_state.scenario_results_df = None
                st.session_state.scenario_total_cost = 0.0
                st.session_state.scenario_savings = 0.0
                st.session_state.scenario_pct = 1
                st.session_state.calculated_total_patients = total_entered_patients
                st.session_state.calculated_entered_patients = total_entered_patients

    # Display results
    if st.session_state.results_calculated and st.session_state.results_df is not None:
        st.markdown('<div class="sub-header"> FINANCIAL IMPACT ANALYSIS - RESULTS</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h3> Total patients entered</h3>
            <h2 style="color: #1f77b4;">{st.session_state.calculated_entered_patients}</h2>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(f"""
        <div class="result-highlight">
            <h2> Total Potential Annual Societal Healthcare Costs</h2>
            <h1 style="color: #2ca02c; font-size: 2.5rem;">€ {st.session_state.total_cost:,.2f}</h1>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        st.info(" This amount represents the estimated costs the healthcare system would incur if these patients required the (estimated) full scope of treatment associated with their condition.")

        st.subheader(" Detailed Overview by Condition")
        st.markdown("**How the costs are calculated:** For each health condition, the total cost is the number of patients * cost per patient. Costs are based on 2024 Dutch healthcare data.")
        
        display_df = st.session_state.results_df.copy()
        display_df['Costs per patient'] = display_df['Costs per patient'].apply(lambda x: f"€ {x:,.2f}")
        display_df['Total societal costs'] = display_df['Total societal costs'].apply(lambda x: f"€ {x:,.2f}")
        display_df = display_df.rename(columns={
            'Condition': ' Health Condition',
            'Patient_Count': ' Patients',
            'Costs per patient': ' Cost per Patient',
            'Total societal costs': ' Total Societal Cost'
        })
        
        st.dataframe(
            display_df,
            use_container_width=True,
            column_config={
                " Health Condition": st.column_config.TextColumn("Health Condition", width="medium"),
                " Patients": st.column_config.NumberColumn("Patients", format="%d"),
                " Cost per Patient": st.column_config.TextColumn("Cost per Patient", width="medium"),
                " Total Societal Cost": st.column_config.TextColumn("Total Societal Cost", width="medium")
            }
        )

        # Stippengrafiek: x = patiënten per aandoening, y = totale kosten (verfraaid)
        try:
            chart_df = st.session_state.results_df.copy()
            chart_df = chart_df.rename(columns={'Patient_Count': 'Patient count','Total societal costs': 'Total healthcare costs'})
            chart_df = chart_df[(chart_df['Patient count'] > 0) & (chart_df['Total healthcare costs'] > 0)]
            if not chart_df.empty:
                st.markdown("---")
                st.subheader(" Scatterplot: Amount of patients vs. Amount of costs per condition")
                st.caption("X-axis: amount of patients • Y-axis: total health insurance costs")

                num_conditions = len(chart_df)
                total_entered = st.session_state.calculated_entered_patients or int(chart_df['Patient count'].sum())
                avg_patients = total_entered / num_conditions if num_conditions > 0 else 0

                # Instellingen voor referentielijn (verticale lijn: patiënten)
                col_ref1, col_ref2, col_ref3, col_ref4 = st.columns([1, 1, 1, 1])
                with col_ref1:
                    ref_type = st.selectbox(
                        "Reference line",
                        ["None", "Average", "Median"],
                        index=0,
                        help="Vertical reference line on the x-axis: None = no line; Average = total patients / amount of conditions; Median = median patients."
                    )
                with col_ref2:
                    line_style = st.selectbox(
                        "Line style",
                        ["dash", "solid", "dot"],
                        index=0,
                        help="Style of the vertical reference line: dash, solid or dot."
                    )
                with col_ref3:
                    line_width = st.slider(
                        "Line width",
                        min_value=1,
                        max_value=6,
                        value=2,
                        help="Width of the vertical reference line."
                    )
                with col_ref4:
                    line_color = st.color_picker(
                        "Line color",
                        value="#ff4d4f",
                        help="Color of the vertical reference line."
                    )

                # Instellingen voor horizontale kostenlijn
                col_href1, col_href2, col_href3, col_href4 = st.columns([1, 1, 1, 1])
                with col_href1:
                    ref_type_y = st.selectbox(
                        "Costs line",
                        ["None", "Average", "Median"],
                        index=0,
                        help="Horizontal reference line on the y-axis: None = no line; Average = average of the total costs; Median = median total costs (in €)."
                    )
                with col_href2:
                    line_style_y = st.selectbox(
                        "Line style (costs)",
                        ["dash", "solid", "dot"],
                        index=0,
                        help="Style of the horizontal costs line: dashed, solid or dotted."
                    )
                with col_href3:
                    line_width_y = st.slider(
                        "Line width (costs)",
                        min_value=1,
                        max_value=6,
                        value=2,
                        help="Width of the horizontal costs line."
                    )
                with col_href4:
                    line_color_y = st.color_picker(
                        "Line color (costs)",
                        value="#5c6bc0",
                        help="Color of the horizontal costs line."
                    )

                # Voorbereiding referentiewaarden en uitlegtekst
                ref_value = None
                if ref_type != "None":
                    ref_value = avg_patients if ref_type == "Average" else float(chart_df['Patient count'].median())

                ref_value_y = None
                label_y = None
                if ref_type_y != "Geen":
                    if ref_type_y == "Average":
                        ref_value_y = float(chart_df['Total healthcare costs'].mean())
                        label_y = f"Average costs: € {ref_value_y:,.0f}"
                    else:
                        ref_value_y = float(chart_df['Total healthcare costs'].median())
                        label_y = f"Median costs: € {ref_value_y:,.0f}"

                if ref_value is not None or ref_value_y is not None:
                    uitleg_parts = []
                    if ref_value is not None:
                        uitleg_parts.append(f"The vertical line shows the {ref_type.lower()} of patiens (≈ {ref_value:.1f}).")
                    if ref_value_y is not None:
                        uitleg_parts.append(f"The horizontal line shows the {ref_type_y.lower()} of total costs (≈ € {ref_value_y:,.0f}).")
                    st.info(" ".join(uitleg_parts))
                else:
                    st.caption("Tip: Use the options above to use reference lines.")

                is_dark = st.session_state.theme == 'dark'
                grid_color = 'rgba(255,255,255,0.15)' if is_dark else 'rgba(0,0,0,0.1)'
                outline_color = '#ffffff' if is_dark else 'rgba(0,0,0,0.35)'

                fig_scatter = px.scatter(
                    chart_df,
                    x='Patient count',
                    y='Total healthcare costs',
                    hover_name='Condition',
                    hover_data={'Costs per patient': True, 'Total healthcare costs': True, 'Patient count': True},
                    color='Total healthcare costs',
                    color_continuous_scale='Viridis',
                    size='Patient count',
                    size_max=30,
                    labels={'Patient count': 'Patients', 'Total healthcare costs': 'Costs (€)', 'Condition': 'Condition'},
                    title='Amount of patients per condition vs. total costs per condition'
                )
                fig_scatter.update_traces(
                    marker=dict(opacity=0.9, line=dict(width=1, color=outline_color)),
                    selector=dict(mode='markers')
                )
                # Bereken en teken referentielijn (x) indien gewenst
                if ref_value is not None:
                    dash_map = {"dash": "dash", "solid": "solid", "dot": "dot"}
                    fig_scatter.add_vline(x=ref_value, line_dash=dash_map[line_style], line_color=line_color, line_width=line_width)
                    fig_scatter.add_annotation(
                        x=ref_value,
                        y=float(chart_df['Total healthcare costs'].max()),
                        text=f"{ref_type}: {ref_value:.1f}",
                        showarrow=False,
                        yshift=10,
                        font=dict(color=line_color)
                    )

                # Bereken en teken horizontale kostenlijn (y) indien gewenst
                if ref_value_y is not None:
                    dash_map_y = {"dash": "dash", "solid": "solid", "dot": "dot"}
                    fig_scatter.add_hline(y=ref_value_y, line_dash=dash_map_y[line_style_y], line_color=line_color_y, line_width=line_width_y)
                    fig_scatter.add_annotation(
                        x=float(chart_df['Patient count'].max()),
                        y=ref_value_y,
                        text=label_y,
                        showarrow=False,
                        xshift=10,
                        font=dict(color=line_color_y)
                    )
                # Top-5 labels (op bedrag)
                top5 = chart_df.nlargest(5, 'Total healthcare costs')
                for _, r in top5.iterrows():
                    fig_scatter.add_annotation(
                        x=float(r['Patient count']),
                        y=float(r['Total healthcare costs']),
                        text=str(r['Condition']),
                        showarrow=False,
                        yshift=8,
                        font=dict(size=11)
                    )
                fig_scatter.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=10, r=10, t=60, b=10),
                    coloraxis_colorbar=dict(title='Total costs')
                )
                fig_scatter.update_xaxes(
                    title_text='Patients per condition',
                    gridcolor=grid_color,
                    zeroline=False,
                    tickmode='auto'
                )
                fig_scatter.update_yaxes(
                    title_text='Total costs (€)',
                    gridcolor=grid_color,
                    zeroline=False,
                    tickprefix='€ ',
                    separatethousands=True
                )
                st.plotly_chart(fig_scatter, use_container_width=True)
        except Exception as e:
            st.warning(f"Couldn't generate scatterplot: {e}")

        # Health Conditions Details section
        conditions_with_details = {
            cond: details
            for cond, details in st.session_state.condition_details.items()
            if details.get("description") or details.get("custom_cost") is not None
        }
        
        if conditions_with_details:
            result_conditions = st.session_state.results_df['Condition'].tolist() if st.session_state.results_df is not None else []
            display_conditions = {cond: details for cond, details in conditions_with_details.items() if cond in result_conditions}
            
            if display_conditions:
                st.markdown("---")
                st.subheader(" Health Conditions Details")
                
                for condition, details in display_conditions.items():
                    cond_row = st.session_state.results_df[st.session_state.results_df['Condition'] == condition]
                    if not cond_row.empty:
                        patients = cond_row.iloc[0]['Patient count']
                        cost_per_patient = cond_row.iloc[0]['Costs per patient']
                        
                        with st.expander(f"{condition}", expanded=False):
                            st.markdown(f"**Number of Patients:** {patients}")

                            if details.get("custom_cost") is not None:
                                default_cost = details.get("default_cost", 0)
                                st.markdown(f"**Cost per Patient:** € {cost_per_patient:,.2f} ✏️ **(Custom)**")
                                st.markdown(f"*Default was: € {default_cost:,.2f}*")
                            else:
                                st.markdown(f"**Cost per Patient:** € {cost_per_patient:,.2f}")

                            st.markdown(f"**Total Cost:** € {patients * cost_per_patient:,.2f}")

                            if details.get('description'):
                                st.markdown("**Description:**")
                                st.info(details.get('description'))

        # Custom Conditions Details section
        if st.session_state.custom_conditions:
            custom_with_data = [c for c in st.session_state.custom_conditions if c.get("name") and c.get("patients", 0) > 0]
            if custom_with_data:
                st.markdown("---")
                st.subheader(" Custom Conditions Details")
                
                for idx, cond in enumerate(custom_with_data):
                    with st.expander(f"{cond.get('name', 'Unnamed Condition')}", expanded=False):
                        st.markdown(f"**Number of Patients:** {cond.get('patients', 0)}")
                        st.markdown(f"**Cost per Patient:** € {cond.get('cost', 0):,.2f}")
                        st.markdown(f"**Total Cost:** € {cond.get('patients', 0) * cond.get('cost', 0):,.2f}")
                        if cond.get('description'):
                            st.markdown("**Description:**")
                            st.info(cond.get('description'))

        # Detailed Cost Calculation section
        if impact_tool.debug_info:
            with st.expander(" Detailed Cost Calculation - Healthcare Services Breakdown", expanded=False):
                st.markdown("**How each condition's cost is calculated:**")
                st.markdown("Each health condition is mapped to relevant healthcare services from 2024 Dutch healthcare data. The cost per patient is the sum of all these service costs.")

                for debug_info in impact_tool.debug_info:
                    if "Debug for" in debug_info:
                        debug_prefix = "Debug for "
                        start_idx = len(debug_prefix)
                        colon_idx = debug_info.find(":", start_idx)
                        condition_name = debug_info[start_idx:colon_idx].strip()
                        
                        st.markdown(f"### **{condition_name}**")

                        services_part = debug_info[colon_idx + 1:].strip()
                        
                        service_data = []
                        total_cost = 0.0
                        parts = services_part.split()
                        
                        i = 0
                        while i < len(parts):
                            if ":" in parts[i]:
                                service_part = parts[i]
                                
                                if service_part == "Total:":
                                    if i + 1 < len(parts):
                                        try:
                                            total_cost = float(parts[i + 1])
                                        except:
                                            total_cost = 0.0
                                    break
                                
                                service_name = service_part[:-1]
                                value_start = i + 1
                                
                                if value_start < len(parts):
                                    next_part = parts[value_start]
                                    
                                    if next_part == "NOT" and value_start + 1 < len(parts) and parts[value_start + 1] == "FOUND":
                                        service_data.append({
                                            "Service": service_name,
                                            "Cost": "Not Found",
                                            "Status": "error",
                                            "Icon": "❌"
                                        })
                                        i = value_start + 2
                                        continue
                                    
                                    elif next_part == "ERROR":
                                        error_parts = []
                                        j = value_start + 1
                                        while j < len(parts) and not parts[j].endswith(":"):
                                            error_parts.append(parts[j])
                                            j += 1
                                        error_msg = " ".join(error_parts)
                                        service_data.append({
                                            "Service": service_name,
                                            "Cost": f"Error: {error_msg}",
                                            "Status": "error",
                                            "Icon": "⚠️"
                                        })
                                        i = j
                                        continue
                                    
                                    else:
                                        try:
                                            cost_value = float(next_part)
                                            service_data.append({
                                                "Service": service_name,
                                                "Cost": f"€ {cost_value:,.2f}",
                                                "Status": "success",
                                                "Icon": "✅"
                                            })
                                            i = value_start + 1
                                            continue
                                        except ValueError:
                                            pass
                            
                            potential_service = []
                            j = i
                            while j < len(parts) and ":" not in parts[j]:
                                potential_service.append(parts[j])
                                j += 1
                            
                            if j < len(parts) and ":" in parts[j]:
                                service_name = " ".join(potential_service) + " " + parts[j][:-1]
                                
                                value_idx = j + 1
                                if value_idx < len(parts):
                                    value = parts[value_idx]
                                    
                                    if value == "NOT" and value_idx + 1 < len(parts) and parts[value_idx + 1] == "FOUND":
                                        service_data.append({
                                            "Service": service_name,
                                            "Cost": "Not Found",
                                            "Status": "error",
                                            "Icon": "❌"
                                        })
                                        i = value_idx + 2
                                    elif value == "ERROR":
                                        error_parts = []
                                        k = value_idx + 1
                                        while k < len(parts) and not (":" in parts[k] or parts[k] == "Total:"):
                                            error_parts.append(parts[k])
                                            k += 1
                                        error_msg = " ".join(error_parts)
                                        service_data.append({
                                            "Service": service_name,
                                            "Cost": f"Error: {error_msg}",
                                            "Status": "error",
                                            "Icon": "⚠️"
                                        })
                                        i = k
                                    else:
                                        try:
                                            cost_value = float(value)
                                            service_data.append({
                                                "Service": service_name,
                                                "Cost": f"€ {cost_value:,.2f}",
                                                "Status": "success",
                                                "Icon": "✅"
                                            })
                                            i = value_idx + 1
                                        except:
                                            service_data.append({
                                                "Service": service_name,
                                                "Cost": value,
                                                "Status": "warning",
                                                "Icon": "⚠️"
                                            })
                                            i = value_idx + 1
                                else:
                                    i = j + 1
                            else:
                                i += 1

                        if service_data:
                            st.markdown(f"**Healthcare Services (Total: € {total_cost:,.2f})**")
                            for service in service_data:
                                css_class = f"debug-service-{service['Status']}"
                                st.markdown(f'<span class="{css_class}">{service["Icon"]} {service["Service"]}: {service["Cost"]}</span>', unsafe_allow_html=True)
                        
                        st.markdown("---")
                        if total_cost > 0:
                            st.markdown(f"**Total Annual Cost per Patient: € {total_cost:,.2f}**")
                        else:
                            st.markdown("**No valid costs found for this condition**")

        # Scenario section

        with st.expander("Reduction in prevalence", expanded=True):
            st.markdown("""
            This scenario calculates the financial impact of reducing the amount of patients with conditions.
            Select the probability (reduction percentage) for which you want to examine the effect on healthcare costs.
            """)
            scenario_pct = st.number_input(
                "Select the reduction percentage",
                min_value=1,
                max_value=100,
                value=10,
                step=1,
                help="Enter a percentage between 1–100: how many fewer patients would have this condition due to prevention or lifestyle coaching."
            )

            st.info(
                "📌 **How is the reduction calculated?**\n\n"
                "The scenario costs are based on:\n"
                "- **Amount of patients:** Current amount * (100% - reduction percentage)\n"
                "- **Costs per patient:** Stays the same\n"
                "- **Scenario costs:** Reduced amount of patients * costs per patient\n"
                "- **Cost savings:** Original costs − scenario costs"
            )

            base_df = st.session_state.results_df.copy()
            
            if 'Costs per patient' in base_df.columns:
                scenario_df = base_df.copy()
                scenario_df = scenario_df.rename(columns={'Patient_Count': 'Patient count', 'Total societal costs': 'Total healthcare costs'})
                scenario_df['Reduced patients'] = (scenario_df['Patient count'] * (1 - scenario_pct / 100)).round().astype(int)
                scenario_df['Reduced patients'] = scenario_df['Reduced patients'].clip(lower=0)
                scenario_df['Scenario costs'] = scenario_df['Reduced patients'] * scenario_df['Costs per patient']
                scenario_df['Savings vs base'] = scenario_df['Total healthcare costs'] - scenario_df['Scenario costs']

                st.session_state.scenario_results_df = scenario_df
                st.session_state.scenario_total_cost = scenario_df['Scenario costs'].sum()
                st.session_state.scenario_savings = scenario_df['Savings vs base'].sum()
                st.session_state.scenario_pct = scenario_pct

                st.markdown(f"**Scenario applied: {st.session_state.scenario_pct}% reduction in prevalence**")

                scen_display = st.session_state.scenario_results_df.copy()
                scen_display['Costs per patient'] = scen_display['Costs per patient'].apply(lambda x: f"€ {x:,.2f}")
                scen_display['Total healthcare costs'] = scen_display['Total healthcare costs'].apply(lambda x: f"€ {x:,.2f}")
                scen_display['Scenario costs'] = scen_display['Scenario costs'].apply(lambda x: f"€ {x:,.2f}")
                scen_display['Savings vs base'] = scen_display['Savings vs base'].apply(lambda x: f"€ {x:,.2f}")
                
                st.markdown("---")
                st.markdown("**Summary of scenario**")
                col_base, col_scenario, col_savings = st.columns(3)
                with col_base:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>💰 Base</h3>
                        <h2 style="color: #1f77b4;">€ {st.session_state.total_cost:,.2f}</h2>
                        <p style="font-size: 0.85em; color: #666;">Current situation</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col_scenario:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>📊 Reduction ({st.session_state.scenario_pct}%)</h3>
                        <h2 style="color: #2ca02c;">€ {st.session_state.scenario_total_cost:,.2f}</h2>
                        <p style="font-size: 0.85em; color: #666;">With reduction</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col_savings:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>✅ Cost savings</h3>
                        <h2 style="color: #ff7f0e;">€ {st.session_state.scenario_savings:,.2f}</h2>
                        <p style="font-size: 0.85em; color: #666;">Annual benefit</p>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("---")
                st.markdown("**Detailed scenario table**")
                st.dataframe(
                    scen_display,
                    use_container_width=True,
                )
                
                with st.expander("Cost Breakdown + " \
                "" \
                "visualization", expanded=False):
                    chart_df = st.session_state.results_df.copy()
                    chart_df = chart_df.rename(columns={'Total societal costs': 'Total healthcare costs'})
                    chart_df = chart_df[chart_df['Total healthcare costs'] > 0]
                    
                    if not chart_df.empty:
                        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                        try:
                            fig = px.bar(chart_df, x='Condition', y='Total healthcare costs', 
                                       title='Healthcare Costs by Condition',
                                       labels={'Total healthcare costs': 'Cost (€)', 'Condition': 'Health Condition'},
                                       color='Total healthcare costs',
                                       color_continuous_scale='Blues')
                            fig.update_layout(xaxis_tickangle=-45, 
                                            plot_bgcolor='rgba(0,0,0,0)',
                                            paper_bgcolor='rgba(0,0,0,0)')
                            st.plotly_chart(fig, use_container_width=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                        except Exception as e:
                            st.error(f"❌ Error creating chart: {e}")
            else:
                st.error("Required column 'Costs per patient' not found in results.")

        # Export scenario results & report
        st.markdown("---")
        st.subheader(" Export Scenario & Generate Report")
        col_export_csv, col_report = st.columns([1, 1])
        
        with col_export_csv:
            if st.session_state.scenario_results_df is not None:
                scenario_csv = st.session_state.scenario_results_df.to_csv(index=False)
                st.download_button(
                    label=" Download Scenario Results (CSV)",
                    data=scenario_csv,
                    file_name="scenario_results.csv",
                    mime="text/csv",
                    help="Download the scenario table with base and scenario costs.",
                    use_container_width=True
                )
        
        with col_report:
            if st.button(" Generate Report (TXT)", use_container_width=True, help="Create a text summary of base and scenario analysis"):
                if st.session_state.scenario_results_df is not None:
                    report_text = f"""
FINANCIAL IMPACT ANALYSIS REPORT
{'='*60}
Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

BASE CALCULATION
{'='*60}
Total patients entered: {st.session_state.calculated_entered_patients}
Total Annual Societal Healthcare Costs: € {st.session_state.total_cost:,.2f}

SCENARIO ANALYSIS: Prevalence Reduction
{'='*60}
Reduction percentage: {st.session_state.scenario_pct}%

Cost Summary:
  Base Costs (Current Situation):     € {st.session_state.total_cost:,.2f}
  Scenario Costs (With Reduction):    € {st.session_state.scenario_total_cost:,.2f}
  Annual Savings from Reduction:      € {st.session_state.scenario_savings:,.2f}

DETAILED BREAKDOWN BY CONDITION
{'='*60}
"""
                    for idx, row in st.session_state.scenario_results_df.iterrows():
                        report_text += f"\n{row['Condition']}\n"
                        report_text += f"  Patients (base):        {row['Patient count']}\n"
                        report_text += f"  Patients (scenario):    {row['Reduced patients']}\n"
                        report_text += f"  Cost per patient:       € {row['Costs per patient']:,.2f}\n"
                        report_text += f"  Total cost (base):      € {row['Total healthcare costs']:,.2f}\n"
                        report_text += f"  Scenario cost:          € {row['Scenario costs']:,.2f}\n"
                        report_text += f"  Savings for this condition: € {row['Savings vs base']:,.2f}\n"
                    
                    st.download_button(
                        label=" Download Report (TXT)",
                        data=report_text,
                        file_name="impact_analysis_report.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

    # Footer
    render_footer()


if __name__ == '__main__':
    main()
