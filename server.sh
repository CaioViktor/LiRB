#!/bin/bash
# gunicorn --bind 0.0.0.0:1111 --log-level=debug --workers 4 --timeout 0 wsgi:app
gunicorn --bind 10.33.96.18:1113 --log-level=debug --workers 4 --timeout 0 wsgi:app  #Colocar IP da máquina hospedeira (Servidor) aqui