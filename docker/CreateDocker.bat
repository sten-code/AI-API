@echo off
cd ..
set /p NAME="Image name: "
docker build -t %NAME% .