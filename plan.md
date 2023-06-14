# Song Structure

This code takes in a song and produces a best guess for where similar parts of the song are repeated. This is used to determine which parts are in a verse, chorus, etc. 

This problem has two parts. The first is a *Clustering* problem, where sections of the song must be grouped together into the same parts. The second, less important problem is a *Classification* problem, that decides if a section is a chorus or verse or whatever. For now, lets only focus on the *Clustering*.

A different approach could be generating a set of times where the song changes. Detecting change may be simpler than categorizing 1-second clips of audio.

Another strategy could be giving the model two sections that are directly next to each other, and predicting if a transition occurs in/between them. This may work well for simple songs with big changes, but metal might struggle. Also, you lose the ability to do grouping, which is part of the thing we want.

## Concepts

*Label* is the variable we are predicting - the output value, and the target we are predicting. Represented as `y`

*Features* are input variables describing the data. Represented as `{x_1, x_2, ... x_n}`

At some point, I will need to define an error on the predictions. 

Will need to separate a `training set`, `validation set` and a `test set` partitioned at the start. This is how we have confidence in a model.

Classifiers involve binary classification. This brings up the true/false negatives/postives question, and we need to have metrics that reflect this. A model needs *Precision* `(true positives)/(all positive predictions)` and *Recall* `(true positives)/(all actual positives)`

Classifiers also need a threshold. As they return probabilities, we have to pick a threshold wisely.

## Research

Pychorus [article](https://towardsdatascience.com/finding-choruses-in-songs-with-python-a925165f94a8) and [github](https://github.com/vivjay30/pychorus) is an analytical solution to this. features: 

- Dimensionality lowering: turns the spectrogram into NOTES
    - Using Librosa
    - Loses octave information (is that necessary?)
    - Loses rhythm
- Uses beat detection
    - Cool
- Generates a time-time and time-lag similarity matrix
    - How to compare all times to each other ineficciently (brute force)
    - Could improve that if we identify a part A, and then B, etc. sequentially

Audio Analysis About [article](https://www.altexsoft.com/blog/audio-analysis/) Just talks about prepping audio for ML tasks.






## Tools

### Spectrogram

x: time, y: frequency, z: intensity. Gives an matrix representation of an audio clip.

### Mel Spectrogram

Transforms the spectrogram and focuses on relative pitch difference for humans. Useful for genre classification, simplifies the input but not too much.


### Tensorflow

- Has tensorflow-io which handles audio processing

[clustering lessons](https://developers.google.com/machine-learning/clustering)


### Windowing samples

As we are going to split the song up into multiple parts, we need to window with a smoothing function.

`wn=sin(pi(n+0.5)/L)`

[Link](https://wiki.aalto.fi/display/ITSP/Windowing)



### Install Process

Following [install tensorflow on windows with wsl2](https://www.tensorflow.org/install/pip#windows-wsl2_1) so I can use my GPU. I paid money for that thing. Then [Tensorflow-io](https://github.com/tensorflow/io#tensorflow-version-compatibility)

- WSL2
- miniconda in wsl2
- conda env for the project
- python 3.9 in the env
- some secret magic commands from the tf team


Then you need 


### Commands

```
# set up environment
conda create --prefix=songstructure python=3.9
conda activate ./songstructure
conda deactivate

# enter vscode
code .

# do package management
conda env export --from-history > env.yml
pip freeze > requirements.txt

```

```
# run once stuff

conda install -c conda-forge cudatoolkit=11.8.0
pip install nvidia-cudnn-cu11==8.6.0.163
pip install --upgrade pip
pip install tensorflow==2.11.*
pip install tensorflow-io==0.31.*
```

## Plan

- install tensorflow
- Use Tensorflow-io to open an audio file
- Figure out how to split the audio file and create training samples
- Figure out how to generate audio/audio/label sets for training
- write a Model for taking audio+audio+label and define all the shit


## Process

Download a song from youtube

```
conda activate ./songstructure
pip install -U yt-dlp
yt-dlp -x --audio-format mp3 --audio-quality 128K -o filename https://www.youtube.com/watch?v=LokJLTLYHGg
```


