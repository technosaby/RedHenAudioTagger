The main idea is to create a pipeline for tagging the audio effects in the audio files generated from the parser. 
At the first step I am using YaMNet model to do a baseline. Later the idea is to have a transfer learning.

## Baselining
  - File Name : tag_audio_effects.py
  - Uses the YaMNet model to tag audio effects 
  - Generates the plots (log-melo-spectrogram, audio tags) for each audio files in a jpg format
  - Generates a file with extension(.sfx) to generate the output tags based on the timeline of the video
  - There is an additional flag to control how refined the filtering should be. If you want the tags with scores to be 
very refined then you can select 4 decimal places which will filter tags with scores up to 4 decimal places {"Speech": 0.96, 
"Clicking": 0.0003}. If you select tags which are dominant you can select 2 decimal places, then only {"Speech" : 0.96} will be 
filtered and "Clicking" will not be filtered at all in this case.

  ### Instructions to Run 
  To run this locally, we can use the command as below.
  ```python tag_audio_effects.py <<folder_for_audio_files>> <<audio_format>> <<output_dump_file_format>> <<output_folder>> <<filtering_score_accuracy>> <<logs_enabled>>```

  #### Example: 
  1. Download a sample wav file using the following command
    ```curl -O https://storage.googleapis.com/audioset/miaow_16k.wav```
  2. Generate audio tags from the downloaded audio file with logs enabled using the below command 
    ```python tag_audio_effects.py . "wav" "default" . 4 1```
    This will take the wav file and generate the tags. For each frame of audio, it will log the scores upto 4 decimal
places.