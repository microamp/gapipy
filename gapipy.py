#-*- coding: utf-8 -*-

from functools import reduce
from pprint import pformat
import json
import os

from oauth2client.client import SignedJwtAssertionCredentials
import click
import httplib2

ENV_SERVICE_ACCOUNT = "GAPIPY_SERVICE_ACCOUNT"
ENV_PEM_FILE_PATH = "GAPIPY_PEM_FILE_PATH"
BASE_URLS = {
    "users.list.v1": "https://www.googleapis.com/admin/directory/v1/users",
    "groups.list.v1": "https://www.googleapis.com/admin/directory/v1/groups",
    "members.list.v1": "https://www.googleapis.com/admin/directory/v1/groups/{groupKey}/members",
    "about.get.v3": "https://www.googleapis.com/drive/v3/about",
    "changes.list.v3": "https://www.googleapis.com/drive/v3/changes",
    "comments.list.v3": "https://www.googleapis.com/drive/v3/files/{fileId}/comments",
    "revisions.list.v3": "https://www.googleapis.com/drive/v3/files/{fileId}/revisions",
    "about.get.v2": "https://www.googleapis.com/drive/v2/about",
    "changes.list.v2": "https://www.googleapis.com/drive/v2/changes",
    "comments.list.v2": "https://www.googleapis.com/drive/v2/files/{fileId}/comments",
    "revisions.list.v2": "https://www.googleapis.com/drive/v2/files/{fileId}/revisions",
}


def _compose(*fns):
    def func(arg):
        return reduce(lambda v, fn: fn(v), fns, arg)

    return func


def _auth(service_account, private_key, scopes, **kwargs):
    credentials = SignedJwtAssertionCredentials(service_account,
                                                bytes(private_key, "utf-8"),
                                                scopes,
                                                **kwargs)
    credentials.refresh(httplib2.Http())
    return credentials.authorize(httplib2.Http())


def _do(http, base_url, req_params):
    params = "&".join("%s=%s" % (k, v,) for k, v in req_params.items())
    url = "%s%s" % (base_url.format(**req_params), "?%s" % params if params else "",)
    return url, http.request(url)


@click.command()
@click.argument("user")
@click.argument("api")
@click.argument("method")
@click.argument("version")
@click.option("--scopes-path", help="default: scopes.txt", default="scopes.txt")
@click.option("--req-params-path", help="default: req-params.json", default="req-params.txt")
def main(user, api, method, version, scopes_path, req_params_path):
    # API URL
    if "%s.%s.%s" % (api, method, version,) not in BASE_URLS:
        click.echo("Invalid API, method, and/or version: %s, %s, %s" % (api, method, version,))
        return
    base_url = BASE_URLS["%s.%s.%s" % (api, method, version,)]

    # Environment variables for service account and path to private key file
    service_account = os.environ.get(ENV_SERVICE_ACCOUNT, "")
    pem_file_path = os.environ.get(ENV_PEM_FILE_PATH, "")
    if not service_account:
        click.echo("Missing environment variable: %s" % ENV_SERVICE_ACCOUNT)
        return
    if not pem_file_path:
        click.echo("Missing environment variable: %s" % ENV_PEM_FILE_PATH)
        return
    click.echo("Service account: %s" % service_account)
    with open(pem_file_path, "r") as f:
        private_key = f.read()

    # Scopes
    with open(scopes_path, "r") as f:
        scopes = [line.replace("\n", "") for line in f.readlines()]

    # Request params
    with open(req_params_path, "r") as f:
        req_params = json.loads(f.read())

    # Do auth
    http = _auth(service_account, private_key, scopes, sub=user)

    # Make request
    url, (headers, body) = _do(http, base_url, req_params)
    click.echo("URL requested: %s" % url)

    click.echo("====headers====")
    click.echo(pformat(headers))
    click.echo("====body====")
    click.echo(_compose(json.loads, pformat)(body.decode("utf-8")))


if __name__ == "__main__":
    main()
