"""
============================================================
Project : Noor AI Home Platform
Module  : Main Entry Point
Version : 1.0.0
============================================================
"""

import uvicorn

from shared.logger import logger
from shared.config_manager import load_config

config = load_config()


def main():
    logger.info("=" * 60)
    logger.info("Noor Camera Node Starting")
    logger.info("=" * 60)

    host = config.get("server", {}).get("host", "0.0.0.0")
    port = config.get("server", {}).get("port", 8000)

    logger.info(f"Host : {host}")
    logger.info(f"Port : {port}")

    uvicorn.run(
        "services.stream_service.stream:app",
        host=host,
        port=port,
        reload=False,
        access_log=False
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Shutdown Requested")
    except Exception as ex:
        logger.exception(ex)
    finally:
        logger.info("Noor Camera Node Stopped")
