from scipy.stats import randint

from src.get_knn_param_grid import get_knn_param_grid


def test_get_knn_param_grid_returns_expected_keys():
    """The parameter grid should expose all tuned KNN hyperparameters."""
    param_grid = get_knn_param_grid()

    assert set(param_grid.keys()) == {
        "knn__n_neighbors",
        "knn__weights",
        "knn__metric",
        "knn__p",
    }


def test_get_knn_param_grid_returns_expected_fixed_options():
    """The fixed option lists should match the training script design."""
    param_grid = get_knn_param_grid()

    assert param_grid["knn__weights"] == ["uniform", "distance"]
    assert param_grid["knn__metric"] == ["euclidean", "manhattan", "minkowski"]
    assert param_grid["knn__p"] == [1, 2]


def test_get_knn_param_grid_uses_expected_neighbor_distribution():
    """The neighbor distribution should span integers from 3 to 49."""
    param_grid = get_knn_param_grid()

    assert isinstance(param_grid["knn__n_neighbors"], type(randint(3, 50)))
    assert param_grid["knn__n_neighbors"].args == (3, 50)
