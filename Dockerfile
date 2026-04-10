# 1. Base Image
FROM quay.io/jupyter/minimal-notebook:2024-02-24

ARG TARGETARCH
ARG QUARTO_VERSION=1.8.27

# 2. Copy the lockfile into the container
COPY conda-lock.yml /tmp/conda-lock.yml

# 3. Install dependencies into a new isolated environment
RUN conda install -y conda-lock && \
    conda-lock install --name dsci310proj /tmp/conda-lock.yml && \
    conda install -y -n dsci310proj pip nbformat nbclient && \
    /opt/conda/envs/dsci310proj/bin/python -c "import pip, nbformat, nbclient, pandera" && \
    conda clean -afy

# 4. Register the new environment to overwrite the default kernel
RUN /opt/conda/envs/dsci310proj/bin/python -m ipykernel install --user --name python3 --display-name "Python (dsci310proj)"

ENV PATH=/opt/conda/envs/dsci310proj/bin:$PATH
ENV QUARTO_PYTHON=/opt/conda/envs/dsci310proj/bin/python

# 4b. Default interactive shells to the project env
# (The Jupyter base image often activates `base` in interactive shells.)
USER root
RUN printf '%s\n' \
    'case "$-" in' \
    '  *i*)' \
    '    if [ -f /opt/conda/etc/profile.d/conda.sh ]; then' \
    '      . /opt/conda/etc/profile.d/conda.sh' \
    '      conda activate dsci310proj >/dev/null 2>&1 || true' \
    '    fi' \
    '  ;;' \
    'esac' \
  > /etc/profile.d/activate-dsci310proj.sh && \
  chmod 0644 /etc/profile.d/activate-dsci310proj.sh && \
  printf '\n%s\n' '. /etc/profile.d/activate-dsci310proj.sh' >> /etc/bash.bashrc

# 5. Install a pinned Quarto release for the target architecture
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    make \
    lmodern \
    texlive-luatex && \
    rm -rf /var/lib/apt/lists/*

RUN if [ "$TARGETARCH" = "arm64" ]; then QUARTO_ARCH="arm64"; \
    elif [ "$TARGETARCH" = "amd64" ]; then QUARTO_ARCH="amd64"; \
    else echo "Unsupported architecture: $TARGETARCH" && exit 1; \
    fi && \
    curl -LO "https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-${QUARTO_ARCH}.deb" && \
    dpkg -i "quarto-${QUARTO_VERSION}-linux-${QUARTO_ARCH}.deb" && \
    rm "quarto-${QUARTO_VERSION}-linux-${QUARTO_ARCH}.deb"
USER ${NB_UID}
 
 
