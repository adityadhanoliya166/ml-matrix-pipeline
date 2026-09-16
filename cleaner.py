import pandas as pd
import numpy as np

def clean_csv(file_path: str) -> pd.DataFrame:
    # 1. Load the raw dataset
    df = pd.read_csv(file_path)
    
    # 2. Drop completely duplicate rows
    df = df.drop_duplicates()
    
    # 3. Clean column names (strip whitespace and lowercase)
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    
    # 4. Clean text strings & auto-fix prices/numbers stored as strings
    for col in df.columns:
        if df[col].dtype == 'object':
            # Strip whitespace from text
            df[col] = df[col].astype(str).str.strip()
            
            # Try converting currency/percentage strings like "$100" or "50%" to numeric
            cleaned_col = df[col].str.replace('$', '', regex=False).str.replace('%', '', regex=False).str.replace(',', '', regex=False)
            try:
                df[col] = pd.to_numeric(cleaned_col)
            except (ValueError, TypeError):
                pass  # Keep as string if it's actual text
                
    # 5. Handle Missing Values
    for col in df.columns:
        if df[col].dtype in ['int64', 'float64']:
            # Fill numeric nulls with median
            df[col] = df[col].fillna(df[col].median())
        else:
            # Fill text nulls with "Unknown"
            df[col] = df[col].fillna("Unknown")
            
    return df