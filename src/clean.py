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
    >>> df = pd.read_csv('../data/raw/asteroid_data_raw.csv')
    >>> result = clean_pha(df)
    >>> print(result)

    Notes:
    -----
    This function uses the pandas library to perform mapping the target
    'pha' variable in the input DataFrame.
    """
    # Define map
    pha_map = {'Y': 1, 'N': 0}

    # Create copy of dataframe
    df = df.copy()

    df['pha'] = (
        df['pha']
        .astype(str) # handle non-strings safely
        .str.strip() # remove any whitespace
        .str.upper() # normalize case
        .map(pha_map) # apply mapping
    )

    # Raise error for unexpected NaN values.
    if df['pha'].isna().any():
        raise ValueError("Unexpected NaN values found in 'pha' column.")

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
    >>> df = pd.read_csv('../data/raw/asteroid_data_raw.csv')
    >>> result = clean_full_name(df)
    >>> print(result)

    Notes:
    -----
    This function uses regular expressions (regex) to clean and 
    standardize the asteroid full name in the input DataFrame.
    """
    # Create copy of dataframe
    df = df.copy()
    
    df['full_name'] = (
        df['full_name']
            .str.replace(r"[()]", "", regex=True) # remove parentheses using regex
            .str.replace(r"\s+", "_", regex=True) # replace spaces with underscores using regex
            .str.strip("_") # strip any leading or trailing underscores
    )

    return df