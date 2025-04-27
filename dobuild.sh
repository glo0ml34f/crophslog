#!/bin/bash
python3 -m venv build
source build/bin/activate
pip3 install -r requirements.txt
git clone https://github.com/MunifTanjim/tree-sitter-lua
pushd tree-sitter-lua
make
python3 setup.py install
popd

