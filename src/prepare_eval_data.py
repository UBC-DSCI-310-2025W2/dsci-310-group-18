import pandas as pd


def prepare_eval_data(df: pd.DataFrame):
    """
    Prepare validation / test data for model evaluation.

    Parameters:
    ----------
    df : pandas.DataFrame
        Input DataFrame containing the target variable 'pha' and columns to drop before evaluation.

    Returns:
    -------
    tuple[pandas.DataFrame, pandas.Series]
        X : DataFrame of predictor columns used for evaluation
        y : Series containing the target column 'pha'
    
    Examples:
    --------
    >>> import pandas as pd
    >>> df = pd.read_csv("data/clean/asteroid_data_clean.csv")
    >>> X, y = prepare_eval_data(df)
    >>> print(X.head())
    >>> print(y.head())

    Notes:
    -----
    This function implements the evaluation data preparation used in scripts/06_eval-predict.py.
    """

    # verify input type
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")

    # verify required columns
    required_columns = {
        "pha",
        "abs_magnitude",
        "epoch",
        "min_orbit_intersection_dist",
        "semi_major_axis",
        "time_of_perihelion_passage",
    }
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise KeyError(f"Missing required columns: {sorted(missing_columns)}")

    # split predictors and target
    X = df.drop(
        columns=[
            "pha",
            "abs_magnitude",
            "epoch",
            "min_orbit_intersection_dist",
            "semi_major_axis",
            "time_of_perihelion_passage",
        ]
    )
    y = df["pha"]

    return X, y