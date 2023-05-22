echo "Installing project requirements"
python -m pip install --upgrade pip
pip install -r ./requirements.txt

echo "Add git config"
git config --global user.name "Sam Hardy"
git config --global user.email "samhardyhey@gmail.com"