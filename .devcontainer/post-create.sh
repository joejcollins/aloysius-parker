# Post create.
make venv-dev
echo "make lint" > .git/hooks/pre-commit
echo "make test" >> .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
