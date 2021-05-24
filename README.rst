ESNPolimi-mgmt
==============

ESN Politecnico Milano Management Site

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


:License: BSD

Setup
-----

1. Create and activate a python virtual environment

2. Install development dependencies::

      pip install -r requirements/local.txt

3. Install precommit::

      pre-commit install
      pre-commit install --hook-type commit-msg

4. Set local environment variables::

      source .envs/.local/.postgres
      export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
      export USE_DOCKER="yes"

5. Install `mkcert` (details_ per platform) and run::

      mkcert -install
      mkcert local "*.local" localhost 127.0.0.1 ::1

   Move the new `.pem` files in current directory to a `./certs/` folder in the project.

6. Finally build docker images::

      docker-compose -f local.yml build

7. (Optional) Add domain name to the host file (usually /etc/hosts) for ease of access::

      127.0.0.1        mgmt.esnpolimi.local    localhost

   as last line if the file.

Check this page_ for details.

.. _page: https://cookiecutter-django.readthedocs.io/en/latest/developing-locally-docker.html
.. _details: https://github.com/FiloSottile/mkcert

Run application
---------------

In order to run the whole stack use::

   docker-compose -f local.yml up -d

The first time it will take a while, wait until :code:`docker-compose -f local.yml logs django` says otherwise.
You could need to make the database migrations if the last ones have not been committed yet, in such cases run::

   ./delete_migrations.sh

or, if you didn't follow the optional step 7::

    docker-compose -f local.yml exec django bash -c 'delete_migrations.sh'

Email Server
^^^^^^^^^^^^

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server `MailHog`_ with a web interface is available as docker container.

Container mailhog will start automatically when you will run all docker containers.
Please check `cookiecutter-django Docker documentation`_ for more details how to start all containers.

With MailHog running, to view messages that are sent by your application, open your browser and go to ``http://localhost:8025``

.. _mailhog: https://github.com/mailhog/MailHog

Deployment
----------

Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html
