# Python parent image
FROM python:3.9

# The working directory of the container
WORKDIR /usr/src/app

# Copy Python dependencies file to the container
COPY requirements.txt ./

# Install depndencies from requirement.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's source code from your host to your filesystem.
COPY . .

# Insert the normalized text to mongodb
CMD ["python", "scripts/db_insert.py"]
