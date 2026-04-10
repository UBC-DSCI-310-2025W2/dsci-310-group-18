import pandas as pd


def prepare_eval_data(df: pd.DataFrame):
    """
    Prepare validation or test data for model evaluation.

    Parameters:
    ----------
    df : pandas.DataFrame
        Input DataFrame containing the target column `pha` and the columns
        expected by the evaluation pipeline.

        Required columns are:
        - `pha`
        - `abs_magnitude`
        - `epoch`
        - `min_orbit_intersection_dist`
        - `semi_major_axis`
        - `time_of_perihelion_passage`

        The returned feature matrix contains every remaining column after those
        fields are removed.

    Returns:
    -------
    tuple[pandas.DataFrame, pandas.Series]
        X : pandas.DataFrame
            Predictor columns used when scoring the trained model.
        y : pandas.Series
            Target labels from the `pha` column.
    
    Examples:
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     "pha": [0, 1],
    ...     "abs_magnitude": [21.1, 22.3],
    ...     "epoch": [2451545.0, 2451546.0],
    ...     "min_orbit_intersection_dist": [0.01, 0.02],
    ...     "semi_major_axis": [1.2, 1.4],
    ...     "time_of_perihelion_passage": [12345.0, 12346.0],
    ...     "eccentricity": [0.2, 0.3],
    ... })
    >>> X, y = prepare_eval_data(df)
    >>> list(X.columns)
    ['eccentricity']
    >>> y.tolist()
    [0, 1]

    Notes:
    -----
    This helper keeps the evaluation-time feature selection aligned with the
    columns removed before model scoring in the pipeline script.
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
