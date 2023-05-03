pip install -r requirements.txt
python server.py & disown
cd website
#curl -fsSL https://deb.nodesource.com/setup_20.x | bash - &&\
#apt-get install -y nodejs
npm run build
#npm install -g serve
serve -s build -l 80


