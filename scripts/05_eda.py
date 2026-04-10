"""Create and save exploratory data analysis figures for the training set.

This command-line script generates the plots referenced in the Quarto report,
including histograms, a correlation heatmap, ECDFs, and KDE plots.

Example
-------
python scripts/05_eda.py \
    --train-data-path=data/processed/asteroid_train.csv \
    --save-plot-dir=results/figures
"""

import click
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math
from pathlib import Path

def make_histogram(df, fields, save_plot_path, scales=None, cols=3):
    """
    Create grid of histograms for quantitative variables
    """
    if scales is None:
        scales = {}

    n = len(fields)
    rows = math.ceil(n / cols)

    fig, axes = plt.subplots(rows, cols, figsize=(5*cols, 4*rows))
    axes = axes.flatten()

    for i, field in enumerate(fields):
        data = df[field].dropna()
        scale = scales.get(field, 'linear')

        if scale == 'log':
            axes[i].hist(data, bins=30, log=True)
            axes[i].set_yscale('log')
            axes[i].set_title(f"{field} - log")
        else:
            axes[i].hist(data, bins=30)
            axes[i].set_title(field)

        axes[i].set_ylabel("Frequency")

    # Remove empty subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.suptitle('Figure 1 - Variable Histograms', fontsize=16)
    plt.tight_layout()
    plt.savefig(save_plot_path)
    plt.close()

@click.command()
@click.option('--train-data-path', type=str, required=True, help='Filepath to preprocessed training data.')
@click.option('--save-plot-dir', type=str, required=True, help='Directory to save plots.')

def main(train_data_path, save_plot_dir):
    """Plots and saves univariate histograms, multivariate heatmap, ECDF, and KDE for EDA."""
    Path(save_plot_dir).mkdir(parents=True, exist_ok=True)
    
    scaled_asteroid_train = pd.read_csv(train_data_path)

    # Figure 1: Univariate histograms
    fields = [
        'min_orbit_intersection_dist',
        'epoch',
        'eccentricity',
        'semi_major_axis',
        'perihelion_dist',
        'inclination',
        'mean_anomaly',
        'time_of_perihelion_passage',
        'abs_magnitude'
    ]

    scales = {
        'min_orbit_intersection_dist': 'log',
        'epoch': 'log',
        'semi_major_axis': 'log',
        'inclination': 'log',
        'time_of_perihelion_passage': 'log'
    }

    make_histogram(
        scaled_asteroid_train, 
        fields,
        save_plot_path=f"{save_plot_dir}/01_eda-histogram.png",
        scales=scales
    )

    # Figure 2: Multivariate correlation heatmap
    data = scaled_asteroid_train.select_dtypes(include='number').drop(columns=['pha'])

    corr = data.corr()

    plt.figure(figsize=(7, 5))
    sns.heatmap(
        corr,
        annot=True,
        fmt='.2f',
        cmap='coolwarm',
        vmin=-1,
        vmax=1,
        linewidths=0.5,
        cbar_kws={'label': 'Correlation'}
    )

    plt.title("Figure 2 - Variable Correlation Heatmap")
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(f"{save_plot_dir}/02_eda-heatmap.png")
    plt.close()

    # Figure 3: ECDF plots
    grid_cols = 3
    n = len(data.columns)
    rows = (n + grid_cols - 1) // grid_cols

    fig, axes = plt.subplots(rows, grid_cols, figsize=(5*grid_cols, 4*rows))
    axes = axes.flatten()

    for i, col in enumerate(data.columns):
        sns.ecdfplot(
            data=scaled_asteroid_train,
            x=col,
            ax=axes[i]
        )
        axes[i].set_xlabel(col)
        axes[i].set_ylabel("ECDF")

    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.suptitle('Figure 3 - Variable ECDF Plots')
    plt.tight_layout()
    plt.savefig(f"{save_plot_dir}/03_eda-ecdf.png")
    plt.close()

    # Figure 4: KDE plots
    predictor_cols = data.columns.tolist()

    cols = 3
    n = len(predictor_cols)
    rows = math.ceil(n / cols)

    fig, axes = plt.subplots(rows, cols, figsize=(6*cols, 5*rows))
    axes = axes.flatten()

    for i, col in enumerate(predictor_cols):
        sns.kdeplot(
            data=scaled_asteroid_train,
            x=col,
            hue='pha',
            fill=True,
            common_norm=False,
            ax=axes[i]
        )
        axes[i].set_title(f"{col} distribution by PHA")

    # Remove any extra empty subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    # Formatting
    fig.suptitle("Figure 4 - Predictor Distribution by PHA Status", fontsize=16)
    plt.tight_layout()
    plt.savefig(f"{save_plot_dir}/04_eda-kde.png")
    plt.close()

if __name__ == '__main__':
    main()
