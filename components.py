"""
Streamlit UI components for input handling
"""
import streamlit as st
from src.models import ImpactTool


def render_sidebar(st_session):
    with st.sidebar:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 1.5rem;">
            <h2 style="color: white; margin-top: 0;">ℹ️ About This Tool</h2>
            <p style="color: #f0f0f0; margin: 0;">
                <strong>Financial Impact Tool for Lifestyle Coaches</strong><br>
                Calculate potential healthcare cost savings from lifestyle coaching interventions.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**📊 Data Source**")
        st.markdown("2024 Dutch healthcare cost data (per capita annual costs)")
        
        st.markdown("---")
        
        with st.expander("🔍 Methodology Details"):
            st.markdown("""
            **How calculations work:**
            - Each health condition has associated annual healthcare costs based on 2024 Dutch data
            - Costs are calculated by multiplying the number of patients by the cost per patient
            - Total societal impact represents potential healthcare system savings from preventive interventions
            - Scenario analysis uses prevalence reduction assumptions
            """)
            
        with st.expander("📚 Data Sources"):
            st.markdown("""
            **Healthcare Cost Data:**
            - **Source:** 2024 Dutch healthcare insurance data
            - **Coverage:** Comprehensive healthcare services including:
              - GP visits & consultations
              - Specialist care
              - Medications & pharmaceutical care
              - Therapies (physical, occupational, speech)
              - Hospital care & procedures
            - **Update Frequency:** Annual updates reflect current healthcare costs
            """)
            
        with st.expander("🤝 Contact & Support"):
            st.markdown("""
            **Questions or feedback?**
            - This tool is designed for lifestyle coaches and healthcare professionals
            - Data accuracy is based on official healthcare cost databases
            - Contact your healthcare institution for implementation guidance
            
            **Disclaimer:** Results are estimates for informational purposes only.
            """)
        
        st.markdown("---")
        
        if st.button("🎨 Switch Theme", use_container_width=True):
            st_session.theme = 'dark' if st_session.theme == 'light' else 'light'
            st.rerun()
        
        st.caption(f"Current theme: {st_session.theme.capitalize()}")
        st.caption("© 2025 Financial Impact Tool\nMade by Séphora, Aslihan, Dinand, Quinn & Karan")


def render_patient_input_section(impact_tool: ImpactTool, st_session):
    st.markdown('<div class="sub-header"> Enter the number of patients you treat for each specified health condition</div>', unsafe_allow_html=True)

    # Condition descriptions
    condition_descriptions = {
        'Burn-Out': 'Physical and mental exhaustion due to prolonged stress at work',
        'Depression': 'Persistent depressive mood and loss of interest',
        'Anxiety Disorder': 'Intense anxiety or panic feelings that affect daily life',
        'Stress': 'Physical and mental response to demands and pressure',
        'Hernia': 'Protrusion of organs due to a weakened muscle wall, often in the back/abdomen',
        'RSI': 'Repetitive Strain Injury – pain complaints caused by repetitive movements',
        'Osteoarthritis': 'Wear-and-tear osteoarthritis – degeneration of joint cartilage',
        'Cardiovascular diseases': 'Cardiovascular diseases, including heart attack and stroke',
        'Eating disorder': 'Eating disorder such as anorexia or bulimia',
        'Type 2 diabetes': 'Diabetes caused by insulin resistance',
        'Certain cancers': 'Malignant tumors',
        'High blood pressure': 'Hypertension – high blood pressure',
        'Sleep apnea': 'Sleep-related breathing disorders',
        'Narcolepsy': 'Tendency for involuntary daytime sleep episodes',
        'Restless legs syndrome': 'RLS – restlessness and pain in the legs, especially at night',
        'Chronic Fatigue': 'ME/CFS – severe fatigue after minimal exertion',
        'Prevented suicide': 'Prevention of suicide attempts',
        'Addiction': 'Addiction to substances or behaviors',
        'Violence': 'Aggressive behavior and violent incidents',
        'Abuse': 'Abuse – physical, psychological, or sexual'
    }

    patients_per_condition = {}
    total_entered_patients = 0

    # Group inputs by category
    for category, conditions in impact_tool.CATEGORIES.items():
        with st.expander(f" {category.upper()}", expanded=False):
            for condition in conditions:
                # Get description
                description_text = condition_descriptions.get(condition, '')
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); padding: 1.5rem; border-radius: 12px; border-left: 5px solid #667eea; margin-bottom: 1.5rem;">
                    <h4 style="margin-top: 0; margin-bottom: 0.5rem; color: #667eea;"> {condition}</h4>
                    <p style="margin: 0.5rem 0 1rem 0; color: #666; font-size: 0.9rem;"><em>{description_text}</em></p>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    default_value = st_session.patients_per_condition.get(condition, 0)
                    count = st.number_input(
                        f"Patients", 
                        min_value=0, 
                        step=1, 
                        value=default_value, 
                        key=f"{category}_{condition}_count",
                        help=f"Enter the number of patients you treat for {condition.lower()}."
                    )
                    patients_per_condition[condition] = count
                    total_entered_patients += count
                
                with col2:
                    if condition not in st_session.condition_details:
                        default_cost, _ = impact_tool.cost_model.get_cost_per_condition(condition)
                        st_session.condition_details[condition] = {
                            "description": "",
                            "custom_cost": None,
                            "default_cost": default_cost
                        }
                    
                    if "default_cost" not in st_session.condition_details[condition]:
                        default_cost, _ = impact_tool.cost_model.get_cost_per_condition(condition)
                        st_session.condition_details[condition]["default_cost"] = default_cost
                    
                    default_cost = st_session.condition_details[condition].get("default_cost", 0.0)
                    custom_cost_val = st_session.condition_details[condition].get("custom_cost")
                    display_cost = custom_cost_val if custom_cost_val is not None else default_cost
                    
                    st.caption(f"Default: € {default_cost:,.2f}")
                    custom_cost = st.number_input(
                        "Cost per patient (€)",
                        min_value=0.0,
                        step=10.0,
                        value=display_cost,
                        key=f"{category}_{condition}_cost",
                        help="Override the default cost with your own estimate"
                    )
                    if abs(custom_cost - default_cost) > 0.01:
                        st_session.condition_details[condition]["custom_cost"] = custom_cost
                    else:
                        st_session.condition_details[condition]["custom_cost"] = None
                
                description = st.text_area(
                    "Description/Notes",
                    value=st_session.condition_details[condition].get("description", ""),
                    key=f"{category}_{condition}_desc",
                    help = "Describe here how your organization addresses this condition or how you, as an organization, make an impact on it.",
                    height=80
                )
                st_session.condition_details[condition]["description"] = description

                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("---")

    st_session.patients_per_condition = patients_per_condition
    total_patients = total_entered_patients
    st_session.total_patients = total_patients
    return total_patients, patients_per_condition, total_entered_patients
