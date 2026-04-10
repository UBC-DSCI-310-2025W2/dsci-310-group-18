import pandas as pd

def split_features_target(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """
    Split the cleaned asteroid DataFrame into model features and target.

    Parameters:
    ----------
    df : pandas.DataFrame
        Input DataFrame containing at least:
        - `pha`: the binary target column
        - `spkid`: the asteroid identifier column

        All numeric columns other than `pha` and `spkid` are treated as model
        features. Non-numeric columns are excluded from the returned feature
        matrix.

    Returns:
    -------
    tuple[pandas.DataFrame, pandas.Series]
        X : DataFrame
            Numeric feature columns used for model training.
        y : pandas.Series
            Target labels from the `pha` column.

    Examples:
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     "spkid": [1, 2],
    ...     "pha": [0, 1],
    ...     "eccentricity": [0.2, 0.3],
    ...     "full_name": ["A", "B"],
    ... })
    >>> X, y = split_features_target(df)
    >>> list(X.columns)
    ['eccentricity']
    >>> y.tolist()
    [0, 1]

    Notes:
    -----
    This helper centralizes the feature/target split used in the preprocessing
    pipeline so the selection logic stays consistent between scripts and tests.
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
