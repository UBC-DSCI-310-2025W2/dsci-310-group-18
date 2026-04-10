"""Utilities for inferring appropriate plot scales from data.

The main helper, ``infer_plot_scales``, examines the empirical distribution
of numeric columns and suggests whether each one should be plotted on a
linear or logarithmic scale.
"""

from __future__ import annotations

from typing import Dict, Iterable, List

import pandas as pd


def infer_plot_scales(
    df: pd.DataFrame,
    columns: Iterable[str],
    log_if_skewed: bool = True,
    skew_threshold: float = 1.0,
    positive_only: bool = True,
) -> Dict[str, str]:
    """Infer per-column plot scales (``'linear'`` or ``'log'``).

    Parameters
    ----------
    df:
        Input DataFrame containing the columns of interest.
    columns:
        Iterable of column names to inspect.
    log_if_skewed:
        If True, highly right-skewed distributions will be mapped to ``'log'``.
    skew_threshold:
        Absolute skewness above which a column is considered "skewed".
    positive_only:
        If True, a column must be strictly positive to be considered for
        logarithmic scaling; otherwise it is forced to ``'linear'``.

    Returns
    -------
    Dict[str, str]
        Mapping from column name to either ``'linear'`` or ``'log'``.

    Raises
    ------
    TypeError
        If ``df`` is not a ``pandas.DataFrame``.
    KeyError
        If any requested column is missing from ``df``.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")

    cols: List[str] = list(columns)
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise KeyError(f"Missing columns in df: {missing}")

    scales: Dict[str, str] = {}

    for col in cols:
        series = df[col].dropna()

        # Default assumption: linear scale
        scale = "linear"

        if log_if_skewed and not series.empty:
            if positive_only and (series <= 0).any():
                # Cannot safely apply log scale to non-positive values
                scale = "linear"
            else:
                skew = series.skew()
                if abs(skew) >= skew_threshold:
                    scale = "log"

        scales[col] = scale

    return scales

