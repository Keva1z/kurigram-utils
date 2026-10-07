import logging
import sys

log = logging.getLogger(__name__)


def install_event_loop() -> None:
    if sys.platform in ("win32", "cygwin", "cli"):
        import winloop

        winloop.install()

        log.info("Using winloop for Windows event loop.")
    else:
        import uvloop

        uvloop.install()

        log.info("Using uvloop for non-Windows event loop.")
