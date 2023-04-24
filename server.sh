#!/bin/bash
gunicorn --bind 0.0.0.0:1111 --log-level=debug --workers 4 --timeout 0 wsgi:app #Put IP host (Server) here