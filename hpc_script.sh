#!/bin/bash

# Load Module
module load singularity/3.8.1

# Change directory into $USER
cd /scratch/users/$USER/

# Clone Source Code
#git clone https://github.com/technosaby/gsoc2022.git

# Creating Singularity Image from Github
singularity pull image.sif docker://ghcr.io/technosaby/gsoc2022-redhen-audio-tagging-stages:1

# Creating Directories for Outputs
mkdir Output/
cd Output
mkdir AudioFiles
mkdir TaggedAudioFiles
mkdir FilteredOutput

#Testing for 1 month videos 
singularity exec /scratch/users/$USER/image.sif python3 /scratch/users/$USER/gsoc2022/tagging_audio_effects/tools/audio_file_convertor.py -i /mnt/rds/redhen/gallina/tv/2022/2022-01/2022-01-01/ -a "wav" -o /scratch/users/$USER/Output/AudioFiles/  -l 0 --verbose=True

#Remove all files from the 
#rm -rf /scratch/users/$USER/image.sif





