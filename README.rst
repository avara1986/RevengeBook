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

  
.. image:: http://img.shields.io/badge/tips-$0/week-red.svg
   :target: https://www.gittip.com/avara1986/ 

RevengeBook is a Social Website based on Pitble Django Project.

More info in:

https://github.com/openwebinars-django/pitble

.. image:: http://www.ateneagested.com/img/rb.png
    :alt: HTTPie compared to cURL
    :width: 835
    :align: center

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

	Django==1.6.5
	Pillow==2.4.0
	South==0.8.4
	argparse==1.2.1
	ipdb==0.8
	ipython==2.0.0
	wsgiref==0.1.2
	django-allauth



Special Thanks
==============

For the support and her ideas and creativity :)

