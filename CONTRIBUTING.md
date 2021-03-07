# Contributing

This project is currently in a pre-alpha stage, and so currently I'd prefer to be the sole author of this code. If you like Theia and would like to help out, I'd love to know how you're using it & if there's anything I can do to improve the documentation!

However, if you're determined to help out with code, here's a couple of things to keep in mind:

## Checks

All PRs and commits to main are automatically checked using Github Actions.

Testing is done with the standard **unittest** library. To run tests from the root directory:

```bash
python -m unittest
```

Formatting is done with [Black]. Style is checked automatically and strictly enforced.

## Releases

Putting this here so I don't forget the commands:

```bash
python setup.py sdist bdist_wheel
twine upload dist/*
```
