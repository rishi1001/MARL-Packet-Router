#!/bin/sh
### Set the job name (for your reference)
#PBS -N map_1_5
### Set the project name, your department code by default
#PBS -P cse
### Request email when job begins and ends, don't change anything on the below line 
#PBS -m bea
### Specify email address to use for notification, don't change anything on the below line
#PBS -M $USER@iitd.ac.in
#### Request your resources, just change the numbers
#PBS -l select=1:ncpus=1:ngpus=1:mem=16G
### Specify "wallclock time" required for this job, hhh:mm:ss
#PBS -l walltime=00:30:00
#PBS -l software=PYTHON

# After job starts, must goto working directory. 
# $PBS_O_WORKDIR is the directory from where the job is fired. 
echo "==============================="
echo $PBS_JOBID
cat $PBS_NODEFILE
echo "==============================="
cd $PBS_O_WORKDIR
echo $PBS_O_WORKDIR

module load pythonpackages/3.6.0/matplotlib/3.0.2/gnu
module load apps/pytorch/1.6.0/gpu/anaconda3
module load pythonpackages/3.6.0/numpy/1.15.0/gnu
module load pythonpackages/3.6.0/tqdm/4.25.0/gnu


make run 
