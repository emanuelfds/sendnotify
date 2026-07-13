import json
import logging

from . import register

log = logging.getLogger(__name__)

SEVERITY_MAP = {
    "ALARM": "CRITICAL",
    "OK": "INFO",
    "INSUFFICIENT_DATA": "WARNING",
}

STATUS_MAP = {
    "ALARM": "FIRING",
    "OK": "RESOLVED",
    "INSUFFICIENT_DATA": "INFO",
}


@register("aws")
def normalize_aws(data):
    if data.get("Type") == "SubscriptionConfirmation":
        return {
            "confirmation_url": data.get("SubscribeURL"),
            "title": None,
            "body": None,
            "severity": None,
            "status": None,
            "details": {},
        }

    message_str = data.get("Message", "{}")
    if isinstance(message_str, str):
        try:
            alarm = json.loads(message_str)
        except json.JSONDecodeError:
            log.error(f"Failed to parse AWS Message JSON: {message_str[:200]}")
            alarm = {}
    else:
        alarm = message_str

    title = alarm.get("AlarmName", "")
    old_state = alarm.get("OldStateValue", "")
    new_state = alarm.get("NewStateValue", "")
    reason = alarm.get("NewStateReason", "")
    region = alarm.get("Region", "")
    account = alarm.get("AWSAccountId", "")
    trigger = alarm.get("Trigger", {})

    status = STATUS_MAP.get(new_state, new_state)
    if status == "FIRING":
        title = f"\U0001f525 FIRING \U0001f525 \n\n*Alarm*: {title}"
    elif status == "RESOLVED":
        title = f"\u2705 RESOLVED \u2705 \n\n*Alarm*: {title}"

    lines = [
        f"*Account*: {account}",
        f"*Region*: {region}",
        f"*State*: {old_state} \u2192 {new_state}",
        f"*Reason*: {reason}",
    ]
    if trigger:
        lines.append(f"*Metric*: {trigger.get('MetricName', '')}")
        lines.append(f"*Threshold*: {trigger.get('Threshold', '')}")

    details = {
        "namespace": trigger.get("Namespace", ""),
        "query": trigger.get("MetricName", ""),
        "summary": reason,
        "metric_values": [trigger.get("Threshold", "")],
    }

    return {
        "confirmation_url": None,
        "title": title,
        "body": "\n".join(lines),
        "severity": SEVERITY_MAP.get(new_state, "INFO"),
        "status": status,
        "details": details,
    }
