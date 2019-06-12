Integrating Crashbin
====================

Crashbin exposes a HTTP REST API to collect reports from applications. Since the
API is very simple to use, there is no client-side ``crashbin`` library needed to
report crashes to Crashbin.

Each report contains a mandatory title (such as a short text describing the
exception which occurred), as well as an optional debug log and the reporter's
email address.

Reports should be sent as a POST request to
https://crashbin.example.com/api/report/new/ (including the trailing slash!),
with the following fields:

- ``title`` (The title to use, mandatory)
- ``log`` (Debug log, optional)
- ``email`` (The reporter's email address, optional)

As an example, here's how unhandled exception reports could be sent to Crashbin
from Python, using the `requests <http://python-requests.org/>`_ HTTP library:

.. literalinclude:: integrating.py
   :language: python
   :linenos:
   :emphasize-lines: 7-11

On line 7, an exception handler is defined, which uses the Python
:py:mod:`traceback` module to get a suitable title and stacktrace text. It
then submits the crash log to Crashbin and calls the original Python excepthook.
Similarly, the exception hook could prompt the user for their email address and
further information.

.. warning::

   Code in exception hooks must be carefully written in order to not trigger additional exceptions. Otherwise, the exception hook will not finish, and thus no report will be received by Crashbin.

Submitting reports is possible in any language which supports handling crashes, such as JavaScript with Node.JS:

.. literalinclude:: integrating.js
   :language: javascript
   :linenos:
   :emphasize-lines: 4-9
