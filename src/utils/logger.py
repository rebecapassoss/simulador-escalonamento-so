import logging
import os

def setup_logger():

    os.makedirs("outputs/logs", exist_ok=True)

    logging.basicConfig(
        filename="outputs/logs/simulator.log",
        level=logging.INFO,
        format="%(asctime)s - %(message)s"
    )

    return logging.getLogger()