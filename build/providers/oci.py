from . import register


@register('oci')
def normalize_oci(data):
    if 'ConfirmationURL' in data:
        return {
            'confirmation_url': data['ConfirmationURL'],
            'title': None,
            'body': None,
            'severity': None,
            'status': None,
            'details': {},
        }

    alarm = data.get('alarmMetaData', [{}])[0]

    title = data.get('title', '')
    severity = data.get('severity', '')
    raw_status = alarm.get('status', '')
    status_map = {'FIRING': 'FIRING', 'OK': 'RESOLVED'}
    status = status_map.get(raw_status, raw_status)

    if status == 'FIRING':
        title = f"\U0001f525 FIRING \U0001f525 \n\n*Alarm*: {title}"
    elif status == 'RESOLVED':
        title = f"\u2705 RESOLVED \u2705 \n\n*Alarm*: {title}"

    details = {
        'namespace': alarm.get('namespace', ''),
        'query': alarm.get('query', ''),
        'summary': alarm.get('alarmSummary', ''),
        'metric_values': alarm.get('metricValues', []),
    }

    return {
        'confirmation_url': None,
        'title': title,
        'body': data.get('body', ''),
        'severity': severity,
        'status': status,
        'details': details,
    }
