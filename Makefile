# The binary to build (just the basename).
MODULE := rss_bundle

init:
	pip install -r requirements.txt

test:
	py.test tests

run:
	@python -m $(MODULE)

PHONY: init test