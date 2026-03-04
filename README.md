# Predicting Potentially Hazardous Near-Earth Asteroids
Authors: Jerry Jin, Malcolm Maxwell, Sadie Lee

## About

We attempt to build a binary classification model using the k-nearest neighbors algorithm to predict potentially hazardous near-earth asteroids from orbital and physical characteristics including eccentricity, perihelion distance, and inclination. This model could provide the detection of potential risks in order to provide timely intervention. The current model achieves a test set AUC (area under the curve) of $0.9972$. Precision could be improved particularly for near-earth asteroids labeled as potentially hazardous. 

The data we used to build our model contains all near-earth asteroids and their characteristics collected from the NASA JPL Small-Body DataBase (SBDB) via the available API. Documentation of this database can be found at https://ssd-api.jpl.nasa.gov/doc/sbdb_query.html.

## Report

The analysis report can be found in `notebooks/asteroid_analysis.ipynb`. 

## Usage
This project uses `conda-lock` for Docker. Install using: 
```bash
conda-lock install --name YOURENV conda-lock.yml
```
### Running with Docker (Recommended)
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

3.  **Running Locally (Without Docker)**
If you prefer not to use Docker, you can install the environment locally using conda-lock:

    ```bash
    conda-lock install --name dsci310proj conda-lock.yml
    conda activate dsci310proj
    jupyter lab 
    ```
## Dependencies
Python version 3.12. Jupyter and Python packages can be found in `environment.yml`. 

## License

This project is offered under the [Attribution 4.0 International (CC BY 4.0) License](https://creativecommons.org/licenses/by/4.0/). The software in this project is offered under the [MIT open source license](https://opensource.org/licenses/MIT). See [the license file](LICENSE.md) for more information. 