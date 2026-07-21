install:
	poetry install --no-root
	chmod +x scripts/clean_manim_output.sh

MEDIA_DIR=videos/rendered


# TEST

test-episode-build:
	PYTHONPATH=$(shell pwd)/videos \
		poetry run manim -pqh --media_dir $(MEDIA_DIR) videos/_test/episode.py TestAnimation

test-episode-build-cleaning:
	./scripts/clean_manim_output.sh $(MEDIA_DIR) TestAnimation


# TRINITRON EPISODES

lexer-episode-build:
	PYTHONPATH=$(shell pwd)/videos \
		poetry run manim -pqh --media_dir $(MEDIA_DIR) videos/lexer/episode.py LexerAnimation

lexer-episode-build-cleaning:
	./scripts/clean_manim_output.sh $(MEDIA_DIR) LexerAnimation
