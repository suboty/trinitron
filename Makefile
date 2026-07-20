install:
	poetry install --no-root
	chmod +x scripts/clean_manim_output.sh

MEDIA_DIR=videos/rendered

lexer-scene-build:
	PYTHONPATH=$(shell pwd)/videos \
		poetry run manim -pqh --media_dir $(MEDIA_DIR) videos/lexer/scene.py LexerAnimation

lexer-scene-build-cleaning:
	./scripts/clean_manim_output.sh $(MEDIA_DIR) LexerAnimation

shell:
	poetry shell

format:
	poetry run black .
	poetry run ruff check --fix .

lint:
	poetry run ruff check .

test:
	poetry run pytest

clean:
	rm -rf .pytest_cache/
	rm -rf **/__pycache__/