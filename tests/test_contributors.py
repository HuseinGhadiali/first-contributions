"""Simple checks for Contributors.md.

Run with:  python -m pytest tests
"""

import re
from pathlib import Path

import pytest

CONTRIBUTORS_FILE = Path(__file__).resolve().parent.parent / "Contributors.md"

# A well-formed entry looks like:
#   - [Your Name](https://github.com/your-username)
# optionally followed by a short message.
ENTRY_PATTERN = re.compile(
    r"^- \[(?P<name>[^\]]+)\]\(https://github\.com/(?P<username>[A-Za-z0-9-]+)/?\)"
)


def parse_entry(line):
    """Return (name, username) for a well-formed entry, or None otherwise."""
    match = ENTRY_PATTERN.match(line)
    if match is None:
        return None
    return match.group("name"), match.group("username")


@pytest.mark.parametrize(
    "line, expected",
    [
        ("- [Jane Doe](https://github.com/janedoe)", ("Jane Doe", "janedoe")),
        ("- [Jane Doe](https://github.com/jane-doe/)", ("Jane Doe", "jane-doe")),
        ("- [Jane](https://github.com/jane) - Hello!", ("Jane", "jane")),
    ],
)
def test_parse_entry_accepts_well_formed_lines(line, expected):
    assert parse_entry(line) == expected


@pytest.mark.parametrize(
    "line",
    [
        "",
        "# Contributors",
        "Jane Doe",
        "-[Jane Doe](https://github.com/janedoe)",  # missing space after dash
        "- [Jane Doe]()",  # empty link
        "- [Jane Doe](https://example.com/janedoe)",  # not a GitHub profile
    ],
)
def test_parse_entry_rejects_malformed_lines(line):
    assert parse_entry(line) is None


def test_contributors_file_exists():
    assert CONTRIBUTORS_FILE.is_file()


def test_contributors_file_has_well_formed_entries():
    lines = CONTRIBUTORS_FILE.read_text(encoding="utf-8").splitlines()
    entries = [entry for entry in map(parse_entry, lines) if entry is not None]
    assert len(entries) > 0
