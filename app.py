import streamlit as st
import pandas as pd
import os
import components.dashboard
from components.personnel_analysis import show_personnel_analysis
from components.negative_margin import show_negative_margin_analysis
from components.project_details import show_project_details
from components.ai_analysis import show_ai_analysis
from data_processor import load_and_process_data

# Simple password protection
st.set_page_config(
    page_title="Project Profit Pulse",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Password protection
def check_password():
    """Returns `True` if the user had the correct password."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets.get("password", "projectpulse123"):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password
        st.markdown("""
        <style>
        .password-container {
            max-width: 500px;
            margin: 0 auto;
            padding: 2rem;
            border-radius: 10px;
            background-color: #1e1e1e;
            border: 1px solid #333;
            margin-top: 20vh;
        }
        .logo {
            text-align: center;
            margin-bottom: 2rem;
        }
        </style>
        """, unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="password-container">', unsafe_allow_html=True)
            st.markdown('<div class="logo"><h1>📊 Project Profit Pulse</h1></div>', unsafe_allow_html=True)
            st.text_input(
                "Password", type="password", on_change=password_entered, key="password"
            )
            st.markdown("</div>", unsafe_allow_html=True)
        return False
    
    return st.session_state["password_correct"]

# If password check fails, stop execution
if not check_password():
    st.stop()  # App won't run past this point

# Hide Streamlit branding
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Custom CSS for dark theme with red trim
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #f0f0f0;
        margin-bottom: 1rem;
        border-bottom: 2px solid #e63946;
        padding-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #e63946;
        margin-bottom: 1rem;
    }
    .card {
        background-color: #252525;
        border-radius: 5px;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #aaa;
    }
    .red-accent {
        color: #e63946;
    }
    .sidebar .sidebar-content {
        background-color: #1e1e1e;
    }
    img {
        display: none !important;
    }
    
    /* Custom button styling */
    div[data-testid="stButton"] button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
        margin: 5px 0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Dashboard button */
    .dashboard-btn button {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        border: none;
    }
    .dashboard-btn button:hover {
        background: linear-gradient(90deg, #0072ff, #00c6ff);
        transform: translateY(-2px);
        box-shadow: 0 0 15px rgba(0, 198, 255, 0.6);
    }
    
    /* Negative margin button */
    .negative-btn button {
        background: linear-gradient(90deg, #4cc9f0, #4895ef);
        border: none;
    }
    .negative-btn button:hover {
        background: linear-gradient(90deg, #4895ef, #4cc9f0);
        transform: translateY(-2px);
        box-shadow: 0 0 15px rgba(76, 201, 240, 0.6);
    }
    
    /* Personnel button */
    .personnel-btn button {
        background: linear-gradient(90deg, #00b4d8, #0077b6);
        border: none;
    }
    .personnel-btn button:hover {
        background: linear-gradient(90deg, #0077b6, #00b4d8);
        transform: translateY(-2px);
        box-shadow: 0 0 15px rgba(0, 180, 216, 0.6);
    }
    
    /* Project details button */
    .details-btn button {
        background: linear-gradient(90deg, #3a0ca3, #4361ee);
        border: none;
    }
    .details-btn button:hover {
        background: linear-gradient(90deg, #4361ee, #3a0ca3);
        transform: translateY(-2px);
        box-shadow: 0 0 15px rgba(67, 97, 238, 0.6);
    }
    
    /* AI button */
    .ai-btn button {
        background: linear-gradient(90deg, #7209b7, #3f37c9);
        border: none;
        text-transform: uppercase;
        letter-spacing: 1px;
        animation: pulse 1.5s infinite;
    }
    .ai-btn button:hover {
        background: linear-gradient(90deg, #3f37c9, #7209b7);
        transform: translateY(-2px);
        box-shadow: 0 0 15px rgba(114, 9, 183, 0.6);
    }
    
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(114, 9, 183, 0.7);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(114, 9, 183, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(114, 9, 183, 0);
        }
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.markdown('<h1 class="main-header">Project Profit Pulse</h1>', unsafe_allow_html=True)

# Load and process data
summary_df, projects_df = load_and_process_data()

# Sidebar navigation
st.sidebar.title("Navigation")

# Add global filters
st.sidebar.markdown('<h2 class="sub-header">Filters</h2>', unsafe_allow_html=True)

# Filter by date if date column exists
if 'Projected End Date' in projects_df.columns:
    min_date = pd.to_datetime(projects_df['Projected End Date']).min()
    max_date = pd.to_datetime(projects_df['Projected End Date']).max()
    
    # Set default date range to Q1 2025
    default_start = pd.Timestamp('2025-01-01')
    default_end = pd.Timestamp('2025-03-31')
    
    # Ensure default dates are within the available range
    default_start = max(default_start, min_date)
    default_end = min(default_end, max_date)
    
    date_range = st.sidebar.date_input(
        "Date Range",
        [default_start, default_end],
        min_value=min_date,
        max_value=max_date
    )
    
    # Apply date filter if selected
    if len(date_range) == 2:
        start_date, end_date = date_range
        projects_df = projects_df[(pd.to_datetime(projects_df['Projected End Date']).dt.date >= start_date) & 
                                 (pd.to_datetime(projects_df['Projected End Date']).dt.date <= end_date)]

# Filter by region
if 'Region' in projects_df.columns:
    regions = ['All'] + sorted(projects_df['Region'].dropna().unique().tolist())
    selected_region = st.sidebar.selectbox("Region", regions)
    
    if selected_region != 'All':
        projects_df = projects_df[projects_df['Region'] == selected_region]

# Add navigation buttons section
st.sidebar.markdown('<h2 class="sub-header">Views</h2>', unsafe_allow_html=True)

# Get current page from query params
query_params = st.query_params
current_page = query_params.get("page", "Dashboard")

# Function to create a navigation button
def nav_button(label, page_name, icon, button_class):
    button_html = f'<div class="{button_class}">{{button_placeholder}}</div>'
    button_placeholder = st.sidebar.empty()
    button_placeholder.markdown(button_html, unsafe_allow_html=True)
    
    # Replace the placeholder with a real button
    with button_placeholder:
        is_current = current_page == page_name
        button_label = f"{icon} {label}"
        if st.button(button_label, key=f"btn_{page_name}", use_container_width=True, disabled=is_current):
            # Set query parameter and rerun
            st.query_params.update({"page": page_name})
            st.rerun()

# Dashboard Button
nav_button("Dashboard Overview", "Dashboard", "📊", "dashboard-btn")

# Negative Margin Projects Button
nav_button("Negative Margin Projects", "Negative", "📉", "negative-btn")

# Personnel Analysis Button
nav_button("Personnel Analysis", "Personnel", "👥", "personnel-btn")

# Project Details Button
nav_button("Project Details", "Details", "🔍", "details-btn")

# Add AI Analysis button section
st.sidebar.markdown('<h2 class="sub-header">AI Analysis</h2>', unsafe_allow_html=True)

# AI Analysis Button
nav_button("AI Project Analysis", "AI", "🤖", "ai-btn")

# Render the selected page
if current_page == "Dashboard":
    components.dashboard.show_dashboard(summary_df, projects_df)
elif current_page == "Personnel":
    show_personnel_analysis(projects_df)
elif current_page == "Negative":
    show_negative_margin_analysis(projects_df)
elif current_page == "AI":
    show_ai_analysis(projects_df)
elif current_page == "Details":
    show_project_details(projects_df)
else:
    components.dashboard.show_dashboard(summary_df, projects_df)
