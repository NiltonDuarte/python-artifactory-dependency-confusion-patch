publish:
	python3 -m build .
	twine upload dist/*
	/bin/rm -r dist/