import os

print("Running on", os.environ.get("HOSTNAME"))
print("NTASKS", os.environ.get("SLURM_NTASKS"))
print("PROCID", os.environ.get("SLURM_PROCID"))
print("NODEID", os.environ.get("SLURM_NODEID"))
print("LOCALID", os.environ.get("SLURM_LOCALID"))
