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

Make a local settings file:

```
cat karaoke/settings_local.example.py > karaoke/settings_local.py
```

If you're developing locally, you should be fine leaving the example settings file
as is.

Make a database:

```
createdb karaoke
```

Run database migrations:

```
python manage.py migrate
```

