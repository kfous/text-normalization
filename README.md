# text-normalization

This is an application ran with llama3 enabling text normalization through a dataset of your choice.
The process can be run in a docker environment where a MongoDb is initialized and connect to your local ollama.

1. Download ollama
2. ollama run deepseek-r1:7b
3. ollama run llama3.2
4. Install docker desktop
5. Create a virtual environment 
- python -m install virtualenv venv
- make sure it is integrated as your interprepter e.g. if you are using PyCharm
6. Enable it
- ./venv/Scripts/activate for windows
- ./venv/bin/activate for Unix based systems
6.Install requirements.txt
7.Install Studio 3T to access the docker container mongo
8.Hit docker-compose up --build
9.Connect to mongo through Studio 3T
101.run in intelishel db.normalized_collection.find({}) to check the inserted data
