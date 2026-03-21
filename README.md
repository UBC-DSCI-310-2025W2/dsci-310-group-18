# Predicting Potentially Hazardous Near-Earth Asteroids
Authors: Jerry Jin, Malcolm Maxwell, Sadie Lee

## About

The main goal of this project is to build a predictive model that classifies near-earth objects as potentially hazardous, specifically aiming to see if additional orbital and physical characteristics are associated with such prediction. We use the k-nearest neighbors algorithm using 4 orbital and physical variables from NASA JPL's Small-Body DataBase (SBDB) as predictors and focusing on the target binary variable `pha` (potentially hazardous asteroid) for classification. Additionally, we tune the model using cross-validation, and evaluate its performance with ROC-AUC, PR curves, confusion matrices, and threshold tuning. Note that the SBDB contains significant class imbalance between PHA and non-PHA near-earth objects, which led us to prioritize recall and reduce false negatives.

The data we used to build our model contains all near-earth asteroids and their characteristics collected from the NASA JPL Small-Body DataBase via the available API. Documentation of this database can be found at https://ssd-api.jpl.nasa.gov/doc/sbdb_query.html.

## Report

The main analysis, a Quarto report, can be found in `asteroid_analysis.qmd`. To render the report as either an HTML or PDF file, use the `Makefile` and run `make` in the terminal. Additionally it can be viewed as a Jupyter notebook in `notebooks/asteroid_analysis.ipynb`.

## Usage
### Run the driver script (Recommended)
The simplest way to run the analysis pipeline involves a driver script, the `Makefile`, which lives in the root directory.
1. Clone the repository:
```bash
git clone https://github.com/UBC-DSCI-310-2025W2/dsci-310-group-18.git
cd dsci-310-group-18
```
2. From the root directory, run the driver script to process the full workflow and render both an HTML and PDF report:
```
make all
```
Or, to simply produce a PDF report:
```
make pdf
```
OR, to produce just an HTML report:
```
make html
```
3. Remove all generated outputs (optional)
```
make clean
```


### Run with Docker Compose 
An alternative way to run the project interactively requires Docker Desktop to be installed and running.
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
4. Navigate to work/notebooks/asteroid_analysis.ipynb and run all cells via Kernel → Restart Kernel and Run All Cells.
   The Quarto report source is at `work/asteroid_analysis.qmd`. From a terminal inside the container, run `cd ~/work && quarto render asteroid_analysis.qmd`.
5. When finished, stop the container with Ctrl+C, then:
```bash
docker compose down
```

### Running with Docker locally
This project uses `conda-lock` for Docker. Install using: 
```bash
conda-lock install --name YOURENV conda-lock.yml
```

This project's computation environment is containerized using Docker. We use a Docker container image to make the computational environment for this project reproducible. To run the analysis and develop collaboratively:

1. **Build the Docker image:**
   Navigate to the root of this repository and run:
   ```bash
   docker build -t dsci-310-group-18 .
   ```

2. **Run Docker**
    ```bash
    docker run --rm -p 8888:8888 -v "$(pwd):/home/jovyan/work" dsci-310-group-18 jupyter lab   
    ```
Open the URL provided in the terminal (starting with http://127.0.0.1:8888/lab) in your browser to access the notebooks.
To render the Quarto report in the container shell, use `cd ~/work && quarto render asteroid_analysis.qmd`.

3.  **Running Locally (Without Docker)**
If you prefer not to use Docker, you can install the environment locally using conda-lock:

    ```bash
    conda-lock install --name dsci310proj conda-lock.yml
    conda activate dsci310proj
    jupyter lab 
    ```
## Dependencies
Python version 3.12. Jupyter and Python packages can be found in `environment.yml`. 
The locked environment can be found in `conda-lock.yml`. 
GNU Make and Quarto are also required to run the full analysis and render the reports.

## License

This project is offered under the [Attribution 4.0 International (CC BY 4.0) License](https://creativecommons.org/licenses/by/4.0/). The software in this project is offered under the [MIT open source license](https://opensource.org/licenses/MIT). See [the license file](LICENSE.md) for more information. 
