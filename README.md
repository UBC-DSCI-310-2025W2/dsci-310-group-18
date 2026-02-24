# Predicting Potentially Hazardous Near-Earth Asteroids

Authors: Jerry Jin, Malcolm Maxwell, Sadie Lee

## About

## Report

## Usage

This project uses `conda-lock` for Docker. Install using: 
```bash
conda-lock install --name YOURENV conda-lock.yml
```
### Running with Docker (Recommended)
This project's computation environment is containerized using Docker. To run the analysis and develop collaboratively:

1. **Build the Docker image:**
   Navigate to the root of this repository and run:
   ```bash
   docker build -t dsci-310-group-18 .

2. **Run Docker**
    docker run --rm -p 8888:8888 -v "$(pwd):/home/jovyan/work" zheqijin/dsci-310-group-18:latest jupyter lab   
Open the URL provided in the terminal (starting with http://127.0.0.1:8888/lab) in your browser to access the notebooks.

3.  **Running Locally (Without Docker)**
If you prefer not to use Docker, you can install the environment locally using conda-lock:

Bash
conda-lock install --name dsci310proj conda-lock.yml
conda activate dsci310proj
jupyter lab 
## Dependencies

## License

This project is offered under the [Attribution 4.0 International (CC BY 4.0) License](https://creativecommons.org/licenses/by/4.0/). The software in this project is offered under the [MIT open source license](https://opensource.org/licenses/MIT). See [the license file](LICENSE.md) for more information. 