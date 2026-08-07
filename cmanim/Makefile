MANIM_BASE=TTY_COMPATIBLE=0 COLUMNS=240 poetry run manim

run-test:
	PYTHONPATH=$(shell pwd)/src $(MANIM_BASE) \
		--disable_caching -pqh test.py TestScene
	rm -r media

run-test-gif:
	# FULL_HD
	PYTHONPATH=$(shell pwd)/src $(MANIM_BASE) \
		--disable_caching -qh --format=gif \
		--output_file TestScene.gif --fps=10 test.py TestScene
	mkdir -p docs
	mv media/videos/test/1080p10/TestScene.gif docs/TestScene.gif
	# SHORTS
	rm -r media
	PYTHONPATH=$(shell pwd)/src $(MANIM_BASE) \
		--disable_caching -qh --format=gif \
		--output_file TestSceneShorts.gif --fps=10 test.py TestSceneShorts
	mkdir -p docs
	mv media/videos/test/1920p10/TestSceneShorts.gif docs/TestSceneShorts.gif
	rm -r media