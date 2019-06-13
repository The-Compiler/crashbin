Configuring Crashbin
====================

Crashbin includes a ``crashbin_settings_example.py`` file in its repository,
which contains all available settings with their default values. To configure
crashbin, copy that file to ``crashbin_settings.py`` and adjust the settings to
your liking.

The following settings are available:

- ``HOMEDIR`` (string or a :py:class:`pathlib.Path` object): The directory used by Crashbin to store its data. Default: ``~/.crashbin``.
- ``DATABASE``: (dict) The Django database settings. Refer to `DATABASES <https://docs.djangoproject.com/en/2.2/ref/settings/#databases>`_ in the Django documentation for details. Default: A sqlite database in ``HOMEDIR/db.sqlite3``.
- ``LANGUAGE_CODE``: (str) The language code to use. Refer to `LANGUAGE_CODE <https://docs.djangoproject.com/en/2.2/ref/settings/#language-code>`_ in the Django documentation for details. Note that Crashbin currently is only available in English. Default: ``en-us``.
- ``TIME_ZONE``: (str) The timezone to use. Refer to `TIME_ZONE <https://docs.djangoproject.com/en/2.2/ref/settings/#time-zone>`_ in the Django documentation for details. Default: ``Europe/Zurich``.
- ``MEDIA_ROOT``: (str or a :py:class:`pathlib.Path` object) The path used to store media files. Refer to `MEDIA_ROOT <https://docs.djangoproject.com/en/2.2/ref/settings/#media-root>`_ in the Django documentation for details. Default: ``HOMEDIR/media``.
- ``EMAIL``: (dict) A dictionary of email settings, with the following keys:

  * ``backend``: (str) The email backend to use for outgoing mails (``smtp``, ``console``, ``filebased``, ``locmem``, ``dummy``), see the section about `email backends <https://docs.djangoproject.com/en/2.2/topics/email/#email-backends>`_ in the Django documentation for details. Default: ``console``.
  * ``smtp_host`` (str), ``smtp_port`` (int): The server/port to connect to when using SMTP.
  * ``smtp_user`` (str), ``smtp_password`` (str): The SMTP credentials to use.
  * ``smtp_tls`` (bool): Whether to use TLS encryption for the SMTP connection.
  * ``incoming_url``: (str) The URL to use to fetch incoming mails, see the `django-mailbox documentation <https://django-mailbox.readthedocs.io/en/latest/topics/mailbox_types.html>`_ for details. If set to ``None`` (the default), mails can be supplied manually via ``manage.py processincomingmessage``.
  * ``outgoing_subject``: (str) The subject to use for outgoing messages. A ``{}`` placeholder is replaced by the report ID. Default: ``qutebrowser report #{}``
  * ``incoming_subject``: (str) A regex for incoming message subjects. The capture group needs to capture the report ID. If your ``outgoing_subject`` is ``example report #{}``, a sensible value would be ``.*example report #(.*)``. The initial ``.*`` accounts for added text such as ``Re:`` in incoming mails. Default: ``.*qutebrowser report #(.*)``
  * ``outgoing_address``: (str) The mail address to use for outgoing mails. Default: ``crashes@qutebrowser.org``

- ``SECRET_KEY``: (str) A randomly generated secret key to use for cryptographic signing. Refer to `SECRET_KEY <https://docs.djangoproject.com/en/2.2/ref/settings/#secret-key>`_ in the Django documentation for details. **Should be kept secret!**
- ``DEBUG``: (bool) Whether to enable debug features. Refer to `DEBUG <https://docs.djangoproject.com/en/2.2/ref/settings/#debug>`_ in the Django documentation for details. **Don't run with debug turned on in production!** Default: true
- ``ALLOWED_HOSTS``: (list of str) The hostnames allowed to serve this Django site. Refer to `ALLOWED_HOSTS <https://docs.djangoproject.com/en/2.2/ref/settings/#allowed-hosts>`_ in the Django documentation for details.
- ``CUSTOM_CSS``: (str) Custom CSS to add to every Crashbin page. Can be used to restyle its interface.
- ``INBOX_BIN``: (str) The name of the Bin to use for new reports. Default: ``Inbox``.
- ``LABEL_COLORS``: (list of str) Colors to suggest in the color picker when adding a new label.
