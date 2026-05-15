#!/bin/bash
# job.sh
# Runs all project notebooks sequentially using the vol-regime conda environment.
# Creates the environment from environment.yaml if it doesn't already exist.

set -e  # Exit immediately on any error

ENV_NAME="vol-regime"
NOTEBOOKS_DIR="notebooks"
LOG_DIR="logs"



echo -e "Volatility Regime Detection Pipeline"

#Create or verify conda environment
echo -e "\nChecking conda environment ${ENV_NAME}"

if conda env list | grep -q "^${ENV_NAME} "; then
    echo -e "Environment '${ENV_NAME}' already exists"
else
    echo -e "  Environment not found. Creating from environment.yaml"
    conda env create -f environment.yaml
    echo -e "Environment '${ENV_NAME}' created successfully"
fi

# Activate environment
conda activate "$ENV_NAME"
echo -e "Environment '${ENV_NAME}' activated"

# Register as Jupyter kernel (idempotent — safe to run repeatedly)
python -m ipykernel install --user --name "$ENV_NAME" --display-name "$ENV_NAME" 2>/dev/null
echo -e "Jupyter kernel registered"

#Create log directory
mkdir -p "$LOG_DIR"
mkdir -p "data/raw" "data/processed" "plots" "models"

#download raw data
python data.py

echo -e "\nRunning notebooks"

NOTEBOOKS=(
    "preprocessing_eda.ipynb"
    "garch_baseline.ipynb"
    "feature_engineering.ipynb"
    "lstm_model.ipynb"
    "walk_forward_cv.ipynb"
    "comparison_analysis.ipynb"
)

TOTAL=${#NOTEBOOKS[@]}
PASSED=0
FAILED=0
FAILED_LIST=()

for i in "${!NOTEBOOKS[@]}"; do
    NB="${NOTEBOOKS[$i]}"
    NB_PATH="${NOTEBOOKS_DIR}/${NB}"
    LOG_FILE="${LOG_DIR}/${NB%.ipynb}.log"
    NUM=$((i + 1))

    echo -e "\n  [${NUM}/${TOTAL}] Running: ${NB}"

    if [ ! -f "$NB_PATH" ]; then
        echo -e "File not found: ${NB_PATH} — skipping"
        FAILED=$((FAILED + 1))
        FAILED_LIST+=("$NB (not found)")
        continue
    fi

    START_TIME=$(date +%s)

    # Execute notebook in-place, saving output back to the same file
    # --kernel matches our registered kernel name
    # stderr goes to log file for debugging
    if jupyter nbconvert \
        --to notebook \
        --execute \
        --inplace \
        --ExecutePreprocessor.kernel_name="$ENV_NAME" \
        --ExecutePreprocessor.timeout=3600 \
        "$NB_PATH" \
        > "$LOG_FILE" 2>&1; then

        END_TIME=$(date +%s)
        ELAPSED=$((END_TIME - START_TIME))
        echo -e "Done in ${ELAPSED}s: output saved to ${NB_PATH}${NC}"
        PASSED=$((PASSED + 1))
    else
        END_TIME=$(date +%s)
        ELAPSED=$((END_TIME - START_TIME))
        echo -e "FAILED after ${ELAPSED}s: see ${LOG_FILE} for details${NC}"
        FAILED=$((FAILED + 1))
        FAILED_LIST+=("$NB")
        break
    fi
done


echo -e "Done!"