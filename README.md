# Notesdude [![Build Status](https://travis-ci.org/xorrr/notesdude.svg)](https://travis-ci.org/xorrr/notesdude)

a basic note taking application realized with the bottle python web
framework while using TDD

# virtualenv
To create the virtual environment and load the requirements with pip use:

    virtualenv --no-site-packages --distribute .env &&
    source .env/bin/activate && pip install -r requirements.txt

## Tests

To run the tests use:

    ./run_tests.sh

## Deployment
### Switch to PostgreSQL
SQLite backs up its data store in files on disk. Heroku will clear the contents of the app periodically and any files written will be discarded the moment the dyno is stopped or restarted. Therefore we're going to switch to PostgreSQL.

### WIP
single out tests by using the following command:

    nosetests <file>:<Test_Case>.<test_method>

e.g.

    nosetests tests/test_dbaccessor.py:TestDbAccessor.test_connection

## License
MIT
