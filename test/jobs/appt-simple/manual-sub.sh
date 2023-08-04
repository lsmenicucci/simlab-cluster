#!/usr/bin/bash

# get node from command line, default to compute-4
node=${1:-compute-4}

sbatch -w $node job.sh && sleep 2 && cat slurm* && rm slurm-*.out^
