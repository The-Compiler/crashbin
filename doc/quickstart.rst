Getting started
===============

Installing Crashbin
-------------------

Crashbin is a normal Python package, and as such, can be installed using the
``pip`` package manager. See the `Python Packaging User Guide
<https://packaging.python.org/tutorials/installing-packages/>`_ for details on
setting up pip.

Currently, no stable release has been pushed to `PyPI <https://pypi.org/>`_ (the
Python Package Index) yet. However, pip can be used to install directly from
GitHub::

  pip install git+https://github.com/The-Compiler/crashbin.git

Starting Crashbin
-----------------

To set up an initial database, add a new user, and run Django's integrated
development server, use::

  python manage.py migrate
  python manage.py createsuperuser
  python manage.py runserver

Then, navigate to http://localhost:8000/ to access Crashbin.

On a production system, it's recommended to set up a proper webserver to run Crashbin with WSGI, see the `Django deployment documentation <https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/>`_ for examples. Popular choices for servers include Apache (with ``mod_wsgi``), Gunicorn or uWSGI.

Basic configuration
-------------------

See :doc:`configuring` for detailed instructions on all available settings. When
setting up Crashbin on a production system, it's recommended to change the
following settings:

- If Crashbin should use an existing SQL server (like MariaDB or PostgreSQL), adjust the ``DATABASE`` setting accordingly.
- Adjust the ``EMAIL`` settings to be able to send and receive mails in Crashbin. Also, adjust the subjects used to match your project.
- Replace ``SECRET_KEY`` by a new, unique, secret key. You can use::

    python -c 'from django.core.management import utils; print(utils.get_random_secret_key())'

  to generate such a key.
- Turn off ``DEBUG``.
- Add the host used to serve crashbin to ``ALLOWED_HOSTS``.

Basic Concepts
--------------

It's useful to understand the following basic concepts how Crashbin organizes data:

- An application crashes and sends a new report to Crashbin. See :doc:`integrating` for details on how this happens.
- Crashbin collects the report and puts it into the configured "Inbox bin".
- Bins are "containers" used to organize reports which are similar in some way.
  As an example, you could create a bin to collect all reports caused by a
  particular bug, or to group all reports related to a certain subsystem.
- Based on the information in the report, it should be moved from the inbox bin
  into the correct bin, or a new bin should be created for it.
- Both bins and reports can be tagged by using labels, for example to mark reports from an important customer.
- When viewing a report, it's possible to reply to the user who sent it using
  the Crashbin webinterface. Similarly, internal notes can be taken, which
  aren't sent to the user.
