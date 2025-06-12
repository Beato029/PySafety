import os

os.system('sudo git clone https://github.com/Beato029/PySafety.git')
os.system('sudo rm -rf main.py')
path = os.getcwd()
os.system(f'sudo mv ./PySafety/main.py {path}')
os.system('sudo rm -rf PySafety')
os.system('sudo python main.py')
