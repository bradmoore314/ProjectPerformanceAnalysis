import pandas as pd
import numpy as np
from typing import Tuple

def load_and_process_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load and process the dataset files for the dashboard
    
    Returns:
        Tuple containing (summary_df, projects_df)
    """
    # Load the data
    try:
        summary_df = pd.read_csv("attached_assets/Summary.csv")
        projects_df = pd.read_csv("attached_assets/Projects.csv")
        
        # Clean up column names by removing leading/trailing spaces
        summary_df.columns = summary_df.columns.str.strip()
        projects_df.columns = projects_df.columns.str.strip()
        
        # Process projects data
        # Convert monetary columns to float
        money_columns = [col for col in projects_df.columns if 'Price' in col or 'Cost' in col or 'Margin' in col or 'Revenue' in col or 'Variance' in col]
        for col in money_columns:
            if projects_df[col].dtype == object:
                projects_df[col] = projects_df[col].str.replace('$', '', regex=False) if isinstance(projects_df[col], pd.Series) else projects_df[col]
                projects_df[col] = projects_df[col].str.replace(',', '', regex=False) if isinstance(projects_df[col], pd.Series) else projects_df[col]
                projects_df[col] = projects_df[col].str.replace(' ', '', regex=False) if isinstance(projects_df[col], pd.Series) else projects_df[col]
                projects_df[col] = pd.to_numeric(projects_df[col], errors='coerce')
        
        # Convert percentage columns
        pct_columns = [col for col in projects_df.columns if '%' in col]
        for col in pct_columns:
            if projects_df[col].dtype == object:
                projects_df[col] = projects_df[col].str.replace('%', '', regex=False) if isinstance(projects_df[col], pd.Series) else projects_df[col]
                projects_df[col] = pd.to_numeric(projects_df[col], errors='coerce') / 100
        
        # Convert date columns
        date_columns = [col for col in projects_df.columns if 'Date' in col]
        for col in date_columns:
            if projects_df[col].dtype == object:
                projects_df[col] = pd.to_datetime(projects_df[col], errors='coerce')
        
        # Calculate derived metrics if needed
        projects_df['Margin_Difference'] = projects_df['Actual Margin %'] - (projects_df['Estimated Margin %'] if 'Estimated Margin %' in projects_df.columns else 0)
        
        # Flag negative margin projects
        projects_df['Is_Negative_Margin'] = projects_df['Actual Margin %'] < 0
        
        # Calculate labor hour variance
        if 'Quoted Labor Hours' in projects_df.columns and 'Actual Labor Hours' in projects_df.columns:
            projects_df['Labor_Hours_Variance'] = projects_df['Actual Labor Hours'] - projects_df['Quoted Labor Hours']
            projects_df['Labor_Hours_Variance_Pct'] = projects_df['Labor_Hours_Variance'] / projects_df['Quoted Labor Hours'].replace(0, np.nan)
        
        return summary_df, projects_df
        
    except Exception as e:
        print(f"Error loading or processing data: {e}")
        # Return empty dataframes if there's an error
        return pd.DataFrame(), pd.DataFrame()
