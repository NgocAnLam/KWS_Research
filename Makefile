.PHONY: setup test clean

setup:
	pip install -r requirements.txt

test:
	pytest tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
