# Use the mambaforge image from conda-forge
FROM condaforge/mambaforge:latest

# Set the working directory in the container
WORKDIR /streamlit-app

# Copy the environment.yml file into the container
COPY environment.yml .

# Create the Conda environment using mamba
RUN mamba env create -f environment.yml && \
    mamba clean --all --yes

# Set the default shell to use bash
SHELL ["/bin/bash", "-c"]

# Copy the rest of the application code into the container
COPY . .

# Expose the port that Streamlit will run on
EXPOSE 8501

# Command to run the Streamlit app
CMD ["bash", "-c", "source activate myenv && streamlit run app.py"]