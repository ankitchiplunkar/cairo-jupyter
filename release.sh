# git commands
git checkout master
git pull
git stash

# tag commands
git tag `cat VERSION`
git push origin --tags

# upload the library to pypi
python setup.py sdist
twine upload dist/*