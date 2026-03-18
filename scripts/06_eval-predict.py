# 06_eval-predict.py
# author: Sadie Lee
# date: 2026-03-16

import click
import pandas as pd
import numpy as np
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix, ConfusionMatrixDisplay, precision_recall_curve, average_precision_score

@click.command()
@click.option('--val-data-path', type=str, required=True, help='Filepath to validation data.')
@click.option('--test-data-path', type=str, required=True, help='Filepath to test data.')
@click.option('--model-path', type=str, required=True, help='Filepath to best model object.')
@click.option('--plot-dir', type=str, required=True, help='Output directory for figures.')
@click.option('--table-dir', type=str, required=True, help='Output directory for results.')

def main(val_data_path, test_data_path, model_path, plot_dir, table_dir):
    """Performs evaluation on the validation set 
    and prediction on the test set, 
    and plots/saves results."""
    os.makedirs(plot_dir, exist_ok=True)
    os.makedirs(table_dir, exist_ok=True)

    # Read in model object
    model = joblib.load(model_path)

    # Split X and y
    val = pd.read_csv(val_data_path)
    test = pd.read_csv(test_data_path)

    X_val = val.drop(columns=['pha', 'abs_magnitude', 'epoch', 'min_orbit_intersection_dist', 'semi_major_axis', 'time_of_perihelion_passage'])
    y_val = val['pha']

    X_test = test.drop(columns=['pha', 'abs_magnitude', 'epoch', 'min_orbit_intersection_dist', 'semi_major_axis', 'time_of_perihelion_passage'])
    y_test = test['pha']

    # Validation evaluation
    y_val_pred = model.predict(X_val)
    y_val_proba = model.predict_proba(X_val)[:,1]

    val_auc = roc_auc_score(y_val, y_val_proba)
    val_report = classification_report(y_val, y_val_pred)

    with open(f"{table_dir}/validation_metrics.txt","w") as f:
        f.write(f"AUC: {val_auc}\n\n")
        f.write(val_report)

    confmat_val = confusion_matrix(y_val, y_val_pred)
    ConfusionMatrixDisplay(confmat_val, display_labels=["Non-PHA", "PHA"]).plot(cmap="Blues")
    plt.title("Figure 5 - Validation Confusion Matrix")
    plt.savefig(f"{plot_dir}/05_val-confusion-matrix.png")
    plt.close()

    precision, recall, thresholds = precision_recall_curve(y_val, y_val_proba)
    avg_prec = average_precision_score(y_val, y_val_proba)

    plt.figure(figsize=(6, 6))
    plt.plot(recall, precision, label=f"AP={avg_prec:.3f}")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Figure 6 - Precision-Recall Curve (Val)")
    plt.legend()
    plt.savefig(f"{plot_dir}/06_val-pr-curve.png")
    plt.close()

    # Threshold selection
    min_precision = 0.5
    valid = precision[:-1] >= min_precision
    best_idx = np.argmax(recall[:-1][valid])
    best_thresh = thresholds[valid][best_idx]
    
    with open(f"{table_dir}/best_threshold.txt", "w") as f:
        f.write(f"best_threshold={best_thresh}\n")
        f.write(f"min_precision={min_precision}\n")

    # Test predictions with threshold
    y_test_pred = model.predict(X_test)
    y_test_proba = model.predict_proba(X_test)[:,1]
    y_test_thresh = (y_test_proba >= best_thresh).astype(int)

    test_auc = roc_auc_score(y_test, y_test_proba)
    test_report = classification_report(y_test, y_test_thresh)
    with open(f"{table_dir}/test_metrics.txt", "w") as f:
        f.write(f"AUC: {test_auc}\n\n")
        f.write(test_report)

    confmat_test = confusion_matrix(y_test, y_test_thresh)
    ConfusionMatrixDisplay(confmat_test, display_labels=["Non-PHA", "PHA"]).plot(cmap="Blues")
    plt.title("Figure 7 - Test Confusion Matrix")
    plt.savefig(f"{plot_dir}/07_test-confusion-matrix.png")
    plt.close()

    # Recall@K curve 
    sorted_idx = np.argsort(-y_test_proba)
    sorted_y = y_test.values[sorted_idx]

    k_vals = np.arange(1, len(sorted_y)+1)
    recall_at_k = np.cumsum(sorted_y) / sorted_y.sum()

    plt.figure()
    plt.plot(k_vals, recall_at_k)
    plt.xlabel("Top K asteroids")
    plt.ylabel("Recall@K")
    plt.title("Figure 8 - Recall@K Curve")
    plt.savefig(f"{plot_dir}/08_recall-at-k.png")
    plt.close()

    # Probability distributions
    plt.figure(figsize=(12, 5))
    sns.kdeplot(y_test_proba[y_test==0], label='Non-PHA', fill=True)
    sns.kdeplot(y_test_proba[y_test==1], label='PHA', fill=True)
    plt.xlabel("Predicted Probability")
    plt.title("Figure 9 - Predicted Probability Distributions by Class")
    plt.legend()
    plt.savefig(f"{plot_dir}/09_prob-dist.png")
    plt.close()

if __name__ == '__main__':
    main()