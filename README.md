sikuli_cpython
==============

A CPython wrapper around the sikuli standalone jar

Why
---
Sikuli is traditionally written in Jython, which is painful if you want to mix it with Selenium scripts. This module makes it possible for CPython to run the Jython scripts created by Sikuli-IDE.

How it works
------------
This module wraps the sikuli standalone jar using [pyjnius](https://github.com/kivy/pyjnius) from the Kivy project. Pyjnius allows us to use java classes in CPython.