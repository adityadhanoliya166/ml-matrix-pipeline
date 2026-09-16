import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

def transform_to_ml_matrix(cleaned_df: pd.DataFrame) -> pd.DataFrame:
    df = cleaned_df.copy()

    # Convert numeric columns safely and handle missing values
    for col in df.columns:
        # Try converting to numeric where possible
        converted = pd.to_numeric(df[col], errors='coerce')
        
        # If it was numeric, fill NaNs with median
        if converted.notna().sum() > 0 and df[col].dtype != 'object':
            df[col] = converted.fillna(converted.median())
        else:
            # Categorical/text columns
            df[col] = df[col].fillna('Missing').astype(str)

    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

    transformers = []
    if numeric_cols:
        transformers.append(('num', StandardScaler(), numeric_cols))
    if categorical_cols:
        transformers.append(('cat', OneHotEncoder(sparse_output=False, handle_unknown='ignore'), categorical_cols))

    if not transformers:
        return df

    preprocessor = ColumnTransformer(transformers=transformers)
    matrix_array = preprocessor.fit_transform(df)

    cat_feature_names = []
    if categorical_cols:
        cat_encoder = preprocessor.named_transformers_['cat']
        cat_feature_names = list(cat_encoder.get_feature_names_out(categorical_cols))

    all_feature_names = numeric_cols + cat_feature_names
    return pd.DataFrame(matrix_array, columns=all_feature_names)