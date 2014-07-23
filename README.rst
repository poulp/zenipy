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

+------------------------+-----------------------+--------+
| Param                  |  Description          | Type   |
+========================+=======================+========+
| title                  | title of the window   | string |
+------------------------+-----------------------+--------+
| width                  | window width          | int    |
+------------------------+-----------------------+--------+
| height                 | window height         | int    |
+------------------------+-----------------------+--------+
| timeout                | in millisecond        | int    |
+------------------------+-----------------------+--------+

Example : 

.. code-block:: python

    Message(title="Close in 5 seconds !", width=800, height=600, timeout=5000)

    
Widgets
=======

Message
-------

Display a simple message

+------------------------+-----------------------+--------+
| Param                  |  Description          | Type   |
+========================+=======================+========+
| text                   | text inside the window| string |
+------------------------+-----------------------+--------+

Example : 

.. code-block:: python

    Message(text="Message in the bottle")

Error
-----

Display a simple message as an error

+------------------------+-----------------------+--------+
| Param                  |  Description          | Type   |
+========================+=======================+========+
| text                   | text inside the window| string |
+------------------------+-----------------------+--------+

Example : 

.. code-block:: python

    Error(text="Something wrong!")

Warning
-------

Display a simple message as an warning

+------------------------+-----------------------+--------+
| Param                  |  Description          | Type   |
+========================+=======================+========+
| text                   | text inside the window| string |
+------------------------+-----------------------+--------+

Example : 

.. code-block:: python

    Warning(text="This operation will delete your computer from the universe")

Question
--------

Display a question, possible answer are yes/no. Return the answer as a boolean

+------------------------+-----------------------+--------+
| Param                  |  Description          | Type   |
+========================+=======================+========+
| text                   | text inside the window| string |
+------------------------+-----------------------+--------+

Example : 

.. code-block:: python

    Question(text="Are you in love with me ?")

Entry
-----

Display a text input, return value as a string

+------------------------+--------------------------+---------+
| Param                  |  Description             | Type    |
+========================+==========================+=========+
| text                   | text inside the window   | string  |
+------------------------+--------------------------+---------+
| entry_text             | placeholder for the input| string  |
+------------------------+--------------------------+---------+

Example : 

.. code-block:: python

    Entry(text="1 + 1 ?", entry_text="2")

Password
--------

Display a text input with hidden characters, return value as a string.

+------------------------+--------------------------+---------+
| Param                  |  Description             | Type    |
+========================+==========================+=========+
| text                   | text inside the window   | string  |
+------------------------+--------------------------+---------+
| entry_text             | placeholder for the input| string  |
+------------------------+--------------------------+---------+

Example : 

.. code-block:: python

    Password(text="Need to be authenticated : ")
    
Calendar
--------

+------------------------+--------------------------+---------+
| Param                  |  Description             | Type    |
+========================+==========================+=========+
| text_info              | text inside the window   | string  |
+------------------------+--------------------------+---------+
| day                    | default day              | int     |
+------------------------+--------------------------+---------+
| month                  | default month            | int     |
+------------------------+--------------------------+---------+

File selection
--------------

Open a file selection window, return path of files selected.

+------------------------+---------------------------------------------------+---------+
| Param                  |  Description                                      | Type    |
+========================+===================================================+=========+
| multiple               | multilple file selection, return a list of files  | boolean |
+------------------------+---------------------------------------------------+---------+
| directory              | only directory selection                          | boolean |
+------------------------+---------------------------------------------------+---------+
| save                   | save mode                                         | boolean |
+------------------------+---------------------------------------------------+---------+
| confir_overwrite       | confirm when a file is overwritten                | boolean |
+------------------------+---------------------------------------------------+---------+
| filename               | placeholder for the filename                      | string  |
+------------------------+---------------------------------------------------+---------+

Example : 

.. code-block:: python

    FileSelection(multiple=True)

Scale
-----

+------------------------+---------------------------------------------------+---------+
| Param                  |  Description                                      | Type    |
+========================+===================================================+=========+
| text_info              | text inside the window                            | string  |
+------------------------+---------------------------------------------------+---------+
| value                  | current value                                     | int     |
+------------------------+---------------------------------------------------+---------+
| min                    | minimum value                                     | int     |
+------------------------+---------------------------------------------------+---------+
| max                    | maximum value                                     | int     |
+------------------------+---------------------------------------------------+---------+
| step                   | incrementation value                              | int     |
+------------------------+---------------------------------------------------+---------+
| draw_value             | hide/show cursor value                            | boolean |
+------------------------+---------------------------------------------------+---------+

Example : 

.. code-block:: python

    Scale(value=50, min=10, max=110, step=10)

Color selection
---------------

+------------------------+---------------------------------------------------+---------+
| Param                  |  Description                                      | Type    |
+========================+===================================================+=========+
| show_palette           | hide/show the palette                             | boolean |
+------------------------+---------------------------------------------------+---------+

Example : 

.. code-block:: python

    ColorSelection(show_palette=True)





