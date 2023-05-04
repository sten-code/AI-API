# AI-API
When running the docker image it is important that you map port 5000 to port 5000 otherwise the backend server can't communicate with the front end
If you want to generate images you need to have an nvidea GPU, and if you want to run the docker container, it needs to have acces to your nvidea GPU

# Running
You can install the nodejs modules by opening an terminal inside the folder website and running npm install -> You need te have nodejs 20 installed for this
After you have installed the node modules you can start the webserver with npm start . -> you still need to be in the website folder
When you no go to localhost/TextGen you won't see any models, in order to see those you need to run serv.py in the main folder

# Adding models
You can easily add your own models inside the models folder, just be aware that you need to use the layout that the other models use, so a folder with the name of the image where the slash is replaced by -- so facebook/opt-1.3b is facebook--opt-1.3b inside the folder you created needs to be a model.py file with a function that looks like the following `def generate(prompt: str, config: server.TextConfig) -> str:` wich returns the answer as a STRING
