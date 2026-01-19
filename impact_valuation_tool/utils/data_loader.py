"""
Data loading utilities
"""
import pandas as pd


def load_data(filename: str, sheetname: str) -> pd.DataFrame:
    df = pd.read_excel(filename, sheetname)
    return df


def load_and_prepare_healthcare_data(filepath: str) -> pd.DataFrame:
    import os
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file '{filepath}' not found in the current directory.")
    
    master_costs_df = load_data(filepath, 'niveau2')
    
    COST_COLUMN_NAME = 'kosten per verzekerde 2024'
    alternative_columns = ['kosten per gebruiker 2024', 'kosten per gebruiker', 'Kosten per gebruiker 2024', 'Kosten per gebruiker']
    for col in alternative_columns:
        if col in master_costs_df.columns:
            COST_COLUMN_NAME = col
            break
    
    if COST_COLUMN_NAME not in master_costs_df.columns:
        raise ValueError(f"Cost column not found. Tried: {alternative_columns}. Available: {master_costs_df.columns.tolist()}")
    
    master_costs_df[COST_COLUMN_NAME] = master_costs_df[COST_COLUMN_NAME].astype(str)
    master_costs_df[COST_COLUMN_NAME] = pd.to_numeric(master_costs_df[COST_COLUMN_NAME], errors='coerce').fillna(0.0)
    
    return master_costs_df
