import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any, Optional, Union
import numpy as np
import os
from google.generativeai import GenerativeModel
import google.generativeai as genai

def format_currency(value: Any) -> str:
    """Format a value as currency"""
    try:
        # If value is a string containing currency formatting, extract the numeric part
        if isinstance(value, str):
            # Remove dollar signs, commas, spaces
            value = value.strip().replace('$', '').replace(',', '').replace(' ', '')
            # Check for parentheses which indicate negative values
            if value.startswith('(') and value.endswith(')'):
                value = '-' + value[1:-1]
            value = float(value)
        
        return f"${value:,.2f}"
    except Exception as e:
        #print(f"Error formatting currency: {e} for value {value}")
        return "$0.00"

def format_percentage(value: Any) -> str:
    """Format a value as percentage"""
    try:
        # If value is a string containing percentage, extract the numeric part
        if isinstance(value, str):
            # Remove percent sign, spaces
            value = value.strip().replace('%', '')
            value = float(value) / 100  # Convert to decimal for percentage formatting
        
        return f"{value:.2%}"
    except Exception as e:
        #print(f"Error formatting percentage: {e} for value {value}")
        return "0.00%"

def create_metric_card(title: str, value: Any, delta: Optional[float] = None, 
                      is_currency: bool = False, is_percentage: bool = False,
                      help_text: str = "") -> None:
    """Create a metric card with styling"""
    # Use a consistent layout - just one column to ensure consistent width
    st.markdown(f"""
    <div style='background-color: #252525; padding: 10px; border-radius: 5px; border-left: 4px solid #e63946; margin-bottom: 10px; height: 80px;'>
        <p style='color: #aaa; margin-bottom: 4px; font-size: 14px;'>{title}</p>
        <p style='font-size: 20px; font-weight: bold; margin: 0;'>
            {format_currency(value) if is_currency else format_percentage(value) if is_percentage else value}
        </p>
        <p style='color: #aaa; font-size: 12px; margin-top: 4px;'>{help_text}</p>
    </div>
    """, unsafe_allow_html=True)

def create_bar_chart(df: pd.DataFrame, x: str, y: str, title: str, color: Optional[str] = None,
                    orientation: str = 'v', height: int = 400, y_min: Optional[float] = None) -> go.Figure:
    """Create a bar chart with Plotly"""
    # Define a custom color palette for better visibility
    custom_colors = ['#4D6FF3', '#5E82FF', '#6F94FF', '#80A6FF', '#91B9FF', '#A2CBFF', '#B3DDFF']
    
    # Create a copy of the dataframe to avoid modifying the original
    chart_df = df.copy()
    
    # Clean the y values if they are strings with $ or %
    if chart_df[y].dtype == object:
        chart_df[y] = chart_df[y].apply(
            lambda x: float(str(x).replace('$', '').replace(',', '').replace('%', '').strip()) 
            if isinstance(x, str) else x
        )
    
    # Create a basic figure
    if orientation == 'v':
        fig = go.Figure()
        
        # Add bars with conditional colors based on value
        for i, row in chart_df.iterrows():
            value = row[y]
            color = '#40CC5A' if value >= 0 else '#F04D4D'  # Green for positive, Red for negative
            
            fig.add_trace(go.Bar(
                x=[row[x]],
                y=[value],
                name=row[x],
                marker_color=color,
                showlegend=False
            ))
    else:
        fig = go.Figure()
        
        # Add bars with conditional colors based on value
        for i, row in chart_df.iterrows():
            value = row[y]
            color = '#40CC5A' if value >= 0 else '#F04D4D'  # Green for positive, Red for negative
            
            fig.add_trace(go.Bar(
                y=[row[x]],
                x=[value],
                name=row[x],
                marker_color=color,
                orientation='h',
                showlegend=False
            ))
    
    # Add title
    fig.update_layout(title=title)
    
    # Determine axis range to ensure negative values are visible
    if orientation == 'v':
        min_value = chart_df[y].min()
        max_value = chart_df[y].max()
        
        # When y_min is explicitly provided, always use it regardless of data values
        if y_min is not None:
            y_min_value = y_min
            y_max = max_value * 1.1
        else:
            # For financial charts, always include some negative range
            # Check if this is likely a financial chart (look for $ in title or 'variance', 'margin', 'cost' in title)
            is_financial = any(term in title.lower() for term in ['$', 'variance', 'margin', 'cost'])
            
            if is_financial:
                # Always show some negative range for financial charts
                # If min_value is negative, go a bit below it
                # If min_value is positive, still show some negative range (20% of the max value)
                y_min_value = min(min_value * 1.1, -max_value * 0.2) if min_value < 0 else -max_value * 0.2
                y_max = max_value * 1.1
            else:
                # For non-financial charts, only extend below zero if there are negative values
                y_min_value = min(0, min_value) * 1.1 if min_value < 0 else 0  # Default to 0 instead of None
                y_max = max_value * 1.1 if max_value > 0 else None
    else:
        min_value = chart_df[y].min()
        max_value = chart_df[y].max()
        
        # When y_min is explicitly provided for horizontal charts (affects x-axis)
        if y_min is not None:
            x_min = y_min
            x_max = max_value * 1.1
        else:
            # For financial charts, always include some negative range
            is_financial = any(term in title.lower() for term in ['$', 'variance', 'margin', 'cost'])
            
            if is_financial:
                # Always show some negative range for financial charts
                x_min = min(min_value * 1.1, -max_value * 0.2) if min_value < 0 else -max_value * 0.2
                x_max = max_value * 1.1
            else:
                # For non-financial charts, only extend below zero if there are negative values
                x_min = min(0, min_value) * 1.1 if min_value < 0 else 0  # Default to 0 instead of None
                x_max = max_value * 1.1 if max_value > 0 else None
    
    # Enhanced layout settings
    layout_settings = {
        'plot_bgcolor': 'rgba(30,30,30,0.3)',  # Slightly visible dark background
        'paper_bgcolor': 'rgba(0,0,0,0)',      # Transparent paper
        'title_font': dict(size=18, color='#ffffff'),
        'font': dict(color='#ffffff', size=14),
        'xaxis': dict(
            title_font=dict(size=14, color='#ffffff'),
            tickfont=dict(size=12, color='#ffffff'),
            showgrid=True,
            gridcolor='rgba(100,100,100,0.2)',
            showline=True,
            linewidth=1,
            linecolor='rgba(200,200,200,0.3)',
        ),
        'yaxis': dict(
            title_font=dict(size=14, color='#ffffff'),
            tickfont=dict(size=12, color='#ffffff'),
            showgrid=True,
            gridcolor='rgba(100,100,100,0.2)',
            showline=True,
            linewidth=1,
            linecolor='rgba(200,200,200,0.3)',
            # Add a zero line for better visualization
            zeroline=True,
            zerolinecolor='rgba(255,255,255,0.5)',
            zerolinewidth=1.5
        ),
        'margin': dict(l=40, r=40, t=50, b=40),
        'height': height,
        'template': "plotly_dark"
    }
    
    # Always apply axis ranges when orientation is vertical
    if orientation == 'v':
        layout_settings['yaxis']['range'] = [y_min_value, y_max]
    else:
        layout_settings['xaxis']['range'] = [x_min, x_max]
    
    fig.update_layout(**layout_settings)
    
    return fig

