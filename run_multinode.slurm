#!/bin/bash

#SBATCH --job-name=simple-multinode-example
#SBATCH --partition=batch
#SBATCH --reservation=root_1    # Reserved nodes for this class (don't add this normally)
#SBATCH --time=00:05:00
#SBATCH --nodes=2
#SBATCH --ntasks=64
#SBATCH --tasks-per-node=32
#SBATCH --cpus-per-task=1

# Optional: print useful job info
echo "Running on host: $(hostname)"
echo "Job started at: $(date)"
echo "SLURM job ID: $SLURM_JOB_ID"
echo "Number of CPUs: $SLURM_CPUS_PER_TASK"

# Load required modules
module purge
module load python

# Set any environment variables or configuration options
export PYTHONUNBUFFERED=1

# Move to job directory
cd $SLURM_SUBMIT_DIR

# Activate Python virtual environment
source venv/bin/activate

# Run the Python script
srun python augment_images_multinode.py
