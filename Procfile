web: gunicorn capstone.wsgi --bind 0.0.0.0:$PORT --worker-class gevent --log-file -
worker: python manage.py runworker --settings=capstone.settings
