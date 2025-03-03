import logging
import os
import sys

from app import create_app

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

log = logging.getLogger("werkzeug")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s",
    handlers=[logging.StreamHandler()],
)


app = create_app()

# To run the project, run
# gunicorn --reload -w 2 -b 0.0.0.0:5000 run:app
