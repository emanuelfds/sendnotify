# SPDX-License-Identifier: MIT
import json
from pathlib import Path

import pytest
from providers import detect, normalize

SAMPLES = Path(__file__).parent / "samples"


def load(name):
    with open(SAMPLES / name) as f:
        return json.load(f)


# --- detect ---

DETECT_CASES = [
    ("oci-confirmation.json", "oci"),
    ("oci-firing.json", "oci"),
    ("oci-resolved.json", "oci"),
    ("aws-confirmation.json", "aws"),
    ("aws-firing.json", "aws"),
    ("aws-resolved.json", "aws"),
    ("azure-firing.json", "azure"),
    ("azure-resolved.json", "azure"),
]


@pytest.mark.parametrize("filename,expected", DETECT_CASES, ids=[c[0] for c in DETECT_CASES])
def test_detect(filename, expected):
    assert detect(load(filename)) == expected


# --- normalize ---

NORMALIZE_CASES = [
    ("oci-confirmation.json", "confirmation_url", True),
    ("oci-firing.json", "status", "FIRING"),
    ("oci-resolved.json", "status", "RESOLVED"),
    ("aws-confirmation.json", "confirmation_url", True),
    ("aws-firing.json", "status", "FIRING"),
    ("aws-resolved.json", "status", "RESOLVED"),
    ("azure-firing.json", "status", "FIRING"),
    ("azure-resolved.json", "status", "RESOLVED"),
]


@pytest.mark.parametrize("filename,field,expected", NORMALIZE_CASES, ids=[c[0] for c in NORMALIZE_CASES])
def test_normalize(filename, field, expected):
    result = normalize(load(filename))
    assert result is not None, f"normalize returned None for {filename}"
    got = result.get(field)
    if expected is True:
        assert bool(got), f"{filename}: {field} is falsy"
    else:
        assert got == expected, f"{filename}: {field}={got}, expected {expected}"


# --- unknown payload ---


def test_unknown_payload():
    assert normalize({"foo": "bar"}) is None
