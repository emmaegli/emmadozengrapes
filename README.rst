.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style

Celery
----------------

This app comes with Celery.

To run a celery worker:

.. code-block:: bash

    celery -A config.celery_app worker -l info

Please note: For Celery's import magic to work,
it is important *where* the celery commands are run.
If you are in the same folder with *manage.py*, you should be right.

---------------------------------------------

Deployment
----------------

The following details how to deploy this application.

Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html
