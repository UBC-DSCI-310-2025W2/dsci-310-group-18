from scipy.stats import randint


def get_knn_param_grid():
    """
    Return the project's KNN hyperparameter search space.

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
    This helper returns a static search space on purpose: it keeps the tuning
    configuration in one place so the training script and tests share the same
    expected parameter grid.
    """
    return {
        "knn__n_neighbors": randint(3, 50),
        "knn__weights": ["uniform", "distance"],
        "knn__metric": ["euclidean", "manhattan", "minkowski"],
        "knn__p": [1, 2],
    }
