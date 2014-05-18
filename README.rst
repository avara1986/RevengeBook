.. contents::

======
RevengeBook
======

Information
===========
.. image:: https://travis-ci.org/avara1986/RevengeBook.svg?branch=master
    :target: https://travis-ci.org/avara1986/RevengeBook


.. image:: https://coveralls.io/repos/avara1986/RevengeBook/badge.png
  :target: https://coveralls.io/r/avara1986/RevengeBook


RevengeBook is a Social Website based on Pitble Django Project.

More info in:

https://github.com/openwebinars-django/pitble

Installation Basics
===================

* In your settings:

::

	EMAIL_HOST = 'smtp.gmail.com'
	EMAIL_PORT = 587
	EMAIL_HOST_USER = 'no-reply@your-domain.es'
	EMAIL_HOST_PASSWORD = '*****'
	EMAIL_USE_TLS = True
	DEFAULT_FROM_EMAIL = 'no-reply@your-domain.es'

Lunch virtual env:

::

	source vrevengeBoo1/bin/activate

Export Data:

::

	python manage.py dumpdata --indent=2 > data_initial.json
	
Load Data:

::

	python manage.py loaddata data_initial.json
	
Executing the test
==================

You need install project before

::

    python manage.py test revengeapp


Executing the test with tox
===========================

You DON'T need install project before. And you executing the tests with python 2.7/3.3 and Django 1.5/1.6

::

    pip install tox==1.7.1
    tox


Executing the test with tox and coverage
========================================

::

    sudo pip install coveralls==0.4.1
    coverage erase
    tox
    coverage combine
    coverage report -m
    coverage html
    chromium-browser htmlcov/index.html  # or another browser

Requirements
============

::

	argparse (1.2.1)
	
	Django (1.6.5)
	
	Pillow (2.4.0)
	
	pip (1.5.5)
	
	setuptools (3.4.4)
	
	wsgiref (0.1.2)


Special Thanks
==============

For the support and her ideas and creativity :)

