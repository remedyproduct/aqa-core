1. python3 -m pip install --user --upgrade setuptools wheel twine
2. navigate to directory
3. python3 setup.py sdist
4. python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*