echo "Creating virtual enviroment..."
python3 -m venv venv

echo "Activating virual enviroment..."
source venv/bin/activate

echo "Installing requirements in virtual enviroment..."
pip3 install -r requirements.txt

echo "Done!"
