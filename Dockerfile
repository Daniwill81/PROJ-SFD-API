FROM python:3.12

WORKDIR /code

# Copy the requirements.txt file to the working directory
COPY requirements.txt /code
COPY requirements-dev.txt /code/requirements-dev.txt


# Install the Python dependencies from the requirements.txt file
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements-dev.txt

# Copy app files
COPY . .

# Load metadata, from metadata.yml :
RUN python register.py
# Run migrations :
RUN python migrate.py

EXPOSE 8000

WORKDIR /code/app
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]
