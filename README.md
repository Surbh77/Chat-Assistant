
# AI Chat Assistant

## Demo


https://github.com/Surbh77/Chat-Assistant/assets/108724393/804d0247-28e6-4890-8dc0-9092b2d3c697



## Table of Content
- [About](#About)  
- [Getting Started](#GettingStarted)  
    - [Prerequisites](#Prerequisites) 
    - [Environment Variables](#EnvironmentVariables)
- [Build and prepare the project](#Buildandpreparetheproject)
- [Running the chat Assistant](#RunningthechatAssistant)
## About

This **AI Chat Assistant**, equipped with versatile models like GPT-3.4 Turbo, GPT-4, Llama-2, and Mistral, dynamically selects the default language model (LLM) based on user preference.

**Current Modules**

-   **Models**: You can load, test, and use multiple LLM model restricted to .ggml format.
-   **Maintain Conversation**: It maintains the previous conversation and gives best output from the history of the chat.
-   **Temperature**: You can change the accuracy of the optput you want form the respective model.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine


## Prerequisites

You need to have a machine with Python >= 3.9. Optional, cuda>=11. for fast and best results

```
$ python3.9 -V
Python 3.9  

cuda11
```

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

Get the openai key by logging into the openai account.
`OPENAI_KEY`

Get the hugging face by logging into the huggingface account.
`HUGGINGFACE_KEY`


## Build and prepare the project

This section will go through the cloning the repo,creating a conda environment, setting up the environment variables and download the LLM models from huggingface.

**Clone this repository**

Open gitbash and navigate to the appropriate directory where you want to clone these files. Run the following commands:

```
git clone https://github.com/Surbh77/Chat-Assistant.git
```
**Creating conda environment**

Open Anaconda Command Prompt. Now create a new conda environment using following commands:

```
conda create -n chat_assistant python=3.10.4
```

Now activate the new conda environment.

```
Conda activate chat_assistant
```
Install all the dependencies from the requirements.txt file using the following command

```
conda install -r requirements.txt
```

**Setting enviroment variables** 

To setup environment variable in linux OS use following command:
```
pip install openai
export OPENAI_API_KEY=your_api_key
```
To setup environment variable in windows OS use following command:
```
set OPENAI_API_KEY=your_api_key
```

**Download LLM models from Huggingface**

You can use any of the .ggml or .gguf format model here.
Login into Huggingface and search for the following models:

```
TheBloke/Llama-2-7B-Chat-GGML
```
From there directly download the .gguf or .ggml file into the local directory.

Now replace the path of the respective model in the app.py file.

## Running the chat Assistant

The UI of this chat assistant is based on streamlit. To start this assistant you need use the following command from the working directory:

```
streamlit run app.py
```


