# Makefile

# This driver script runs the full analysis from start to finish. 
# It downloads the raw asteroid data, 
# cleans the data, 
# splits and preprocesses it, 
# creates figures, trains a KNN model, 
# evaluates the model on validation and test sets, 
# and renders the Quarto report as an HTML and PDF file. 

# Usage:
#   make all - creates HTML and pdf PDF processing/running data, eda, model, and evaluation
#   make html - renders only the HTML file
#   make pdf - renders only the PDF file
#   make clean - removes all generated data files, figures, tables, models, and reports

.PHONY: all data eda model eval html pdf clean

all: asteroid_analysis.html asteroid_analysis.pdf

html: asteroid_analysis.html

pdf: asteroid_analysis.pdf

data: data/raw/asteroid_data_raw.csv \
	data/clean/asteroid_data_clean.csv \
	data/processed/asteroid_train.csv \
	data/processed/asteroid_val.csv \
	data/processed/asteroid_test.csv \
	data/processed/robust_scaler.pkl

eda: results/figures/01_eda-histogram.png \
	results/figures/02_eda-heatmap.png \
	results/figures/03_eda-ecdf.png \
	results/figures/04_eda-kde.png

model: results/models/best_knn_model.pkl \
	results/tables/model_results.csv \
	results/tables/best_params.txt

eval: results/figures/05_val-confusion-matrix.png \
	results/figures/06_val-pr-curve.png \
	results/figures/07_test-confusion-matrix.png \
	results/figures/08_recall-at-k.png \
	results/figures/09_prob-dist.png \
	results/tables/validation_metrics.txt \
	results/tables/best_threshold.txt \
	results/tables/test_metrics.txt

# html file
asteroid_analysis.html: asteroid_analysis.qmd references.bib data eda model eval
	quarto render asteroid_analysis.qmd --to html

# pdf file
asteroid_analysis.pdf: asteroid_analysis.qmd references.bib data eda model eval
	quarto render asteroid_analysis.qmd --to pdf

# raw data from NASA JPL SBDB API
data/raw/asteroid_data_raw.csv: scripts/01_fetch-data.py
	python scripts/01_fetch-data.py \
		--read-url="https://ssd-api.jpl.nasa.gov/sbdb_query.api" \
		--write-path=data/raw/asteroid_data_raw.csv

# clean raw data
data/clean/asteroid_data_clean.csv: scripts/02_clean-data.py data/raw/asteroid_data_raw.csv
	mkdir -p data/clean
	python scripts/02_clean-data.py \
		--raw-data-path=data/raw/asteroid_data_raw.csv \
		--clean-data-path=data/clean/asteroid_data_clean.csv

# preprocess data
data/processed/asteroid_train.csv \
data/processed/asteroid_val.csv \
data/processed/asteroid_test.csv \
data/processed/robust_scaler.pkl: scripts/03_split-data.py data/clean/asteroid_data_clean.csv
	mkdir -p data/processed
	python scripts/03_split-data.py \
		--clean-data-path=data/clean/asteroid_data_clean.csv \
		--output-dir=data/processed 

# eda
results/figures/01_eda-histogram.png \
results/figures/02_eda-heatmap.png \
results/figures/03_eda-ecdf.png \
results/figures/04_eda-kde.png: scripts/04_eda.py data/processed/asteroid_train.csv
	mkdir -p results/figures
	python scripts/04_eda.py \
		--train-data-path=data/processed/asteroid_train.csv \
		--save-plot-dir=results/figures

# train tuned KNN model
results/models/best_knn_model.pkl \
results/tables/model_results.csv \
results/tables/best_params.txt: scripts/05_train-model.py data/processed/asteroid_train.csv data/processed/robust_scaler.pkl
	mkdir -p results/models results/tables
	python scripts/05_train-model.py \
		--train-data-path=data/processed/asteroid_train.csv \
		--preprocessor-path=data/processed/robust_scaler.pkl \
		--results-dir=results \
		--model-path=results/models/best_knn_model.pkl 

# evaluate on validation and test sets
results/figures/05_val-confusion-matrix.png \
results/figures/06_val-pr-curve.png \
results/figures/07_test-confusion-matrix.png \
results/figures/08_recall-at-k.png \
results/figures/09_prob-dist.png \
results/tables/validation_metrics.txt \
results/tables/best_threshold.txt \
results/tables/test_metrics.txt: scripts/06_eval-predict.py data/processed/asteroid_val.csv data/processed/asteroid_test.csv results/models/best_knn_model.pkl
	mkdir -p results/figures results/tables
	python scripts/06_eval-predict.py \
		--val-data-path=data/processed/asteroid_val.csv \
		--test-data-path=data/processed/asteroid_test.csv \
		--model-path=results/models/best_knn_model.pkl \
		--plot-dir=results/figures \
		--table-dir=results/tables

# make clean
clean:
	rm -f data/raw/asteroid_data_raw.csv \
		data/clean/asteroid_data_clean.csv \
		data/processed/asteroid_train.csv \
		data/processed/asteroid_val.csv \
		data/processed/asteroid_test.csv \
		data/processed/robust_scaler.pkl \
		results/figures/01_eda-histogram.png \
		results/figures/02_eda-heatmap.png \
		results/figures/03_eda-ecdf.png \
		results/figures/04_eda-kde.png \
		results/figures/05_val-confusion-matrix.png \
		results/figures/06_val-pr-curve.png \
		results/figures/07_test-confusion-matrix.png \
		results/figures/08_recall-at-k.png \
		results/figures/09_prob-dist.png \
		results/models/best_knn_model.pkl \
		results/tables/model_results.csv \
		results/tables/best_params.txt \
		results/tables/validation_metrics.txt \
		results/tables/best_threshold.txt \
		results/tables/test_metrics.txt \
		asteroid_analysis.html \
		asteroid_analysis.pdf