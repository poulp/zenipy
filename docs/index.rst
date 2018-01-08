.. Zenipy documentation master file, created by
   sphinx-quickstart on Tue Jul  4 16:09:11 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Zenipy
******

Requirements
============

* Python 2 or 3
* GTK+3
* python3-gi or python-gi (for python2)

Installation
============

Install using pip :

.. code-block:: bash

    $ pip install zenipy

Or clone the repo :

.. code-block:: bash

    $ git clone https://github.com/poulp/zenipy.git
    $ cd ./zenipy
    $ python setup.py install

Example
=======

Simple dialog :

.. code-block:: python

    from zenipy import calendar
    result = calendar(title="Awesome Calendar",text="Your birthday ?")
    print(result)

This code show a calendar dialog :

.. image:: images/screen.png
    :align: center

And display the result :

.. code-block:: bash

    $ python test.py
    $ (year=2017, month=6, day=4)


API
===

.. automodule:: zenipy.zenipy
.. autofunction:: message
.. autofunction:: error
.. autofunction:: warning
.. autofunction:: question
.. autofunction:: entry
.. autofunction:: password
.. autofunction:: zlist
.. autofunction:: file_selection
.. autofunction:: calendar
.. autofunction:: color_selection
.. autofunction:: scale

.. toctree::
   :maxdepth: 2
   :caption: Contents:

