from scipy.stats import randint


def get_knn_param_grid():
    """
    Return the hyperparameter search space for the asteroid KNN model.

    Returns
    -------
    dict
        Dictionary of parameter distributions and option lists for
        ``RandomizedSearchCV``.
    """
    return {
        "knn__n_neighbors": randint(3, 50),
        "knn__weights": ["uniform", "distance"],
        "knn__metric": ["euclidean", "manhattan", "minkowski"],
        "knn__p": [1, 2],
    }
