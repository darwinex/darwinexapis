#!/bin/bash
# Get into your python env > You may need to install twine > pip install twine
source activate alphateam
pip install twine
conda env export > your_alpha_env.yml 
rm -Rf dist/*
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*