def create_line_chart(df: pd.DataFrame, x: str, y: Union[str, List[str]], title: str, color: Optional[str] = None,
                     height: int = 400) -> go.Figure:
    """Create a line chart with Plotly"""
    # Define a custom color palette for better visibility
    custom_colors = ['#4D6FF3', '#F04D4D', '#40CC5A', '#E6C830', '#9850E6', '#F98D00', '#00D0FA']
    
    # Clean numeric columns if they are strings with $ or %
    clean_df = df.copy()
    
    # Handle both string and list for y parameter
    y_cols = [y] if isinstance(y, str) else y
    
    for col in y_cols:
        if col in clean_df.columns and clean_df[col].dtype == object:
            if any('$' in str(val) for val in clean_df[col] if isinstance(val, str)):
                clean_df[col] = clean_df[col].apply(
                    lambda x: float(str(x).replace('$', '').replace(',', '').strip()) 
                    if isinstance(x, str) else x
                )
            elif any('%' in str(val) for val in clean_df[col] if isinstance(val, str)):
                clean_df[col] = clean_df[col].apply(
                    lambda x: float(str(x).replace('%', '').strip()) / 100
                    if isinstance(x, str) else x
                )
    
    fig = px.line(
        clean_df, x=x, y=y, 
        title=title,
        color=color,
        color_discrete_sequence=custom_colors,
        template="plotly_dark",
        height=height
    )
    
    # Thicker lines for better visibility (update line width after figure creation)
    fig.update_traces(line=dict(width=3))
    
    # Enhanced layout settings
    fig.update_layout(
        plot_bgcolor='rgba(30,30,30,0.3)',  # Slightly visible dark background
        paper_bgcolor='rgba(0,0,0,0)',      # Transparent paper
        title_font=dict(size=18, color='#ffffff'),
        font=dict(color='#ffffff', size=14),
        legend_title_font=dict(color='#ffffff'),
        legend_font=dict(color='#ffffff'),
        xaxis=dict(
            title_font=dict(size=14, color='#ffffff'),
            tickfont=dict(size=12, color='#ffffff'),
            showgrid=True,
            gridcolor='rgba(100,100,100,0.2)',
            showline=True,
            linewidth=1,
            linecolor='rgba(200,200,200,0.3)',
        ),
        yaxis=dict(
            title_font=dict(size=14, color='#ffffff'),
            tickfont=dict(size=12, color='#ffffff'),
            showgrid=True,
            gridcolor='rgba(100,100,100,0.2)',
            showline=True,
            linewidth=1,
            linecolor='rgba(200,200,200,0.3)',
        ),
        margin=dict(l=40, r=40, t=50, b=40)
    )
    
    fig.update_traces(marker=dict(size=8))  # Larger markers for data points
    
    return fig

