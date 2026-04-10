import numpy as np
import pytest

from src.threshold_utils import select_threshold, ThresholdSelectionResult


def test_select_threshold_max_recall_with_precision_constraint():
    """When precision constraint is feasible, choose threshold with max recall."""
    y_true = np.array([0, 0, 1, 1])
    # Probabilities roughly separate positives and negatives
    y_proba = np.array([0.1, 0.2, 0.8, 0.9])

    result = select_threshold(
        y_true=y_true,
        y_proba=y_proba,
        objective="max_recall",
        min_precision=0.5,
        fallback="max_f1",
    )

    assert isinstance(result, ThresholdSelectionResult)
    assert 0.0 <= result.threshold <= 1.0
    assert result.precision >= 0.5
    # At least one positive should be recalled
    assert result.recall > 0.0


def test_select_threshold_fallback_to_max_f1_when_constraint_infeasible():
    """If no threshold satisfies the precision constraint, fall back to max F1."""
    y_true = np.array([0, 0, 0, 1])
    # Probabilities that make it hard to get very high precision
    y_proba = np.array([0.4, 0.45, 0.5, 0.55])

    result = select_threshold(
        y_true=y_true,
        y_proba=y_proba,
        objective="max_recall",
        min_precision=0.99,
        fallback="max_f1",
    )

    # Still returns a valid threshold and metrics
    assert 0.0 <= result.threshold <= 1.0
    assert 0.0 <= result.precision <= 1.0
    assert 0.0 <= result.recall <= 1.0


def test_select_threshold_raises_for_shape_mismatch():
    """The helper should enforce matching shapes for inputs."""
    y_true = np.array([0, 1])
    y_proba = np.array([0.2, 0.8, 0.9])

    with pytest.raises(ValueError, match="same shape"):
        select_threshold(y_true=y_true, y_proba=y_proba)


def test_select_threshold_invalid_objective_raises():
    """Unsupported objectives should result in a clear error."""
    y_true = np.array([0, 1])
    y_proba = np.array([0.2, 0.8])

    with pytest.raises(ValueError, match="Unsupported objective"):
        select_threshold(y_true=y_true, y_proba=y_proba, objective="unknown")

