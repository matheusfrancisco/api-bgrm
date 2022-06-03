# API backend to image
This application contains all our backend application

##  Run Local

* Install python3.10
* Install poetry

Then run the following commands to bootstrap your environment with ``poetry``: ::

    poetry install
    poetry shell
    poetry run uvicorn --host=0.0.0.0 app.main:app --reload

Then create ``.env`` file (or rename and modify ``.env.example``) in project root and set environment variables for application: ::

Run tests
---------

To run all the tests of a project, simply run the ``pytest`` command: ::

    $ pytest



Web routes
----------

All routes are available on ``/docs`` or ``/redoc`` paths with Swagger or ReDoc.


Project structure
-----------------

Files related to application are in the ``app`` or ``tests`` directories.
Application parts are:
::

    app
    ├── api                 - web related stuff.
    │   └── routes          - web routes.
    │   └── logic           - pure functions.
    │   └── db              - pure migrations db
    │   └── types 
    │       └── models.py   - types annotations
    ├── core                - application configuration, startup events, logging.
    └── main.py             - FastAPI application creation and configuration.


