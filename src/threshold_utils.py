"""Helpers for selecting decision thresholds from predicted probabilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
from sklearn.metrics import precision_recall_curve


@dataclass
class ThresholdSelectionResult:
    threshold: float
    precision: float
    recall: float
    objective: str
    min_precision: float


def select_threshold(
    y_true,
    y_proba,
    objective: Literal["max_recall", "max_f1"] = "max_recall",
    min_precision: float = 0.5,
    fallback: Literal["max_f1", "default"] = "max_f1",
) -> ThresholdSelectionResult:
    """Select a classification threshold from predicted probabilities.

    This helper encapsulates the threshold-selection logic used in evaluation:

    - For ``objective='max_recall'`` it chooses the threshold with the
      highest recall subject to ``precision >= min_precision``.
    - If no threshold satisfies the precision constraint, a fallback strategy
      is applied:
        * ``'max_f1'``: choose the threshold with maximum F1-score
        * ``'default'``: fall back to a conventional 0.5 threshold

    Parameters
    ----------
    y_true, y_proba:
        1D array-like of true binary labels and predicted probabilities.
    objective:
        Primary optimization objective. Currently supports ``'max_recall'``
        and ``'max_f1'``.
    min_precision:
        Minimum precision required when ``objective='max_recall'``.
    fallback:
        Strategy to use when no threshold satisfies ``min_precision``.

    Returns
    -------
    ThresholdSelectionResult
        Dataclass with the chosen threshold and associated precision/recall.

    Raises
    ------
    ValueError
        If the inputs have incompatible shapes or an unsupported objective
        or fallback strategy is requested.
    """
    y_true_arr = np.asarray(y_true)
    y_proba_arr = np.asarray(y_proba)

    if y_true_arr.shape != y_proba_arr.shape:
        raise ValueError("y_true and y_proba must have the same shape")

    precision, recall, thresholds = precision_recall_curve(y_true_arr, y_proba_arr)

    # thresholds has length N-1 corresponding to precision[:-1], recall[:-1]
    prec = precision[:-1]
    rec = recall[:-1]
    thr = thresholds

    if objective not in {"max_recall", "max_f1"}:
        raise ValueError(f"Unsupported objective: {objective}")

    if fallback not in {"max_f1", "default"}:
        raise ValueError(f"Unsupported fallback strategy: {fallback}")

    chosen_idx: int

    if objective == "max_recall":
        valid = prec >= min_precision
        if valid.any():
            # Among thresholds satisfying the precision constraint,
            # pick the one with highest recall.
            constrained_rec = rec[valid]
            chosen_idx = np.argmax(constrained_rec)
            # Map back into the full threshold index space
            chosen_idx = np.nonzero(valid)[0][chosen_idx]
        else:
            # Apply fallback strategy when the constraint is infeasible.
            if fallback == "max_f1":
                f1 = 2 * prec * rec / (prec + rec + 1e-12)
                chosen_idx = int(np.argmax(f1))
            else:  # fallback == "default"
                # Choose the threshold closest to 0.5
                chosen_idx = int(np.argmin(np.abs(thr - 0.5)))
    else:  # objective == "max_f1"
        f1 = 2 * prec * rec / (prec + rec + 1e-12)
        chosen_idx = int(np.argmax(f1))

    chosen_threshold = float(thr[chosen_idx])
    chosen_precision = float(prec[chosen_idx])
    chosen_recall = float(rec[chosen_idx])

    return ThresholdSelectionResult(
        threshold=chosen_threshold,
        precision=chosen_precision,
        recall=chosen_recall,
        objective=objective,
        min_precision=min_precision,
    )

