ORCID integration
==========================

This is a plugin for `pretalx`_, connecting pretalx users with ORCID. It adds
an additional, non-mandatory step in the CfP process, allowing submitters to
connect their ORCID account with their pretalx account.

Consequently, their name (as separate first and last name), their biography,
their title, and their organisation will be pre-filled from ORCID data.
(Additional data fields can be added – please open a PR if you are missing a
field!)

Development setup
-----------------

1. Make sure that you have a working `pretalx development setup`_.

2. Clone this repository, eg to ``local/pretalx-orcid``.

3. Activate the virtual environment you use for pretalx development.

4. Execute ``python setup.py develop`` within this directory to register this application with pretalx's plugin registry.

5. Execute ``make`` within this directory to compile translations.

6. Update your database scheme with ``python -m pretalx migrate``.

7. Restart your local pretalx server. You can now use the plugin from this repository for your events by enabling it in
   the 'plugins' tab in the settings.


License
-------

Copyright 2019 Tobias Kunze

Released under the terms of the Apache License 2.0


.. _pretalx: https://github.com/pretalx/pretalx
.. _pretalx development setup: https://docs.pretalx.org/en/latest/developer/setup.html
