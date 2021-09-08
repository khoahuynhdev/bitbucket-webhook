#!/usr/bin/env bash

set -e

if [ "$PAM_TYPE" != "close_session" ]; then
  host="$(hostname)"
  curl -d '{"user":"'$PAM_USER'", "user_host":"'$PAM_RHOST'", "host": "'$host'"}' -H "Content-Type: application/json" -X POST http://209.97.168.191:8000/ssh &
fi
