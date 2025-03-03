import logging

from app import create_app

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

    """
    Add ssl_context=('cert.pem', 'key.pem') to app.run to turn on SSL usage (HTTPS)
    """


# Test comment
# Test 2
# Test 3
