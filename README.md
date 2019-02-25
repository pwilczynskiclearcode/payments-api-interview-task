Design
------

[Design](./DESIGN.pdf)

Installation
------------

Prerequisite:
* Docker compose https://docs.docker.com/compose/install/

Build entire project:

    $ docker-compose build

It may take up to 5 minutes.

Run the tests to make sure that project is ready to be used:

    $ docker-compose up tests

(it should exit 0 with no errors)

Start web server (running on :8000 port) and the database.

    $ docker-compose start web

Now you can open http://0.0.0.0:8000/swagger/ showing the API swagger interactive UI.