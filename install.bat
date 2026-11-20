@echo off

python -m venv dbt_env

call dbt_env\Scripts\activate.bat

python -m pip install --upgrade pip
pip install -e .

load

pause