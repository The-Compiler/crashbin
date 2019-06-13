Extending Crashbin
==================

To automate repetitive tasks, Crashbin can be extended with plugins. Plugins are
simple Python files in ``~/.crashbin/plugins`` (or in ``HOMEDIR/plugins`` if the
homedir location was changed).

Plugins can use the `Django signals mechanism <https://docs.djangoproject.com/en/2.2/topics/signals/>`_ to get notified on
certain events. Currently, only two such events are available:

.. automodule:: crashbin_app.signals
   :members: new_report, bin_assigned

A minimal example plugin which reacts on those events could look like this:

.. literalinclude:: simpleplugin.py
   :language: python

Crashbin's model classes can be used by Plugins as `Django models <https://docs.djangoproject.com/en/2.2/topics/db/models/>`_:

.. autoclass:: crashbin_app.models.Report
   :members: all_messages, assign_to_bin

.. autoclass:: crashbin_app.models.Bin
   :members: get_inbox

.. autoclass:: crashbin_app.models.Label

For example, the following plugin moves any new report with a title such as "Exception: Forced crash" into the bin named "Forced crashes":

.. literalinclude:: autoplugin.py
   :language: python
