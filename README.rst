Producteev: Python API
======================

This is an awesome Python wrapper for the Github API.


Installation
------------

To install producteev, simply::

    $ pip install producteev

Or, if you absolutely must::

    $ easy_install producteev



Usage
-----

Create a new client instance::

    from producteev import Producteev

    client = Producteev("api_key_from_producteev","api_secret_from_producteev")


Login in as a user::

    client.login("username","password")

Get the server time::

    client.time

Get as list of tasks::

    client.tasks.list


Get as list of lables::

    client.labels.list

License
-------

Copyright (c) 2012 Martín García <newluxfero@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.