# Predicting Potentially Hazardous Near-Earth Asteroids
Authors: Jerry Jin, Malcolm Maxwell, Sadie Lee

## About

The main goal of this project is to build a predictive model that classifies near-earth objects as potentially hazardous, specifically aiming to see if additional orbital and physical characteristics are associated with such prediction. We use the k-nearest neighbors algorithm using 4 orbital and physical variables from NASA JPL's Small-Body DataBase (SBDB) as predictors and focusing on the target binary variable `pha` (potentially hazardous asteroid) for classification. Additionally, we tune the model using cross-validation, and evaluate its performance with ROC-AUC, PR curves, confusion matrices, and threshold tuning. Note that the SBDB contains significant class imbalance between PHA and non-PHA near-earth objects, which led us to prioritize recall and reduce false negatives.

The data we used to build our model contains all near-earth asteroids and their characteristics collected from the NASA JPL Small-Body DataBase via the available API. Documentation of this database can be found at https://ssd-api.jpl.nasa.gov/doc/sbdb_query.html.

## Report

The main analysis, a Quarto report, can be found in `asteroid_analysis.qmd`. To render the report as either an HTML or PDF file, use the `Makefile` and run `make` in the terminal. Additionally it can be viewed as a Jupyter notebook in `notebooks/asteroid_analysis.ipynb`.

## Usage
### Run with Docker Compose 
A recommended way to run the project interactively requires Docker Desktop to be installed and running.
1. Clone the repository:
```bash
git clone https://github.com/UBC-DSCI-310-2025W2/dsci-310-group-18.git
cd dsci-310-group-18
```
2. Start the container:
```bash
docker compose up
```
3. Open the URL printed in the terminal (starting with http://127.0.0.1:8888/...) in your browser.
4. From a terminal inside the container use the following command to generate report in pdf and html:
```bash
cd ~/work
conda activate dsci310proj
make clean (optional)
make all
```
5. The rendered files `asteroid_analysis.html` and `asteroid_analysis.pdf` will be written to the repository root mounted at `~/work`. Open them from your host machine's file browser, or navigate to them in the Jupyter file browser launched by Docker.
6. When finished, stop the container with Ctrl+C, then:
```bash
docker compose down
```

## Dependencies
The project uses Python 3.12 and the Conda environment named `dsci310proj`.
Core dependencies are declared in `environment.yml` and locked in `conda-lock.yml`, including:

- `python=3.12`
- `pandas=3.0`
- `numpy=2.4.2`
- `matplotlib=3.10.8`
- `seaborn=0.13.2`
- `scikit-learn=1.8.0`
- `requests=2.32.5`
- `pandera=0.30.1`
- `pytest=9.0.2`
- `jupyterlab`

System tools required to reproduce the full analysis are:

- GNU Make
- Quarto
- Docker Desktop and Docker Compose for the containerized workflow

## License

This project is offered under the [Attribution 4.0 International (CC BY 4.0) License](https://creativecommons.org/licenses/by/4.0/). The software in this project is offered under the [MIT open source license](https://opensource.org/licenses/MIT). See [the license file](LICENSE.md) for more information. 
