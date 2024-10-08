echo "Creating virtual enviroment..."
python3 -m venv venv /dev/null 2>&1

echo "Activating virual enviroment..."
source venv/bin/activate --quiet

echo "Installing tkinter (may ask for password)..."
sudo apt-get install python3-tk -q

echo "Installing requirements in virtual enviroment..."
pip3 install -r requirements.txt --quiet

echo "Done!"
