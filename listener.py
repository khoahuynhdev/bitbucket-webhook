"""Listener module."""
from sys import platform as _platform
from os import environ
from dateutil import parser
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
        event_key = request.headers.get("X-Event-Key")
        if event_key == "pullrequest:comment_created":
            comment_content = data["comment"]["content"]["raw"]
            pullrequest_author = data["pullrequest"]["author"]["display_name"]
            pullrequest_link = data["pullrequest"]["links"]["html"]["href"]
            comment_actor = data["actor"]["display_name"]
            send_message_bitbucket(f'''Commenter: {comment_actor}
Pull-request: {pullrequest_link}
Author: {pullrequest_author}
Content: {comment_content}''')

        if event_key == "repo:push":
            commit_author = data["push"]["changes"][0]["new"]["target"]["author"]["raw"]
            commit_link = data["push"]["changes"][0]["new"]["target"]["links"]["html"]["href"]
            commit_date = data["push"]["changes"][0]["new"]["target"]["date"]
            commit_message = data["push"]["changes"][0]["new"]["target"]["message"]
            repository_name = data["repository"]["full_name"]

            formatted_date = parser.parse(commit_date).strftime('%c')
            send_message_bitbucket(f'''=====PUSH COMMIT CREATED=====
Author: {commit_author}
Repository: {repository_name}
Commit link: {commit_link}
Commit date: {formatted_date}
Commit message: {commit_message}''')

        # @TODO add all pull request reviewers
        # @TODO add all pull request participants
        if event_key == "pullrequest:created" or event_key == "pullrequest:updated":
          pullrequest_author = data["actor"]["display_name"]
          pullrequest_title = data["pullrequest"]["title"]
          pullrequest_state = data["pullrequest"]["state"]
          pullrequest_source = data["pullrequest"]["source"]["branch"]["name"]
          pullrequest_destination = data["pullrequest"]["destination"]["branch"]["name"]
          pullrequest_created_date = data["pullrequest"]["created_on"]
          pullrequest_link = data["pullrequest"]["links"]["html"]["href"]
          formatted_date = parser.parse(pullrequest_created_date).strftime('%c')
          send_message_bitbucket(f'''=====PULL REQUEST CREATED=====
Author: {pullrequest_author}
PR title: {pullrequest_title}
PR branch: {pullrequest_source} ===>>> {pullrequest_destination}
PR state: {pullrequest_state}
PR date : {formatted_date}
PR link: {pullrequest_link}''')

        if event_key == "pullrequest:changes_request_created":
          pullrequest_author = data["actor"]["display_name"]
          pullrequest_title = data["pullrequest"]["title"]
          pullrequest_state = data["pullrequest"]["state"]
          pullrequest_source = data["pullrequest"]["source"]["branch"]["name"]
          pullrequest_destination = data["pullrequest"]["destination"]["branch"]["name"]
          pullrequest_link = data["pullrequest"]["links"]["html"]["href"]
          pullrequest_change_request_created_date = data["changes_request"]["date"]
          pullrequest_change_request_requestee = data["changes_request"]["user"]["display_name"]
          formatted_date = parser.parse(pullrequest_change_request_created_date).strftime('%c')
          send_message_bitbucket(f'''=====CHANGE REQUEST CREATED=====
Author: {pullrequest_author}
PR title: {pullrequest_title}
PR branch: {pullrequest_source} ===>>> {pullrequest_destination}
PR change request requestee: {pullrequest_change_request_requestee}
PR change request date: {formatted_date}
PR link: {pullrequest_link}''')
        return "OK"
    else:
        return display_html(request)


if __name__ == "__main__":
    display_intro()
    app.run(host="0.0.0.0", port=5000, debug=True)
