import logging

from main import app

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(port=8080, debug=True, host="0.0.0.0")
