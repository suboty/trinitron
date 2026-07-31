run-test:
	PYTHONPATH=$(shell pwd)/src poetry run manim \
		--disable_caching -pqh test.py TestScene
	rm -r media

run-test-gif:
	PYTHONPATH=$(shell pwd)/src poetry run manim \
		--disable_caching -qh --format=gif \
		--output_file TestScene.gif --fps=10 test.py TestScene
	mkdir -p docs
	mv media/videos/test/1080p10/TestScene.gif docs/TestScene.gif
	rm -r media