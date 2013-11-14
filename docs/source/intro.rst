
Introduction
============


python-zenity is a library for python wich inspired by Zenity. When you write scripts, you can use python-zenity to create simple dialogs that interact graphically with the user.

Requirements
************

* Python 2.x (x>6)
* PyGTK

Installation
************

Install using pip :

.. code-block:: bash

  $ pip install python-zenity

Or clone the repo :

.. code-block:: bash

  $ hg clone http://bitbucket.org/poulp/python-zenity
  $ cd python-zenity/
  $ python setup.py install

Example
*******

Simple dialog :

.. code-block:: python

  from pythonzenity import Calendar
  result = Calendar(title="Awesome Calendar",text_info="Your birthday ?")
  print result

This code show a calendar dialog :

.. image:: http://i.imgbox.com/abfd26Vb.png
  :align: center

And display the result :

.. code-block:: python

  $ python test.py
  $ (2013, 7, 8)
