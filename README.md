# Karaoke Party

Karaoke Party is a web app that runs DIY karaoke so you don't have to. Who
needs a DJ?

Currently under rapid development. Check back soon 🎤 🎉

# Installation

## Requirements

Os-level requirements:
- PostgreSQL

Install Python requirements with pipenv:

```python
pipenv install
```

Or the old fashioned way, with pip:

```python
pip install -U -r requirements.txt
```

## Set up

Make a Postgres database:

```
createdb karaoke
```

Create the tables:

```
export FLASK_APP=karaoke/__init__.py
flask initdb
```

You're ready to start the server:

```
python runserver.py
```
