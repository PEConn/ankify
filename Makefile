test:
	pytest -vv .

freeze:
	pip freeze > requirements.txt

exe:
	pyinstaller ankify/main.py