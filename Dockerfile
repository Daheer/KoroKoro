# Use an official PyTorch image based on CUDA
FROM pytorch/pytorch:1.10.0-cuda11.1-cudnn8-runtime

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Hugging Face Accelerate
RUN pip install accelerate

# Run setup.sh
RUN ["bash", "setup.sh"]

RUN ["python", "KoroKoro/pipeline/stage_01.py"]

CMD ["python", "KoroKoro/pipeline/stage_02.py"]