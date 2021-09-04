"""Listener module."""
from sys import platform as _platform
from os import environ
import json

from flask import Flask, request
from send_skype_message import send_message_bitbucket
app = Flask(__name__)

# check for ngrok subdomain
ngrok = environ.get("NGROK_SUBDOMAIN", "")


def display_intro():
    """Helper method to display introduction message."""
    if ngrok:
        message = "".join([
            "You can access this webhook publicly via at ",
            "http://%s.ngrok.io/webhook. \n" % ngrok,
            "You can access ngrok's web interface via http://localhost:4040"
        ])
    else:
        message = "Webhook server online! Go to http://localhost:5000"
    print(message)


def display_html(request):
    """
    Helper method to display message in HTML format.

    :param request: HTTP request from flask
    :type  request: werkzeug.local.LocalProxy
    :returns message in HTML format
    :rtype basestring
    """
    url_root = request.url_root
    if ngrok:
        return "".join([
            """Webhook server online! Go to """,
            """<a href="https://bitbucket.com">Bitbucket</a>""",
            """ to configure your repository webhook for """,
            """<a href="http://%s.ngrok.io/webhook">""" % ngrok,
            """http://%s.ngrok.io/webhook</a> <br />""" % ngrok,
            """You can access ngrok's web interface via """,
            """<a href="http://localhost:4040">http://localhost:4040</a>"""
        ])
    else:
        return "".join([
            """Webhook server online! """,
            """Go to <a href="https://bitbucket.com">Bitbucket</a>""",
            """ to configure your repository webhook for """,
            """<a href="%s/webhook">%s/webhook</a>""" % (url_root, url_root)
        ])


@app.route("/", methods=["GET"])
def index():
    """Endpoint for the root of the Flask app."""
    return display_html(request)


@app.route("/webhook", methods=["GET", "POST"])
def tracking():
    """Endpoint for receiving webhook from bitbucket."""
    if request.method == "POST":
        data = request.get_json()
        if request.headers.get("X-Event-Key") == "pullrequest:comment_created":
            comment_content = data["comment"]["content"]["raw"]
            pullrequest_author = data["pullrequest"]["author"]["display_name"]
            pullrequest_link = data["pullrequest"]["links"]["html"]["href"]
            comment_actor = data["actor"]["display_name"]
            send_message_bitbucket(f'''Commenter: {comment_actor}
Pull-request: {pullrequest_link}
Author: {pullrequest_author}
Content: {comment_content}''')
        else:
            commit_author = data["actor"]
            commit_hash = data["push"]["changes"][0]["new"]["target"]["hash"][:7]
            commit_url = data["push"]["changes"][0]["new"]["target"]["links"]
            commit_url = commit_url["html"]["href"]
            print("Webhook received! %s committed %s" % (commit_author,
                                                         commit_hash))
        return "OK"
    else:
        return display_html(request)


if __name__ == "__main__":
    display_intro()
    app.run(host="0.0.0.0", port=5000, debug=True)
