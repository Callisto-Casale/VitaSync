import logging

from app import create_app

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

app = create_app()

# To run the project, execute
# gunicorn -w 2 -b 0.0.0.0:5000 run:app
