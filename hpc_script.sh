#!/bin/bash

VIDEO_FILES=/mnt/rds/redhen/gallina/tv/2022/2022-01/2022-01-01
SCRATCH_USER=/scratch/users/$USER
TOOLS_FOLDER=$SCRATCH_USER/gsoc2022/tagging_audio_effects/tools
ROOT_FOLDER=$SCRATCH_USER/gsoc2022/tagging_audio_effects
HOME_FOLDER=/home/$USER

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

#Testing for 1 month videos 
#singularity exec /scratch/users/$USER/image.sif python3 /scratch/users/$USER/gsoc2022/tagging_audio_effects/tools/audio_file_convertor.py -i /mnt/rds/redhen/gallina/tv/2022/2022-01/2022-01-01/ -a "wav" -o /scratch/users/$USER/Output/AudioFiles/  -l 0 --verbose=True
singularity exec --bind $SCRATCH_USER $SCRATCH_USER/image.sif python3 $TOOLS_FOLDER/audio_file_convertor.py -i $SCRATCH_USER/VideosFiles/ -a "wav" -o $SCRATCH_USER/Output/AudioFiles/  -l 1
echo "All the video files are converted to Audio, now run the tagging"
singularity exec --bind $SCRATCH_USER $SCRATCH_USER/image.sif python3 $ROOT_FOLDER/tag_audio_effects.py -i $SCRATCH_USER/Output/AudioFiles/ -o $SCRATCH_USER/Output/TaggedAudioFiles/ -l 1
echo "All the audio files are tagged with the effects, now you can run queries on them"

#Remove all Video and Audio files
rm -rf $SCRATCH_USER/VideosFiles
rm -rf $SCRATCH_USER/Output/AudioFiles
echo "All audio and video files removed, only tagged files present"

# Copy the tagged files to home
cp -r $SCRATCH_USER/Output/TaggedAudioFiles $HOME_FOLDER




