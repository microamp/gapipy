# gapipy #

Google API handler with command line interface

## Installation ##

Clone the repo and set up a virtual environment as below.

```
$ git clone git@github.com:microamp/gapipy.git
$ cd gapipy
$ virtualenv --python=python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Environment Variables ##

|Environment Variable    |Description                                             |
|------------------------|--------------------------------------------------------|
|`GAPIPY_SERVICE_ACCOUNT`|service account [1]                                     |
|`GAPIPY_PEM_FILE_PATH`  |path to the pem file associated with the service account|

Links:

1. https://developers.google.com/identity/protocols/OAuth2ServiceAccount

## Command Line Arguments ##

```
$ python gapipy.py --help
```
```
Usage: gapipy.py [OPTIONS] USER API METHOD VERSION

Options:
  --scopes-path TEXT      default: scopes.txt
  --req-params-path TEXT  default: req-params.json
  --help                  Show this message and exit.
```

## Examples ##

1. [`users:list` v1](https://developers.google.com/admin-sdk/directory/v1/reference/users/list#request)
```
$ python gapipy.py admin@example.com users list v1 \
--scopes-path=scopes.txt --req-params-path=req-params-users.json
```
2. [`about.get` v3](https://developers.google.com/drive/v3/reference/about/get#request)
```
$ python gapipy.py microamp@example.com about get v3 \
--scopes-path=scopes.txt --req-params-path=req-params-about.json
```
3. [`changes.list` v2](https://developers.google.com/drive/v2/reference/changes/list)
```
$ python gapipy.py microamp@example.com changes list v2 \
--scopes-path=scopes.txt --req-params-path=req-params-changes.json
```
