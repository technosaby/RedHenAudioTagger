#!/bin/bash

VIDEO_FILES=/mnt/rds/redhen/gallina/tv/2022/2022-01/2022-01-01
SCRATCH_USER=/scratch/users/$USER
TOOLS_FOLDER=$SCRATCH_USER/gsoc2022/tagging_audio_effects/tools

# Load Module
module load singularity/3.8.1

# Change directory into $USER
cd $SCRATCH_USER/

# Copy one month video file from mnt to scratch
mkdir VideosFiles
cp -r $VIDEO_FILES $SCRATCH_USER/VideosFiles/

# Clone Source Code
#git clone https://github.com/technosaby/gsoc2022.git

# Creating Singularity Image from Github
#singularity pull image.sif docker://ghcr.io/technosaby/gsoc2022-redhen-audio-tagging-stages:1

# Creating Directories for Outputs
mkdir Output/
cd Output
mkdir AudioFiles
mkdir TaggedAudioFiles
mkdir FilteredOutput

#Testing for 1 month videos 
#singularity exec /scratch/users/$USER/image.sif python3 /scratch/users/$USER/gsoc2022/tagging_audio_effects/tools/audio_file_convertor.py -i /mnt/rds/redhen/gallina/tv/2022/2022-01/2022-01-01/ -a "wav" -o /scratch/users/$USER/Output/AudioFiles/  -l 0 --verbose=True
singularity exec --bind $SCRATCH_USER $SCRATCH_USER/image.sif python3 $TOOLS_FOLDER/audio_file_convertor.py -i $SCRATCH_USER/VideosFiles/ -a "wav" -o $SCRATCH_USER/Output/AudioFiles/  -l 1

#Remove all copied files
#rm -rf /scratch/users/$USER/image.sif





