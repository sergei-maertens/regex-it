Regex-IT website
================

Website for https://regex-it.nl.

[![Build Status](https://travis-ci.org/sergei-maertens/regex-it.svg?branch=develop)](https://travis-ci.org/sergei-maertens/regex-it)

[![Build Status](https://travis-ci.org/sergei-maertens/regex-it.svg?branch=develop)](https://travis-ci.org/sergei-maertens/regex-it)

[![Coverage Status](https://coveralls.io/repos/sergei-maertens/regex-it/badge.svg?branch=develop&service=github)](https://coveralls.io/github/sergei-maertens/regex-it?branch=develop)

[![Requirements Status](https://requires.io/github/sergei-maertens/regex-it/requirements.svg?branch=develop)](https://requires.io/github/sergei-maertens/regex-it/requirements/?branch=develop)


Getting started
---------------

The python dependencies for development are easily installed with:

    pip install -r requirements/dev.txt

Create the database, default settings are in `regex.conf.settings.dev`.
Postgres 9.4 is used by default.

For the front-end tools, `nodejs` and `npm` are required, install them
with your favourite package manager.

Next, install the global build tools if not present yet:

    npm install grunt-cli bower -g

And install the project dev dependencies:

    npm install
    bower install

To watch the sass files and recompile sass to css on the fly, run:

    grunt


You can now fire up the development server:

    src/manage.py runserver --settings=regex.conf.settings.dev


Deployment
----------
You need a python 2 virtualenvironment with `ansible` installed. It does not work (yet) on Py3.

    cd deployment
    ansible-playbook -i hosts deploy.yml -e "release_tag=<branch-or-tag> target=[staging|production]" --ask-vault-pass

