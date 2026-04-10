import pandas as pd
import pytest

from src.infer_plot_scales import infer_plot_scales


def test_infer_plot_scales_basic_behavior():
    """Highly skewed positive columns should be assigned a log scale."""
    df = pd.DataFrame(
        {
            "mild": [1, 2, 3, 4, 5],
            "skewed": [1, 1, 1, 1, 100],
        }
    )

    scales = infer_plot_scales(df, ["mild", "skewed"], skew_threshold=1.0)

    assert scales["mild"] == "linear"
    assert scales["skewed"] == "log"


def test_infer_plot_scales_non_positive_values_force_linear():
    """Columns containing non-positive values should never be log-scaled."""
    df = pd.DataFrame(
        {
            "has_zero": [0, 1, 2, 3],
            "has_negative": [-1, 0, 1, 1],
        }
    )

    scales = infer_plot_scales(df, ["has_zero", "has_negative"], positive_only=True)

    assert scales["has_zero"] == "linear"
    assert scales["has_negative"] == "linear"


def test_infer_plot_scales_requires_dataframe():
    """The helper should reject non-DataFrame inputs."""
    with pytest.raises(TypeError, match="df must be a pandas DataFrame"):
        infer_plot_scales(["not", "a", "df"], ["a"])


def test_infer_plot_scales_missing_columns_error():
    """The helper should raise when requested columns are not present."""
    df = pd.DataFrame({"a": [1, 2, 3]})

    with pytest.raises(KeyError, match="Missing columns in df"):
        infer_plot_scales(df, ["a", "missing"])