def create_pie_chart(df: pd.DataFrame, values: str, names: str, title: str,
                    height: int = 400) -> go.Figure:
    """Create a pie chart with Plotly"""
    # Diverse color palette with vibrant colors for better visibility
    custom_colors = [
        '#4CAF50', '#2196F3', '#F44336', '#FF9800', '#9C27B0', 
        '#00BCD4', '#FFEB3B', '#8BC34A', '#3F51B5', '#009688',
        '#673AB7', '#CDDC39', '#795548', '#E91E63', '#607D8B'
    ]
    
    fig = px.pie(
        df, values=values, names=names,
        title=title,
        template="plotly_dark",
        height=height,
        hole=0.4,
        color_discrete_sequence=custom_colors
    )
    
    # Enhanced layout settings
    fig.update_layout(
        plot_bgcolor='rgba(30,30,30,0.3)',  # Slightly visible dark background
        paper_bgcolor='rgba(0,0,0,0)',      # Transparent paper
        title_font=dict(size=18, color='#ffffff'),
        font=dict(color='#ffffff', size=14),
        legend=dict(
            font=dict(color='#ffffff', size=12),
            bgcolor='rgba(0,0,0,0.2)',
            bordercolor='rgba(255,255,255,0.3)',
            borderwidth=1
        )
    )
    
    # Update trace settings for better visibility
    fig.update_traces(
        textfont=dict(size=14, color='#ffffff'),
        marker=dict(line=dict(color='#000000', width=1.5))
    )
    
    return fig

def analyze_negative_margin_projects(projects_df: pd.DataFrame) -> str:
    """
    AI analysis of negative margin projects using Gemini API.
    """
    try:
        api_key = "AIzaSyAXl1y6xCNoIek55f9JuOBGcAV16P-91Fw"
        
        if not api_key:
            return """
            **No API key found for Gemini. Please add a GEMINI_API_KEY to your environment variables.**
            
            In the meantime, here is a placeholder analysis:
            
            ## Common Issues in Negative Margin Projects
            
            * Labor hours significantly exceeding estimates
            * Parts costs variance higher than expected
            * Scope creep without proper change orders
            * Insufficient pricing for complex takeover projects
            * Geographic variations in labor efficiency
            
            ## Recommendations
            
            * Improve labor estimation process for takeover projects
            * Implement better scope definition and change management
            * Develop region-specific pricing models
            * Establish clearer performance metrics for project managers
            """
        
        # Initialize Gemini API
        genai.configure(api_key=api_key)
        model = GenerativeModel('gemini-1.5-pro')
        
        # Prepare negative margin projects data
        negative_margin_projects = projects_df[projects_df['Actual Margin %'] < 0].copy()
        
        # Limit data to important columns to fit in the context window
        columns_to_include = [
            'Topic', 'Region', 'Owner', 'Actual Margin %', 'Total Costs Variance $',
            'Quoted Labor Hours', 'Actual Labor Hours', 'Labor Variance $',
            'Parts Variance $', 'Calculated Total Install Price $'
        ]
        
        # Only include columns that exist in the dataframe
        columns_to_use = [col for col in columns_to_include if col in negative_margin_projects.columns]
        
        # Get notes column if it exists
        notes_col = next((col for col in negative_margin_projects.columns if 'Notes' in col or 'Performance' in col), None)
        if notes_col:
            columns_to_use.append(notes_col)
        
        # Get a subset of the data with only the relevant columns
        data_for_analysis = negative_margin_projects[columns_to_use].head(15)  # Limit to top 15 negative margin projects
        
        # Prepare prompt
        prompt = f"""
        I'm analyzing financial data for projects with negative margins. 
        Here's the data for some representative negative margin projects:
        
        {data_for_analysis.to_csv(index=False)}
        
        Based on this data, please provide:
        1. 5-6 bullet points identifying common issues or patterns in these negative margin projects
        2. 3-4 actionable recommendations for improving profitability on future projects
        3. A brief analysis of the relationship between quoted vs. actual labor hours in these projects
        
        Format your response as markdown with clear sections.
        Focus on practical, data-driven insights that can help improve project performance.
        """
        
        # Generate response
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"""
        **Error using Gemini API: {str(e)}**
        
        In the meantime, here is a placeholder analysis:
        
        ## Common Issues in Negative Margin Projects
        
        * Labor hours significantly exceeding estimates
        * Parts costs variance higher than expected
        * Scope creep without proper change orders
        * Insufficient pricing for complex takeover projects
        * Geographic variations in labor efficiency
        
        ## Recommendations
        
        * Improve labor estimation process for takeover projects
        * Implement better scope definition and change management
        * Develop region-specific pricing models
        * Establish clearer performance metrics for project managers
        """
