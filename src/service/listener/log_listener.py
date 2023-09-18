import logging

from src.service.event import subscribe

logger = logging.getLogger(__name__)


def handle_request(data: dict):
    logging.info("Handling %(method)s request for %(data)s", extra=data)
    _ = data.pop("method")


def setup_log_event_handlers():
    subscribe("list", handle_request)
