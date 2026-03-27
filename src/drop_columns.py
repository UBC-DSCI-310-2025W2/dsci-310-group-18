import pandas as pd


def drop_columns(data_frame, columns):
    """
    Drops selected columns from a pandas DataFrame.

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
    This function uses the pandas library to remove a specified set of
    columns from the input DataFrame. It raises a TypeError if the
    input is not a pandas DataFrame or if columns is not provided as a list.
    """
    if not isinstance(data_frame, pd.DataFrame):
        raise TypeError("data_frame must be a pandas DataFrame")
    if not isinstance(columns, list):
        raise TypeError("columns must be provided as a list of strings")

    return data_frame.drop(columns=columns)
