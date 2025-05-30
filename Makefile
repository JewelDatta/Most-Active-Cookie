.PHONY: test lint coverage build mypy clean

test:
	pytest

lint:
	pylint most_active_cookie.py

coverage:
	pytest --cov=most_active_cookie --cov-report=term-missing tests/

build:
	pyinstaller --onefile most_active_cookie.py

mypy:
	mypy most_active_cookie.py

clean:
	rm -rf __pycache__ dist/ build/ *.spec .mypy_cache .pytest_cache
