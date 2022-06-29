The main idea is to create a pipeline for tagging the audio effects in the audio files generated from the parser. 
At the first step I am using YaMNet model to do a baseline. Later the idea is to have a transfer learning.

## Baselining
  - File Name : tag_audio_effects.py
  - Uses the YaMNet model to tag audio effects 
  - Generates the plots (log-melo-spectrogram, audio tags) for each audio files in a jpg format
  - Generates a file with extension(.sfx) to generate the output tags based on the timeline of the video
    
  ### Instructions to Run 
  To run this locally, we can use the command as below.
  ```python tag_audio_effects.py <<folder_for_audio_files>> <<audio_format>> <<output_dump_file_format>> <<output_folder>> <<logs_enabled>>```

  #### Example: 
  1. Download a sample wav file using the following command
    ```curl -O https://storage.googleapis.com/audioset/miaow_16k.wav```
  2. Generate audio tags from the downloaded audio file with logs enabled using the command, 
    ```python tag_audio_effects.py . "wav" "default" . 1```
