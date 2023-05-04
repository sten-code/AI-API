@echo off
set /p NAME="What docker image do you want to run?"
docker run -it --gpus all -e NVIDIA_DRIVER_CAPABILITIES=all -p 80:80 -p 5000:5000 --privileged %NAME%