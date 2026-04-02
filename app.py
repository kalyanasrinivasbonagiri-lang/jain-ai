import os
import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from jain_ai.app_factory import create_app
from jain_ai.config import get_runtime_host, get_runtime_port
from jain_ai.constants.settings import APP_NAME
from jain_ai.utils.logging_utils import get_logger


app = create_app()
logger = get_logger(APP_NAME.lower().replace(" ", "_"))


def main():
    host = get_runtime_host()
    port = get_runtime_port()
    logger.info("%s starting on http://%s:%s", APP_NAME, host, port)
    app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    main()
