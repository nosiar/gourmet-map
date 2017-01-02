#!venv/bin/python

from app import app
application = app

if __name__ == "__main__":
    context = ('cert.pem', 'key.pem')
    application.run(host='0.0.0.0', ssl_context=context)
