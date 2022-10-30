# Gsoc2022 - RedHen Labs - Tagging Audio Effects
In GSoc 2022, I worked with [Redhen Labs](https://www.redhenlab.org/summer-of-code/red-hen-lab-gsoc-2022-projects). 

The objective was to develop a machine learning model to tag sound effects in streams (like police sirens in a news-stream) 
of Red Hen’s data. A single stream of data can contain multiple sound effects, so the model should be able to label them 
from a group of known sound effects like a Multi-label classification problem. YamNet is used a pretrained model in this project.
The video files are converted into audio files. Then they are tagged by YamNet for the sound effects and dumped into 
2 kinds of files:
- SFX Files: These files are based on RedHen's standards where tags are mapped with every frame of audio data. JQ queries can 
be used to filter the SFX tags.
- CSV Files: These files contain tags and their times for the frames. These CSV files are consumed by ELAN tool for annotations
based on the tiers as sound effects.

## Usage
### Singularity Environment

The below mentioned steps are to run the Audio Tagger in Case Western Reserve HPC as of August 2022.

1. Create a folder name with videos required for tagging or use an existing folder from RedHen's mount point. Store it in a variable VIDEO_FILES. 
```VIDEO_FILES=/mnt/rds/redhen/gallina/tv/2022/2022-01/2022-01-01/``` 
If you are planning to create in the tags in SFX file, it is better to have a .seg files for your videos. If you dont have a .seg file only TOP Block will be generated along with the Audio taggings. 

2. Please clone the repo in RedHen's HPC as a scratch user in the home of the scratch user (e.g: /scratch/users/sxg1263/). After cloning you will have 
a folder containing all the code.

3. Go inside the folder (using cd command) and set the variables as below
   ```
   HOME_FOLDER=$PWD
   TOOLS_FOLDER=$HOME_FOLDER/tagging_audio_effects/tools
   ROOT_FOLDER=$HOME_FOLDER/tagging_audio_effects
   SCRATCH_USER=/scratch/users/$USER
   ```
4. Load the singularity container.  
  ```module load singularity/3.8.1```

5. In the scratch workspace, (e.g: /scratch/users/sxg1263/) create the singularity image from Github workspace.
   ```singularity pull image.sif docker://ghcr.io/technosaby/gsoc2022-redhen-audio-tagging-stages:1```

6. Create temporary folders for Outputs. The AudioFiles folder will contain the converted audio files while the TaggedAudioFiles contain the tagged files.
   ```
   mkdir Output/
   cd Output || exit
   mkdir AudioFiles
   mkdir TaggedAudioFiles
   ```

7. Execute the following command to convert the video (from $VIDEO_FILES) to audio file im the wav format (in Output/AudioFiles).   
```singularity exec --bind $SCRATCH_USER $SCRATCH_USER/image.sif python3 $TOOLS_FOLDER/audio_file_convertor.py -i $VIDEO_FILES -a "wav" -o $SCRATCH_USER/Output/AudioFiles/ ```

8. Execute the following command to use the Audio Files generated from the last step to generate the Audio Tags in CSV (with confidence >= 0.2) and SFX format. The tags will be generated in TaggedAudioFiles folder.
```singularity exec --bind $SCRATCH_USER $SCRATCH_USER/image.sif python3 $ROOT_FOLDER/tag_audio_effects.py -i $SCRATCH_USER/Output/AudioFiles/ -o $SCRATCH_USER/Output/TaggedAudioFiles/ -s 0.2```

9. After the script is run, an TaggedAudioFiles folders will be generated with the tagged audio files.

10.  You can now choose to copy the tagged files to your HPC home/PC for analysis using ELAN or JQ.

A script called [hpc_script.py](hpc_script.sh) contains all the steps for running in a singularity container. But it is better to run the steps individually.

## Future work
- Evaluate other audio taggers and evaluate their results 
- Compare the taggers and use transfer learning to create our own tags
