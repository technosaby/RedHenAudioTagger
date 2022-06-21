This will contain all the tools required for the project. 

## Generate Audio files from the video files
  - File Name : VideoProcessor.py
  - Parses the video files and extracts audio from the video files. 
  - This will copy the folder structure with all videos and create similar folder structure with generated audio files.
  - It generates mono audio because Yamnet needs only mono.
  - It generates sampling rate of 16k based on Yamnet's requirements.
    
  ### Instructions to Run 
  To run this locally, we can use the command as below.
  
  ```python VideoProcessor.py <<folder_with_video_files>> <<folder_for_audio_files>> <<output_audio_format>> <<input_video>> <<logs_enabled>>```
  #### Example: 
  1. Download a sample mp4 file using the following command
    ```curl -L -o sample_video.mp4 "https://drive.google.com/uc?export=download&id=1BSEKvjTawTd36rvpE4pFjYKPwh-fKNZ-"```
  2. Generate an audio file (wav format) from the downloaded video file (mp4 format) with logs enabled using the command, 
    ```python VideoProcessor.py sample_video.mp4 ./ "wav" "mp4" 1```
