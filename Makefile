# The binary to build (just the basename).

init:
	pip install -r requirements.txt

test:
	py.test tests

bundle:
	@python -m rss_bundle

proxy:
	@uvicorn rss_proxy.__main__:app

PHONY: init test