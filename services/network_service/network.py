"""
============================================================
Project : Noor AI Home Platform
Module  : Network Service
Version : 1.0.0
============================================================
"""

import socket
import time

import requests

from shared.logger import logger
from shared.config_manager import load_config


class NetworkService:

    def __init__(self):

        config = load_config()

        server = config.get("server", {})

        brain = config.get("brain", {})

        self.host = server.get("host", "0.0.0.0")

        self.port = server.get("port", 8000)

        self.brain_url = brain.get(
            "url",
            "http://127.0.0.1:9000"
        )

        self.timeout = 3

    # -----------------------------------------------------

    def internet(self):

        try:

            socket.create_connection(

                ("8.8.8.8", 53),

                timeout=self.timeout

            )

            return True

        except Exception:

            return False

    # -----------------------------------------------------

    def ping(self, url):

        start = time.time()

        try:

            r = requests.get(

                url,

                timeout=self.timeout

            )

            elapsed = (

                time.time() - start

            ) * 1000

            return {

                "online": r.status_code == 200,

                "status_code": r.status_code,

                "latency_ms": round(

                    elapsed,

                    2

                )

            }

        except Exception as ex:

            return {

                "online": False,

                "error": str(ex)

            }

    # -----------------------------------------------------

    def brain(self):

        return self.ping(

            self.brain_url + "/health"

        )

    # -----------------------------------------------------

    def camera(self):

        return self.ping(

            f"http://127.0.0.1:{self.port}/health"

        )

    # -----------------------------------------------------

    def snapshot(self):

        return {

            "internet":

                self.internet(),

            "camera":

                self.camera(),

            "brain":

                self.brain()

        }


network_service = NetworkService()


if __name__ == "__main__":

    logger.info(

        network_service.snapshot()

    )
