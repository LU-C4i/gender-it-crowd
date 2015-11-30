# Introduction

This README covers how to run the Lynks webserver on UNIX based systems.

# Installation on Ubuntu

This assumes that Ubuntu still uses Python2.7

    sudo apt-get install python-setuptools
    sudo apt-get install build-essential python-dev \
        libsqlite3-dev libreadline6-dev \
        libgdbm-dev zlib1g-dev libbz2-dev sqlite3 zip
    sudo easy_install pip
    sudo apt-get install libmysqlclient-dev

    sudo pip install virtualenv
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

    sudo apt-get install mysql-server
    sudo apt-get install gawk
    pip install pyvirtualdisplay

    cp config/local.socketio.cfg webserver.cfg

    make reset-db
    make handlebars
    make run

	
## [Setting up virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

Use the following commands to setup the virtual environment:

    sudo pip install virtualenv
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    # Did not manage to install this using pip
    easy-install greenlet

## Configuring

The `config/` folder contains example configuration files. One of these must be
copied to the root directory of the project, and needs to be named
`webserver.cfg`.

    cp config/local.socketio.cfg webserver.cfg

Consult the configuration itself for more information.

# Running

The makefile provides aliases for often used commands. First reset the DBMS
(WARNING: do not do this if you have valuable data in ANY database. See the
section on setting up separate DBMS instances.) using `make reset-db`.

After resetting the database, the server can be started using `make run`,
provided that you followed the steps before.

