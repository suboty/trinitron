install:
	poetry install --no-root
	chmod +x scripts/clean_manim_output.sh

MEDIA_DIR=videos/rendered

lexer-scene-build:
	PYTHONPATH=$(shell pwd)/videos \
		poetry run manim -pqh --media_dir $(MEDIA_DIR) videos/lexer/scene.py LexerAnimation

lexer-scene-build-cleaning:
	./scripts/clean_manim_output.sh $(MEDIA_DIR) LexerAnimation
