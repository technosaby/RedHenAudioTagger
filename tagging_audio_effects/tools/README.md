This will contain all the tools required for the project. 

## Generate Audio files from the video files
  - File Name : audio_file_convertor.py
  - Parses the video files and extracts audio from the video files. 
  - This will copy the folder structure with all videos and create similar folder structure with generated audio files.
  - It generates mono audio because YaMNet needs only mono.
  - It generates sampling rate of 16k based on YaMNet's requirements.

  ### Instructions to Run 
  To run this locally, we can use the command as below.
    ```python audio_file_convertor.py <<folder_with_video_files>> <<folder_for_audio_files>> <<output_audio_format>> <<input_video>> <<logs_enabled>>```
  #### Example: 
  1. Download a sample mp4 file using the following command
  ```curl -L -o sample_video.mp4 "https://drive.google.com/uc?export=download&id=1X-TOEZ6wmnNDMzagt0Hyhp2YSwQaHI-T"```
  2. Place the file in a folder "sample"
  3. To generate an audio file (wav format) from the downloaded video file (mp4 format) with logs enabled using the command from the path outside the "sample" folder ,
  ```python audio_file_convertor.py sample/ ./ "wav" 1```

## Parse the metadata(.sfx) to filter tags
 - File Name: ssfx.py
 - Parses the metadata file (.sfx) file to filter tags.
 - It filters only single tags and gives the timestamp with the scores for that tag.
 - Currently, it only filters a single tag within a timeframe.
 - In the future, we need to implement an advanced filtering mechanism using logical operations (&, | etc).

  ### Instructions to Run
  To run this locally, we can use the command as below.
  ```python ssfx.py ../samples/ 2010-01-01 2020-01-01 Clicking 5 1```
  This will take the sfx file(s) from the "samples" folder (which are generated from the tagging script) and filters 
  between the dates "2010-01-01" and "2020-01-01" and then generates the tagging in a csv format. The tagging
  only contains the sound effects occuring within 5 seconds timeframe.
  The output will contain the tag name the timestamp where the tag is found and the scores for all the tags at that timestamp.
  A sample [output file](../samples/2010-01-01_2335_US_CSPAN2_World_War_II.csv) is also present in the "samples" folder for reference.
  
