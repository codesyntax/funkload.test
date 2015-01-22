funkload.buildout
=================

How to run this::

  $ virtualenv .
  $ ./bin/python bootstrap.py
  $ ./bin/buildout -vv

Run one test::

  $ make test

Run all test-suite::

  $ make bench-app

Then see the report file. You will find the exact location of this report
in the output of the previous command.
