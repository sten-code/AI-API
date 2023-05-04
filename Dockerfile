# Use the official Python image as the base image
FROM python:3.11-bullseye

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY ./website ./website
COPY ./models ./models
COPY ./server.py ./
COPY --chmod=+x ./setup.sh ./

# Install Node.js and npm
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - &&\
    apt-get install -y nodejs


# Install the Node.js dependencies and build the React app
RUN cd website && \
    npm run build && \
    npm install -g serve 

RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
# Expose port 8000 for the Python app
EXPOSE 80
EXPOSE 5000

# Start the Python app and the React server
CMD ./setup.sh
