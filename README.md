## What is CompDays Recorder ?

This is a simple Gtk application developed with quickly. The purpose is to build a tool that keeps track of working overtimes and computes compensation days.

## Installation
For the time being there is no official release since the project is under development. If you still want to run *CompDays Recorder*, you will need to install some dependencies.

### Dependencies
- ```python 2.7``` or higher
- ```matplotlib``` version 1.2.0 or higher
- ```quickly``` the ultimate development tool from Canonical :-)

Under Ubuntu, ```quickly``` can be simply installed by

```bash
$ sudo apt-get install quickly
```

Beware that if you are running **Ubuntu below 13.04** (*Raring Ringtail*) the version of ```matplotlib``` provided on the universe repository is a bit outdated (1.1.1 at the time this is written). So please follow the setup instructions on the [official website](http://matplotlib.org/users/installing.html#installing-from-source).

If you are running **Ubuntu 13.04 or higher**, the packet has been updated and you can simply run ```sudo apt-get install python-matplotlib```.

In order to make sure you have the right version, open a terminal and do

```
$ python
Python 2.7.4 (default, Sep 26 2013, 03:20:26) 
[GCC 4.7.3] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import matplotlib
>>> matplotlib.__version__   # make sure you have a version above 1.2.0
'1.2.1'   # OK
```

### Run it !
Just clone the git repo on your own machine. Then at the root of the project do

```
$ quickly run
```
this is that simple :-)


## Target platforms

The application is developed for Ubuntu. Other platforms might be supported in the future.
