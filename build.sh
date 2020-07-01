rm -rf *.egg-info dist build

python setup.py build sdist

twine check dist/*
