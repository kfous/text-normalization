# Text Normalization System Using Ollama

This is a system running with **llama3**, enabling text normalization on a dataset of your choice.  
Docker is used to spin up a MongoDB instance for this project.

<img src='images/ollamadocker.jpg' alt='Penguins' width="800">

1. **Download [Ollama](https://ollama.com/)**  
2. **Run Ollama**  
   ```bash
   ollama run llama3.1:8b-instruct-q4_0
   ```
3. **Install [Docker Desktop](https://www.docker.com/)**  
4. **Create a virtual environment**  
   ```bash
   python -m install virtualenv venv
   ```
   - Make sure it is integrated as your interpreter (e.g., in PyCharm).
5. **Activate the virtual environment**  
   - **Windows**: `.\venv\Scripts\activate`  
   - **Unix**: `./venv/bin/activate`
6. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```
7. **Install [Studio 3T](https://studio3t.com)** to query MongoDB  
8. **Run Docker Compose**  
   ```bash
   docker-compose up -d
   ```
9. **Connect to MongoDB** through Studio 3T at `localhost:27017`
10. **Run the clean data script**
    ```bash
    python ./scripts/clean_data.py
    ```
10. **Run the insert script**  
    ```bash
    python ./scripts/db_insert.py
    ```
11. **In IntelliShell**, run the following to verify inserted data:  
    ```js
    db.normalized_collection.find({})
    ```
