This will contain all the tools required for the project. 

## Generate Audio files from the video files
  - File Name : VideoProcessor.py
  - Parses the video files and extracts audio from the video files. 
  - This will copy the folder structure with all videos and create similar folder structure with generated audio files.
  - It generates mono audio because Yamnet needs only mono.
  - It generates sampling rate of 16k based on Yamnet's requirements.
    
  ### Instructions to Run 
  To run this locally, we can use the command as below.
    - python VideoProcessor.py <<folder_with_video_files>> <<folder_for_audio_files>> <<output_audio_format>> <<input_video>> <<logs_enabled>>
    - Example: Command to generate video files from "sample_redhen_files" containing ".mp4" files to "output_files" with ".wav" files and logging enabled 
      python VideoProcessor.py sample_redhen_files/ output_files/ "wav" "mp4" 1
  
## DataParser.py
  - This file parses the outputs from the model and parses the data and dump it in different formats
