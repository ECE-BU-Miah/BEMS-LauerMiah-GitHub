# Assign the project directory variables
project_dir=$(dirname $(readlink -f "$0"))
tempwebserver_dir="/WebServer/"
webserver_dir=$project_dir$tempwebserver_dir

# Update Linux
sudo apt-get update

# Install pip3 and venv
sudo apt-get install python3-pip python3-venv xterm sqlite3

# Delete the venv if already exists
if [ -d "venv/" ];
then
  sudo rm -r venv/
fi

# Create the virtual environment
python3 -m venv venv

# Activate the virtual environment
. venv/bin/activate

# Install the python dependencies
pip3 install -r requirements.txt

# Get the python version
chmod +x utils.py
pyversion=$(./utils.py version)

# Create a pth_directories.pth file in the
# site-packages directory and add
# the directories to be added to the PYTHON_PATH
# variable to the file
if [[ -d venv/lib/$pyversion/site-packages/ ]];
then
  cd venv/lib/$pyversion/site-packages/
  touch pth_directories.pth
  echo $webserver_dir > pth_directories.pth
  echo $project_dir > pth_directories.pth
  cd $project_dir
  echo "Succesfully added directories to the PYTHON_PATH"
else
  echo "Unable to add directories to the PYTHON_PATH"
fi

echo
echo "Installation successful!"
echo "Run the platform with ./run.sh"
echo

# Deactivate the virtual environment
deactivate
