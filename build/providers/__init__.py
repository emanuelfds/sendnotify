import logging
from collections.abc import Callable

log = logging.getLogger(__name__)

PROVIDERS: dict[str, Callable] = {}


def register(name):
    def decorator(fn):
        PROVIDERS[name] = fn
        return fn

    return decorator


# Import provider modules to trigger @register decorators
from . import aws, azure, oci  # noqa: F401, E402


def detect(data):
    if "alarmMetaData" in data or "ConfirmationURL" in data:
        return "oci"
    if "Type" in data and data.get("Type") in ("Notification", "SubscriptionConfirmation"):
        return "aws"
    if "data" in data and "essentials" in data.get("data", {}):
        return "azure"
    return None


def normalize(data):
    provider = detect(data)
    if not provider:
        log.error(f"Unknown payload format: {list(data.keys())}")
        return None
    fn = PROVIDERS.get(provider)
    if not fn:
        log.error(f"No normalizer registered for provider: {provider}")
        return None
    result = fn(data)
    result["provider"] = provider
    return result
