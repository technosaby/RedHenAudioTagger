# Gsoc2022
In GSoc 2022, I will be working with [Redhen Labs](https://www.redhenlab.org/summer-of-code/red-hen-lab-gsoc-2022-projects). 

The objective is to develop a machine learning model to tag sound effects in streams (like police sirens in a news-stream) of Red Hen’s data. A single stream of data can contain multiple sound effects, so the model should be able to label them from a group of known sound effects like a Multi-label classification problem. The first step would be to develop a baseline model using existing pre-trained deep learning models and add to the Red Hen’s pipeline. Then the performance can be improved using transfer learning and fine tuning the existing model to achieve better accuracy. In this process, the models can be trained on sound effects from noisy or human labeled data sets after they are pre-processed to avoid acoustic domain mismatch problems.

## Usage

### Local Development

#### Singularity 

TODO:

#### Docker Container

1. To build the docker image run the following command

```
docker-compose up
```

This command builds the docker image which can be pushed to the docker hub container.

2. Next use the following command to start up the docker container

```
docker run --gpus all -it --rm -p 8888:8888 -v $PWD:/TaggingAudioEffects technosaby/gsoc2022-redhen-audio-tagging
```


### Remote Development

The following set of instructions are to be used when developing on the CWRU HPC.

#### Singularity
1. Start a screen session
```
screen -S singularity
```

or reattach to existing screen

```
screen -r
```

2. Clone the docker image from docker hub
```
#ToDo
```

3. Start singularity shell
```
module load singularity/3.8.1
singularity shell -e -H `pwd` -B /mnt/rds/redhen/gallina/ ../Singularity/xxxx.sif
```


#### Syncing local files to remote

```
lsyncd -nodaemon -rsyncssh ./ sxg1263@rider.case.edu /mnt/rds/redhen/gallina/home/sxg1263/gsoc2022
```
