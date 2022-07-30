#!/bin/bash

# Load Module
module load singularity/3.8.1

# Change directory into $USER
cd /scratch/$USER/

# Clone Source Code
git clone https://github.com/technosaby/gsoc2022.git

# Creating Singularity Image from Github
singularity pull image.sif docker://ghcr.io/technosaby/gsoc2022-redhen-audio-tagging-stages:1

# Creating Directories for Outputs
mkdir Output/
cd Output
mkdir AudioFiles
mkdir TaggedAudioFiles
mkdir FilteredOutput


#Remove all files from the 
rm -rf /scratch/$USER/*
rm -rf /temp/$USER/*





