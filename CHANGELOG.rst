Change Log
----------

..
   All enhancements and patches to getsmarter-api-clients will be documented
   in this file.  It adheres to the structure of https://keepachangelog.com/ ,
   but in reStructuredText instead of Markdown (for ease of incorporation into
   Sphinx documentation and the PyPI description).
   
   This project adheres to Semantic Versioning (https://semver.org/).

.. There should always be an "Unreleased" section for changes pending release.

Unreleased
~~~~~~~~~~

*

[0.5.2]
~~~~~~~
* Include payload in error message

[0.5.1]
~~~~~~~
* Catch a `requests.HTTPError`, not an `urllib.error.HTTPError`.

[0.5.0] - 2023-04-12
~~~~~~~~~~~~~~~~~~~~

* Added new field for data_share_consent in enterprise_allocations

[0.4.0] - 2022-09-12
~~~~~~~~~~~~~~~~~~~~

* Add enterprise_allocations endpoint functionality to client

[0.1.0] - 2022-08-01
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* First release on PyPI.
