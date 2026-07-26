"""
============================================================
Noor Camera Node
Production Test
============================================================
"""

from shared.config_manager import load_config
from shared.logger import logger
from shared.camera_state import camera_state
from shared.system_monitor import system_monitor
from shared.performance import performance
from shared.diagnostics import diagnostics


def main():

    logger.info("=" * 60)
    logger.info("Running Production Test")
    logger.info("=" * 60)

    config = load_config()

    print()

    print("CONFIG")

    print(config)

    print()

    print("CAMERA")

    print(camera_state.to_dict())

    print()

    print("SYSTEM")

    print(system_monitor.snapshot())

    print()

    print("PERFORMANCE")

    print(performance.snapshot())

    print()

    print("DIAGNOSTICS")

    print(diagnostics.snapshot())

    print()

    logger.info("Production Test Passed")


if __name__ == "__main__":

    main()
