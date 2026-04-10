import pandas as pd


def drop_columns(data_frame, columns):
    """
    Drop selected columns from a pandas DataFrame with input validation.

    Parameters:
    ----------
    data_frame : pandas.DataFrame
        Input dataframe containing columns to remove.
    columns : list of str
        Names of columns to remove.

    Returns:
    -------
    pandas.DataFrame
        A DataFrame with the selected columns removed.

    Examples:
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({"pha": [0, 1], "epoch": [1, 2], "feature_x": [3, 4]})
    >>> result = drop_columns(df, ["epoch"])
    >>> print(result)

    Notes:
    ------
    This helper is intentionally thin around `pandas.DataFrame.drop`, but it
    centralizes basic input validation and gives the training pipeline a single
    project-level function to test and reuse.
    """
    if not isinstance(data_frame, pd.DataFrame):
        raise TypeError("data_frame must be a pandas DataFrame")
    if not isinstance(columns, list):
        raise TypeError("columns must be provided as a list of strings")

    return data_frame.drop(columns=columns)
