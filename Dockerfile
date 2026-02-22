# 1. Base Image
FROM quay.io/jupyter/minimal-notebook:2024-02-24

# 2. Copy the lockfile into the container
COPY conda-lock.yml /tmp/conda-lock.yml

# 3. Install dependencies into a NEW environment named dsci310proj
RUN conda install -y conda-lock && \
    conda-lock install --name dsci310proj /tmp/conda-lock.yml && \
    conda clean -afy

# 4. Register the new environment as a Jupyter kernel
RUN /opt/conda/envs/dsci310proj/bin/python -m ipykernel install --user --name python3 --display-name "Python (dsci310proj)"

# 5. Set the new environment as the default path
ENV PATH=/opt/conda/envs/dsci310proj/bin:$PATH

#test auto build