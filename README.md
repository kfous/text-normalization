# Text Normalization System Using Ollama

This is an application running with llama3 that enables text normalization on a dataset of your choice.
It can be run in a Docker environment where a MongoDB instance is initialized and connected to your local Ollama.

![ollamadocker.jpg](..%2F..%2FPictures%2Follamadocker.jpg)

1. Download [Ollama](https://ollama.com/)  
2. Run:  
   ```bash
   ollama run llama3.1:8b-instruct-q4_0
4. Install [Docker Desktop](https://www.docker.com/)
5. Create a virtual environment 
   ```bash
    python -m install virtualenv venv
- Make sure it is integrated as your interpreter (e.g. in PyCharm)
6. Activate the virtual environment
- Windows: ***./venv/Scripts/activate*** 
- Unix: ***./venv/bin/activate*** 
7. Install dependencies
   ```bash
    pip install -r requirements.txt
8. Install [Studio 3T](https://studio3t.com) to access MongoDB container
9. Run Docker Compose
   ```bash
    docker-compose up --build
10. Connect to MongoDB through Studio 3T at ***localhost:27017*** 
11. In IntelliShell run the below command and verify data inserted:
   ```bash
    db.normalized_collection.find({})