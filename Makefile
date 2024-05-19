test:
	pytest -vv .

freeze:
	pip freeze > requirements.txt

install:
	pip install -r requirements.txt

exe:
	pyinstaller ankify/main.py

