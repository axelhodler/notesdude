#!/bin/sh

#form: postgres://user:password@host:port/database
export DATABASE_URL=postgres://xorrr:@localhost/test

nosetests --rednose -s
