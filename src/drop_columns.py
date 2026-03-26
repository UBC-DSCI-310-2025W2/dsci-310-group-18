import pandas as pd


def drop_columns(data_frame, columns):
    """
    Remove selected columns from a pandas DataFrame.

    Parameters
    ----------
    data_frame : pandas.DataFrame
        Input DataFrame.
    columns : list of str
        Names of columns to remove.

    Returns
    -------
    pandas.DataFrame
        A new DataFrame with the selected columns removed.

    Raises
    ------
    TypeError
        If ``data_frame`` is not a pandas DataFrame or ``columns`` is not a list.
    KeyError
        If any requested column names are not present in ``data_frame``.
    """
    if not isinstance(data_frame, pd.DataFrame):
        raise TypeError("data_frame must be a pandas DataFrame")
    if not isinstance(columns, list):
        raise TypeError("columns must be provided as a list of strings")

    return data_frame.drop(columns=columns)
