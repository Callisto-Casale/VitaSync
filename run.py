import logging
import os
import sys

from app import create_app

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

log = logging.getLogger("werkzeug")
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s: %(message)s",
    handlers=[logging.StreamHandler()],
)


def main():
    app = create_app()


if __name__ == "__main__":
    main()

# To run the project, run
# gunicorn -w 2 -b 0.0.0.0:5000 run:app
