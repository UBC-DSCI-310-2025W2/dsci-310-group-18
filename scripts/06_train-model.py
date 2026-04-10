"""Tune and train the KNN classifier used in the asteroid analysis.

This command-line script loads the processed training data, runs randomized
cross-validation over the KNN search space, and saves the fitted model and
training artifacts.

Example
-------
python scripts/06_train-model.py \
    --train-data-path=data/processed/asteroid_train.csv \
    --preprocessor-path=data/processed/robust_scaler.pkl \
    --results-dir=results \
    --model-path=results/models/best_knn_model.pkl
"""

import click
import pandas as pd
import os
import joblib
from sklearn.pipeline import Pipeline
from sklearn.model_selection import RandomizedSearchCV
from sklearn.neighbors import KNeighborsClassifier
from asteroidprep import get_knn_param_grid, drop_columns

@click.command()
@click.option('--train-data-path', type=str, required=True, help='Filepath to training data csv.')
@click.option('--preprocessor-path', type=str, required=True, help='Filepath to preprocessor object.')
@click.option('--results-dir', type=str, required=True, help='Output directory to write result objects.')
@click.option('--model-path', type=str, required=True, help='Output path to write best model object.')
@click.option('--seed', type=int,  default=123, help='Random seed for reproducibility.')

def main(train_data_path, preprocessor_path, results_dir, model_path, seed):
    """Fits a binary KNN classifier to the asteroid training data and 
    saves the pipeline object."""
    os.makedirs(results_dir, exist_ok=True)

    # Read in data and preprocessor
    asteroid_train = pd.read_csv(train_data_path)
    asteroid_preprocessor = joblib.load(preprocessor_path)

    # Feature selection
    drop_cols = [
        'min_orbit_intersection_dist',
        'abs_magnitude',
        'epoch',
        'semi_major_axis',
        'time_of_perihelion_passage'
    ]
    asteroid_train = drop_columns(asteroid_train, drop_cols)

    # Instantiate model and pipeline objects
    knn = KNeighborsClassifier()
    asteroid_tune_pipe = Pipeline([
        ("scaler", asteroid_preprocessor),
        ("knn", knn)
    ])

    # Parameters
    param_dict = get_knn_param_grid()

    # 5-fold random search CV
    random_search = RandomizedSearchCV(
        asteroid_tune_pipe,
        param_distributions=param_dict,
        n_iter=50,
        cv=5,
        scoring="roc_auc",
        n_jobs=-1,
        random_state=seed,
        verbose=2
    )

    asteroid_fit = random_search.fit(
        asteroid_train.drop(columns=['pha']),
        asteroid_train["pha"]
    )

    # Save objects
    results = pd.DataFrame(random_search.cv_results_)
    results.to_csv(f"{results_dir}/tables/model_results.csv", index=False)

    best_params = random_search.best_params_
    with open(f"{results_dir}/tables/best_params.txt", "w") as f:
        f.write(str(best_params))
    
    best_model = random_search.best_estimator_
    with open(model_path, "wb") as f:
        joblib.dump(best_model, f)

if __name__ == '__main__':
    main()
