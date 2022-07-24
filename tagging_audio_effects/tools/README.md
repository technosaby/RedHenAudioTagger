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
 - Parses the metadata file (.sfx) file to filter tags based on query. The .sfx file is passed as an argument with "-i". 
 - It takes a JQ query and filters the tags and the scores based on that. 
This is passed as an argument with "-q". 
 - To select the range of dates, the start date is passed with "-s" argument while the end date is passed with "-e".
 - It filters score for each frames present in the SFX file and dumps the result in a CSV file. 

  ### Instructions to Run
  To run this locally, we can use the command as below.
  ```python ssfx.py -i <tagged files> -s <start date> -e <end date> -q <JQ Query> -l <logs enabled (default 0) >```
  
This will take the sfx file(s) from the "samples" folder (which are generated from the tagging script) and filters 
  between the dates "2022-01-01" and "2022-11-01" and then filters the scores based on the query for each frame of data.
  The output will contain the timestamp where the tag is found and the scores for all the tags at that timestamp.
  The tags which are present in the SFX file and should be used for filtering are given in the [code book](../codebook/codebook_yamnet_1.0.csv)
  . An example of an output csv file filtered by the command given above can be found [here](../samples/2022-07-10_PresidentXiJinping-Why_I_proposed_the_Belt_and_Road-hNKTbMx8PFk.csv) can 
  for reference.
  
  ### Reference for writing the query
  [JQ](https://stedolan.github.io/jq/) has been used to generate the query for the tags. Some examples to make the queries 
  are given below. These are standard JQ query formats.
  - ```"(.Music // .Song)"```
    Filter the frames which contain tag with (Music or Radio) 
  - ```".Song, .Radio"```
    Filter the frames which contain tags with Song and Radio
  - ```"(.Music // .Song), (.Television // .Radio)"```
    Filter the frames which contain tag with (Music or Radio) and (Television or Radio)
 
 ## Generate Codebook
 - File Name: codebook_generator.py
 - This file with take the YaMNet class mapping [csv file](../models/assets/yamnet_class_map.csv) and generate 
 a [codebook file](../codebook/codebook_yamnet_1.0.csv)
 - In the process, it also does some formatting ( like removing the ',' between tags and replacing them with '|', 
 string formatting, etc)
   ### Instructions to run
   ```python codebook_generator.py```

