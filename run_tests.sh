# Activate the virtual environment
source .venv/bin/activate

# Run mypy
mypy --config-file sp2txtbot/mypy.ini sp2txtbot

# Run flake8
flake8 --ignore=E501,F401,F405,F403,W503 sp2txtbot