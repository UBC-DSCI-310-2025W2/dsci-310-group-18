**Predicting Potentially Hazardous Near-Earth Asteroids**
Authors: Jerry Jin, Malcolm Maxwell, Sadie Lee
**About**
This project uses machine learning to predict potentially hazardous near-earth asteroids (PHAs) using NASA's Small-Body DataBase (SBDB).
Report
The analysis notebook can be found at notebooks/asteroid_analysis.ipynb.

**Usage**
**Option 1: Run with Docker Compose (Recommended)**
The simplest way to run the project. Requires Docker Desktop to be installed and running.
Step 1: Clone the repository:
bash
git clone https://github.com/UBC-DSCI-310-2025W2/dsci-310-group-18.git
cd dsci-310-group-18
Step 2: Start the container:
bash
docker compose up
Step 3: Open the URL printed in the terminal (starting with http://127.0.0.1:8888/...) in your browser.
Step 4: Navigate to work/notebooks/asteroid_analysis.ipynb and run all cells via Kernel → Restart Kernel and Run All Cells.
Step 5: When finished, stop the container with Ctrl+C, then:
bashdocker compose down

**Option 2: Build Docker Image Locally and Run**
Use this if you want to build the image from source rather than pulling from DockerHub. Requires Docker Desktop.
Step 1: Clone the repository:
bash 
git clone https://github.com/UBC-DSCI-310-2025W2/dsci-310-group-18.git
cd dsci-310-group-18
Step 2: Build the image locally:
bash
docker build -t dsci-310-group-18 .

Note: This may take 5–10 minutes as it installs all dependencies.

Step 3: Run the container:
bashdocker run --rm -p 8888:8888 -v "$(pwd)":/home/jovyan/work dsci-310-group-18
Step 4: Open the URL printed in the terminal (starting with http://127.0.0.1:8888/...) in your browser.
Step 5: Navigate to work/notebooks/asteroid_analysis.ipynb and run all cells via Kernel → Restart Kernel and Run All Cells.

**Option 3: Run Locally with Conda**
Use this if you prefer not to use Docker. Requires conda and conda-lock to be installed.
Step 1: Clone the repository:
bash
git clone https://github.com/UBC-DSCI-310-2025W2/dsci-310-group-18.git
cd dsci-310-group-18
Step 2: Install conda-lock if not already installed:
bash
conda install -n base conda-forge::conda-lock
Step 3: Create and activate the environment:
bash
conda-lock install --name dsci310proj conda-lock.yml
conda activate dsci310proj
Step 4: Launch Jupyter Lab:
bash
jupyter lab
Step 5: Open notebooks/asteroid_analysis.ipynb and run all cells via Kernel → Restart Kernel and Run All Cells.

**Dependencies**
All dependencies are pinned in conda-lock.yml and defined in environment.yml:
PackageVersionpython3.12pandas3.0numpy2.4.2scipy1.17.0matplotlib3.10.8seaborn0.13.2scikit-learn1.8.0requests2.32.5ipykernel7.1conda-lock4.0
**License**
This project is offered under the Attribution 4.0 International (CC BY 4.0) License. The software in this project is offered under the MIT open source license. See the license file for more information.