py_v=$'which python'
pip_v=$'which pip'



if [ -z "$py_v" ]; then
    echo 'no python'
    # sudo apt install python3
    brew install python 
fi

if [ -z "$pip_v" ]; then
    echo 'no pip'
    python get-pip.py
fi

pip install -r requirements.txt
