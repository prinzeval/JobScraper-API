FROM python:3.9

WORKDIR /app

# Install system dependencies for building dlib and others (adjust if needed)
RUN apt-get update && apt-get install -y \
    cmake \
    build-essential

# Copy requirements and install in a single layer
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire resources folder
COPY . . 

# Expose the port the app runs on
EXPOSE $PORT

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
