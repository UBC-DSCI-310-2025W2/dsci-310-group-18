import pandas as pd

def split_features_target(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """
    Splits the cleaned asteroid dataframe into features and target.

    Parameters:
    ----------
    df : pandas.DataFrame
        Input DataFrame containing the target variable 'pha' and identifier 'spkid'.

    Returns:
    -------
    tuple[pandas.DataFrame, pandas.Series]
        X : DataFrame of numeric predictor columns only, excluding 'pha'
            and 'spkid'
        y : Series containing the target column 'pha'

    Examples:
    --------
    >>> import pandas as pd
    >>> df = pd.read_csv("data/clean/asteroid_data_clean.csv")
    >>> X, y = split_features_target(df)
    >>> print(X.head())
    >>> print(y.head())

    Notes:
    -----
    This function implements the feature-target selection logic used in scripts/03_split-data.py.
    """
    # verify input type
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")

    # verify required columns
    required_columns = {"pha", "spkid"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise KeyError(f"Missing required columns: {sorted(missing_columns)}")

    # split predictors and target
    X = df.select_dtypes(include="number").drop(columns=["pha", "spkid"])
    y = df["pha"]

    return X, y