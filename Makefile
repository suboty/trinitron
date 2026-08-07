MEDIA_DIR=videos/_rendered
PYTHONPATH_SETUP=PYTHONPATH=$(shell pwd)
MANIM_BASE=TTY_COMPATIBLE=0 COLUMNS=240 poetry run manim -qh
MANIM_SHORTS=$(MANIM_BASE) -r 1080,1920

FRONTEND_PATH=videos/compilers/frontend.py
LEXER_PATH=videos/compilers/lexer.py
PARSER_PATH=videos/compilers/parser.py
SEMANTIC_PATH=videos/compilers/semantic.py

install:
	poetry install --no-root
	chmod +x scripts/clean_manim_output.sh

clean:
	rm -rf media


create-episode-base:
	@test -n "$(EPISODE_PATH)" || (echo "EPISODE_PATH is required"; exit 1)
	@test -n "$(EPISODE)" || (echo "EPISODE is required"; exit 1)
	@test -n "$(EPISODE_NAME)" || (echo "EPISODE_NAME is required"; exit 1)
	@mkdir -p "$(EPISODE_PATH)"
	@cp videos/template.py "$(EPISODE_PATH)/$(EPISODE_NAME).py"
	@sed -i '' 's/EPISODE/$(EPISODE)/g' "$(EPISODE_PATH)/$(EPISODE_NAME).py"
	@echo "Created $(EPISODE_PATH)/$(EPISODE_NAME).py"


# FRONTEND

frontend-episode-build-hd:
	$(PYTHONPATH_SETUP) $(MANIM_BASE) $(FRONTEND_PATH) FrontendAnimation
	./scripts/clean_manim_output.sh $(MEDIA_DIR) FrontendAnimation frontend

frontend-episode-build-shorts:
	$(PYTHONPATH_SETUP) $(MANIM_SHORTS) $(FRONTEND_PATH) FrontendAnimationShorts
	./scripts/clean_manim_output.sh $(MEDIA_DIR) FrontendAnimationShorts frontend

frontend-episode-build-all: frontend-episode-build-hd frontend-episode-build-shorts


# LEXER

lexer-episode-build-hd:
	$(PYTHONPATH_SETUP) $(MANIM_BASE) $(LEXER_PATH) LexerAnimation
	./scripts/clean_manim_output.sh $(MEDIA_DIR) LexerAnimation lexer

lexer-episode-build-shorts:
	$(PYTHONPATH_SETUP) $(MANIM_SHORTS) $(LEXER_PATH) LexerAnimationShorts
	./scripts/clean_manim_output.sh $(MEDIA_DIR) LexerAnimationShorts lexer

lexer-episode-build-all: lexer-episode-build-hd lexer-episode-build-shorts


# PARSER

parser-episode-build-hd:
	$(PYTHONPATH_SETUP) $(MANIM_BASE) $(PARSER_PATH) ParserAnimation
	./scripts/clean_manim_output.sh $(MEDIA_DIR) ParserAnimation parser

parser-episode-build-shorts:
	$(PYTHONPATH_SETUP) $(MANIM_SHORTS) $(PARSER_PATH) ParserAnimationShorts
	./scripts/clean_manim_output.sh $(MEDIA_DIR) ParserAnimationShorts parser

parser-episode-build-all: parser-episode-build-hd parser-episode-build-shorts


# SEMANTIC

semantic-episode-build-hd:
	$(PYTHONPATH_SETUP) $(MANIM_BASE) $(SEMANTIC_PATH) SemanticAnimation
	./scripts/clean_manim_output.sh $(MEDIA_DIR) SemanticAnimation semantic

semantic-episode-build-shorts:
	$(PYTHONPATH_SETUP) $(MANIM_SHORTS) $(SEMANTIC_PATH) SemanticAnimationShorts
	./scripts/clean_manim_output.sh $(MEDIA_DIR) SemanticAnimationShorts semantic

semantic-episode-build-all: semantic-episode-build-hd semantic-episode-build-shorts