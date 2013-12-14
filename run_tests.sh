#!/bin/sh

export DATABASE_URL=postgres://xorrr:@localhost/test

nosetests --rednose -s
