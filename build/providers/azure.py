from . import register

SEVERITY_MAP = {
    'Sev0': 'CRITICAL',
    'Sev1': 'CRITICAL',
    'Sev2': 'WARNING',
    'Sev3': 'WARNING',
    'Sev4': 'INFO',
    'Sev5': 'INFO',
}

STATUS_MAP = {
    'Fired': 'FIRING',
    'Resolved': 'RESOLVED',
}


@register('azure')
def normalize_azure(data):
    essentials = data.get('data', {}).get('essentials', {})
    context = data.get('data', {}).get('alertContext', {})

    alert_rule = essentials.get('alertRule', '')
    monitor_condition = essentials.get('monitorCondition', '')
    severity_raw = essentials.get('severity', '')
    description = essentials.get('description', '')
    signal_type = essentials.get('signalType', '')
    monitoring_service = essentials.get('monitoringService', '')
    target_ids = essentials.get('alertTargetIDs', [])

    status = STATUS_MAP.get(monitor_condition, monitor_condition)
    title = alert_rule

    if status == 'FIRING':
        title = f"\U0001f525 FIRING \U0001f525 \n\n*Alarm*: {title}"
    elif status == 'RESOLVED':
        title = f"\u2705 RESOLVED \u2705 \n\n*Alarm*: {title}"

    condition = context.get('condition') or {}
    metric_name = condition.get('metricName', '')
    metric_value = condition.get('metricValue', '')

    lines = [
        f"*Signal*: {signal_type}",
        f"*Service*: {monitoring_service}",
        f"*Condition*: {monitor_condition}",
    ]
    if description:
        lines.append(f"*Description*: {description}")
    if metric_name:
        lines.append(f"*Metric*: {metric_name}" + (f" = {metric_value}" if metric_value else ""))
    if target_ids:
        lines.append(f"*Resource*: {target_ids[0].split('/')[-1] if '/' in target_ids[0] else target_ids[0]}")

    details = {
        'namespace': monitoring_service,
        'query': metric_name,
        'summary': description,
        'metric_values': [metric_value] if metric_value else [],
    }

    return {
        'confirmation_url': None,
        'title': title,
        'body': '\n'.join(lines),
        'severity': SEVERITY_MAP.get(severity_raw, 'INFO'),
        'status': status,
        'details': details,
    }
