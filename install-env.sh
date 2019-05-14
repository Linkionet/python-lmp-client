#!/bin/sh

echo -e "Install python3 virtualenv ? [Y/n]"
read INPUT_STRING
if [ "$INPUT_STRING" = "Y" ]; then

    # install python3 virutalenv
    sudo apt-get install python3-tk
    sudo apt-get install python3-venv
    mkdir -p env3
    python3 -m venv env3
    . "env3/bin/activate"
    pip install -r requirements3.txt
else
    # install python2.7 virutalenv
    echo "So install python2.7 virtualenv"
    mkdir -p env27
    virtualenv --python=/usr/bin/python2.7  env27
    . "env/bin/activate"
    pip install -r requirements27.txt
fi
