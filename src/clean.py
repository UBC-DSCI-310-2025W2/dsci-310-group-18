import pandas as pd

def clean_pha(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts target variable 'pha' to numeric (1/0).

    Parameters:
    ----------
    df : pandas.DataFrame
        Input dataframe containing 'pha' column.
    
    Returns:
    -------
    pandas.DataFrame
        A DataFrame with cleaned 'pha' column.

    Examples:
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({"pha": ["Y", " n ", "y"]})
    >>> result = clean_pha(df)
    >>> result["pha"].tolist()
    [1, 0, 1]

    Notes:
    -----
    This function uses the pandas library to perform mapping the target
    'pha' variable in the input DataFrame.
    """
    # Define map
    pha_map = {'Y': 1, 'N': 0}

    # Create copy of dataframe
    df = df.copy()

    # Handle NaNs first
    if df['pha'].isna().any():
        raise ValueError("The column contains NaN values.")

    cleaned = df['pha'] = (
        df['pha']
        .astype(str) # handle non-strings safely
        .str.strip() # remove any whitespace
        .str.upper() # normalize case
    )

    mapped = cleaned.map(pha_map)

    # Raise error for unexpected NaN values.
    if mapped.isna().any():
        raise ValueError("PHA column contains invalid values.")
    
    df['pha'] = mapped

    return df

def clean_full_name(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and standardizes asteroid full name.

    Parameters:
    ----------
    df : pandas DataFrame
        Input dataframe containing 'full_name' column.
    
    Returns:
    -------
    Pandas DataFrame with cleaned full name.

    Examples:
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({"full_name": ["Asteroid (1234)"]})
    >>> result = clean_full_name(df)
    >>> result["full_name"].iloc[0]
    'Asteroid_1234'

    Notes:
    -----
    This function uses regular expressions (regex) to clean and 
    standardize the asteroid full name in the input DataFrame.
    """
    # Create copy of dataframe
    df = df.copy()

    # Check for NaN
    if df['full_name'].isna().any():
        raise ValueError("The column contains NaN values.")
    
    # Check for non-strings
    if not df['full_name'].map(lambda x: isinstance(x, str)).all():
        raise ValueError("The column contains invalid values.")
    
    df['full_name'] = (
        df['full_name']
            .str.replace(r"[()]", "", regex=True) # remove parentheses using regex
            .str.replace(r"\s+", "_", regex=True) # replace spaces with underscores using regex
            .str.strip("_") # strip any leading or trailing underscores
    )

    return df
