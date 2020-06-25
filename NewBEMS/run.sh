# Assign the project directory variables
project_dir=$(dirname $(readlink -f "$0"))
tempwebserver_dir="/WebServer/"
tempagent_dir="/AgentPlatform/"
webserver_dir=$project_dir$tempwebserver_dir
agent_dir=$project_dir$tempagent_dir

# Activate the virtual environment
. venv/bin/activate

# Export the flask variables
export FLASK_APP=WebServer
export FLASK_ENV=development

# Setup the db file
cd $webserver_dir
if [ -f "meta.db" ];
then
  rm meta.db
  touch meta.db
else
  touch meta.db
fi

# Run the initialization.sql file
sqlite3 meta.db < initialization.sql
cd $project_dir

# Run all the agents
cd $agent_dir
#xterm python3 DiscoveryAgent.py &
python3 DiscoveryAgent.py &

# Run the server
cd $project_dir
flask run

# Deactivate the virtual environment
deactivate
