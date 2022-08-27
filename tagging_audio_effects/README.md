The main idea is to create a pipeline for tagging the audio effects in the audio files generated from the parser. 
At the first step I am using YaMNet model to do a baseline.

## Baselining
  - File Name : [tag_audio_effects.py](tag_audio_effects.py) 
  - Uses the YaMNet model to tag audio effects and generate outputs in a folder specified by the "-o" argument. 
The default path to generate the output is the path from where the command is run.
  - Takes an argument "-f" with the output file type (SFX/CSV) and generates a file with that extension 
with the output tags based on the timeline of the video. The CSV format is consumed by ELAN tool while SFX by the 
RedHen community for further research. The default value will generate both CSV and SFX files.
  - Takes the audio files as an input in a folder. This can be specified using the "-i" argument.
  - Takes the format of the audio files given as input. This can be specified by the "-a" argument. 
For now the default value is set to "wav" and it only supports WAV files because YaMNet supports only WAV files. 
The idea later is to extend it to other formats.
  - There is an additional flag (-d) to control how refined the filtering of the confidence scores should be. 
These are confidence scores calculated by the model for different classes of tags. If you want the tags with confidence 
scores to be very refined then you can select 4 decimal places which will filter tags with scores up to 4 decimal places 
{"Speech": 0.9600, "Clicking": 0.0003}. If you select tags which are dominant you can select 2 decimal places, then only 
{"Speech" : 0.96} will be filtered and "Clicking" will not be filtered at all in this case. The default value of this 
flag is set to 2.
  - In case of CSV files to be used in ELAN tool, there is an option to filter the scores (0 to 1). If you pass the 
score value with the -s parameter, you can generate tags in CSV format only for scores above the value. 
For example, if you want the tags with confidence scores more than 0.2, then pass "-s 0.2", so all confidence scores above 0.2 will be filtered. The default value of this flag is set to 0.0.
  - Generates the plots (log-melo-spectrogram, audio tags) for each audio files in a jpg format. This is set by "-g" argument.
By default, it is set to 0.
  

  ### Instructions to Run 
  To run this locally, we can use the command as below.
  ```python tag_audio_effects.py -i <audio input path> -a <audio input format (default: wav)> -o <output data path (default: .)> -d <decimal places for scores filtering (default : 2)> -f <output file type (default : BOTH) -s <score_filter (default :  0.0)> -g <plot graphs(default: 0)> -l <logs enabled (default 0) >```

  #### Example: 
  1. Download a sample wav file using the following command
    ```curl -O https://storage.googleapis.com/audioset/miaow_16k.wav```
  2. Create a folder like "audio_files" and move the downloaded files to this newly created folder. This is because, 
currently the script only processes files from a folder
    ```mkdir audio_inputs```
    ```mv miaow_16k.wav audio_inputs/```
  3. Generate audio tags from the downloaded audio file using the below command 
    ```python tag_audio_effects.py -i audio_inputs/ ```
This will take the wav files present in the "audio_inputs" folder and generate a file with name "miaow_16k.sfx" in the current path.
This file will contain the tags for each audio frames as tagged by YaMNet. For each frame of audio, it will log the scores up to 2 decimal places.
