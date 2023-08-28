Tinyfy
======

Esta é uma aplicação para gerar urls encurtadas.
Está implementado uma interface web e também uma

A implementação da solução desta aplição se dá a partir de um gerador de hash que usa como base um número de entrada que é único e controlado pela aplicação.
Desta forma nos permite escalar horizontalmente os servidores de aplicação para suportar uma alta escala sem perder consistência.
Este contador é controlado por um serviço REDIS que tem a funcionalidade de contador atomico necessário para que a solução funcione em alta escala.
Com o contador único em mãos utilizamos a lib https://sqids.org/ para gerar o hash.


.. _tutorial: https://github.com/victorhcf/tinyfy


Install
-------

**Be sure to use the same version of the code as the version of the docs
you're reading.** You probably want the latest tagged version, but the
default Git version is the main branch. ::

    # clone the repository
    $ git clone https://github.com/victorhcf/tinyfy
    $ cd flask
    # checkout the correct version
    $ git tag  # shows the tagged versions
    $ git checkout latest-tag-found-above
    $ cd examples/tutorial

Create a virtualenv and activate it::

    $ python3 -m venv .venv
    $ . .venv/bin/activate

Or on Windows cmd::

    $ py -3 -m venv .venv
    $ .venv\Scripts\activate.bat

Install Flaskr::

    $ pip install -e .

Or if you are using the main branch, install Flask from source before
installing Flaskr::

    $ pip install -e ../..
    $ pip install -e .


Run
---

.. code-block:: text

    $ flask --app flaskr init-db
    $ flask --app flaskr run --debug

Open http://127.0.0.1:5000 in a browser.


Test
----

::

    $ pip install '.[test]'
    $ pytest

Run with coverage report::

    $ coverage run -m pytest
    $ coverage report
    $ coverage html  # open htmlcov/index.html in a browser
