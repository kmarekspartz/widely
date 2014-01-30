widely
======

Static Site as a Service using AWS S3
-------------------------------------

Widely makes deploying static websites easy!

Usage
~~~~~

::

    mkdir www.hello-world.com
    echo 'Hello world!' > www.hello-world.com/index.html
    cd www.hello-world.com
    widely sites:create www.hello-world.com
    widely open

Installation
~~~~~~~~~~~~

::

    pip install widely

If your ``pip`` is ``pip-3``:

::

    pip-2.7 install widely

``widely`` was developed on Python 2.7.5 on Mac OS X, but it should work
on any system with Python 2.7.

Compatibility with Python 3 and 2.6 is planned.

Heroku toolbelt-style command line tool
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Built using ``docopt``, ``prettytable``, ``boto``, ``feedparser``

Issues
~~~~~~

-  Python 3 and 2.6 compatibility
-  Use S3's logging
-  Support multipart etags (or add in our own metadata)
-  Don't use MD5
-  Better globs
-  Port not being released quickly in ``widely local``
-  Serving compressed files from S3
-  Use Amazon CloudFront and Route 53
-  Tests!

MIT License
~~~~~~~~~~~

-  http://www.github.com/zeckalpha/widely

Contact
~~~~~~~

-  kms@celador.mn
-  http://www.celador.mn/widely

