.. image:: https://badge.fury.io/py/python-zenity.png
    :target: http://badge.fury.io/py/python-zenity
    
python-zenity
*************

python-zenity is a library for python wich inspired by Zenity. When you write scripts, 
you can use python-zenity to create simple dialogs that interact graphically with the user.

Requirements
============

* Python 2.x (x>6)
* PyGTK

Installation
============

Install using pip :

.. code-block:: bash

    $ pip install python-zenity

Or clone the repo :

.. code-block:: bash

    $ git clone http://github.org/poulp/python-zenity.git
    $ cd python-zenity/
    $ python setup.py install

Example
================

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
    
    
Usage
=====

All the widgets have some common parameters :

+------------------------+-----------------------+
| Param                  |  Description          |
+========================+=======================+
| title                  | title of the window   |
+------------------------+-----------------------+
| width                  | window width          |
+------------------------+-----------------------+
| height                 | window height         |
+------------------------+-----------------------+
| timeout                | in millisecond        |
+------------------------+-----------------------+

Example : 

.. code-block:: python

    Message(title="Close in 5 seconds !", width=800, height=600, timeout=5000)

    
Widgets
=======

Message
-------

Display a simple message

+------------------------+-----------------------+
| Param                  |  Description          |
+========================+=======================+
| text                   | text inside the window|
+------------------------+-----------------------+

Example : 

.. code-block:: python

    Message(text="Message in the bottle")

Error
-----

Display a simple message as an error

+------------------------+-----------------------+
| Param                  |  Description          |
+========================+=======================+
| text                   | text inside the window|
+------------------------+-----------------------+

Example : 

.. code-block:: python

    Error(text="Something wrong!")

Warning
-------

Display a simple message as an warning

+------------------------+-----------------------+
| Param                  |  Description          |
+========================+=======================+
| text                   | text inside the window|
+------------------------+-----------------------+

Example : 

.. code-block:: python

    Warning(text="This operation will delete your computer from the universe")

Question
--------

Display a question, possible answer are yes/no. Return the answer as a boolean

+------------------------+-----------------------+
| Param                  |  Description          |
+========================+=======================+
| text                   | text inside the window|
+------------------------+-----------------------+

Example : 

.. code-block:: python

    Question(text="Are you in love with me ?")

Entry
-----

Display a text input, return value as a string

+------------------------+--------------------------+
| Param                  |  Description             |
+========================+==========================+
| text                   | text inside the window   |
+------------------------+--------------------------+
| entry_text             | placeholder for the input|
+------------------------+--------------------------+

Example : 

.. code-block:: python

    Entry(text="1 + 1 ?", entry_text="2")

Password
--------

Display a text input with hidden characters, return value as a string.

+------------------------+--------------------------+
| Param                  |  Description             |
+========================+==========================+
| text                   | text inside the window   |
+------------------------+--------------------------+
| entry_text             | placeholder for the input|
+------------------------+--------------------------+

Example : 

.. code-block:: python

    Password(text="Need to be authenticated : ")

File selection
--------------

Scale
-----

Color selection
---------------






