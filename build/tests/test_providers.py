#!/usr/bin/env python3
import json
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import providers


def load(name):
    path = Path(__file__).parent / 'samples' / name
    with open(path) as f:
        return json.load(f)


def test_detect():
    cases = [
        ('oci-confirmation.json', 'oci'),
        ('oci-firing.json', 'oci'),
        ('oci-resolved.json', 'oci'),
        ('aws-confirmation.json', 'aws'),
        ('aws-firing.json', 'aws'),
        ('aws-resolved.json', 'aws'),
        ('azure-firing.json', 'azure'),
        ('azure-resolved.json', 'azure'),
    ]
    for file, expected in cases:
        data = load(file)
        result = providers.detect(data)
        status = '✓' if result == expected else '✗'
        print(f"  {status} {file:30s} → {result or 'None':10s} (expected {expected})")


def test_normalize():
    cases = [
        ('oci-confirmation.json', 'confirmation_url', True),
        ('oci-firing.json', 'status', 'FIRING'),
        ('oci-resolved.json', 'status', 'RESOLVED'),
        ('aws-confirmation.json', 'confirmation_url', True),
        ('aws-firing.json', 'status', 'FIRING'),
        ('aws-resolved.json', 'status', 'RESOLVED'),
        ('azure-firing.json', 'status', 'FIRING'),
        ('azure-resolved.json', 'status', 'RESOLVED'),
    ]
    all_ok = True
    for file, field, expected in cases:
        data = load(file)
        result = providers.normalize(data)
        if result is None:
            print(f"  ✗ {file:30s} → normalize returned None")
            all_ok = False
            continue
        got = result.get(field)
        if expected is True:
            ok = bool(got)
        else:
            ok = got == expected
        if not ok:
            all_ok = False
        status = '✓' if ok else '✗'
        extra = f" ({got})" if not ok else ''
        print(f"  {status} {file:30s} → {field}={got}{extra}")
    return all_ok


def test_unknown():
    result = providers.normalize({"foo": "bar"})
    ok = result is None
    print(f"  {'✓' if ok else '✗'} unknown payload        → {'None (correct)' if ok else result}")
    return ok


def main():
    print("\n=== Detect ===")
    test_detect()

    print("\n=== Normalize ===")
    ok = test_normalize()

    print("\n=== Unknown ===")
    ok = test_unknown() and ok

    print(f"\n{'→ Todos os testes passaram!' if ok else '→ Alguns testes falharam!'}")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
