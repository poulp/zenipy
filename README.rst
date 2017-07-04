.. image:: https://badge.fury.io/py/zenipy.png
    :target: http://badge.fury.io/py/zenipy

.. image:: https://readthedocs.org/projects/zenipy/badge/?version=latest
    :target: http://zenipy.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Zenipy
******

Zenipy is a library for python wich inspired by Zenity. When you write scripts,
you can use Zenipy to create simple dialogs that interact graphically with the user.

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
    
.. image:: docs/images/screen.png
    :align: center

And display the result :

.. code-block:: bash

    $ python test.py
    $ (year=2017, month=6, day=4)

There is more dialog, checkout the documentation !
