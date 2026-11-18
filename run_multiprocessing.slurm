#!/bin/sh

#SBATCH --job-name=python-multiprocessing
#SBATCH --partition=batch
#SBATCH --reservation=root_1    # Reserved nodes for this class (don't add this normally)
#SBATCH --time=00:05:00     # Maximum run time
#SBATCH --nodes=1           # Run on just 1 node
#SBATCH --ntasks=1          # Run one instance of the script
#SBATCH --cpus-per-task=64  # Use 64 multiprocessing Python workers/cores

# Optional: print useful job info
echo "Running on host: $(hostname)"
echo "Job started at: $(date)"
echo "SLURM job ID: $SLURM_JOB_ID"
echo "Number of CPUs: $SLURM_CPUS_PER_TASK"

# Load required modules
module purge
module load python

# Move to job directory
cd $SLURM_SUBMIT_DIR

# activate the Python environment
source venv/bin/activate

# run the code (disable progress bar when running batch)
TQDM_DISABLE=1 python augment_images_multiprocessing.py

# Clean-up
deactivate
module purge
