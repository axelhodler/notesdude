# Notesdude

[![Build Status](https://travis-ci.org/xorrr/notesdude.png)](https://travis-ci.org/xorrr/notesdude)

a basic note taking application realized with the bottle python web
framework while using TDD

# virtualenv
To create the virtual environment and load the requirements with pip use:

    virtualenv --no-site-packages --distribute .env &&
    source .env/bin/activate && pip install -r requirements.txt

## Tests

To run the tests use:

    ./run_tests.sh