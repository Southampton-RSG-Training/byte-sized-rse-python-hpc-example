#!/bin/sh

#SBATCH --job-name=python-mpi
#SBATCH --partition=batch
#SBATCH --reservation=root_1    # Reserved nodes for this class (don't add this normally)
#SBATCH --time=00:15:00     # Maximum run time
#SBATCH --nodes=2           # Run on 2 nodes
#SBATCH --ntasks=64         # Run 64 total workers
#SBATCH --tasks-per-node=32

# Optional: print useful job info
echo "Running on host: $(hostname)"
echo "Job started at: $(date)"
echo "SLURM job ID: $SLURM_JOB_ID"
echo "Number of CPUs allocated on each node: $SLURM_JOB_CPUS_PER_NODE"

# Load required modules
module purge
module load openmpi
module load python

# Move to job directory
cd $SLURM_SUBMIT_DIR

# activate the Python environment
source venv/bin/activate

# run the code
mpirun -mca coll_hcoll_enable 0 -n $SLURM_NTASKS python -m mpi4py.futures augment_images_mpi.py

# Clean-up
deactivate
module purge
