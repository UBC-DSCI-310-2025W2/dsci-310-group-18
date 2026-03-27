from scipy.stats import randint


def get_knn_param_grid():
    """
    Creates the hyperparameter grid for tuning the KNN classifier.

    Parameters:
    ----------
    None

    Returns:
    -------
    dict
        A dictionary containing the KNN hyperparameter search space.

    Examples:
    --------
    >>> param_grid = get_knn_param_grid()
    >>> print(param_grid["knn__weights"])

    Notes:
    -----
    This function defines the search space used by RandomizedSearchCV
    when tuning the KNN model in the training script.
    """
    return {
        "knn__n_neighbors": randint(3, 50),
        "knn__weights": ["uniform", "distance"],
        "knn__metric": ["euclidean", "manhattan", "minkowski"],
        "knn__p": [1, 2],
    }
