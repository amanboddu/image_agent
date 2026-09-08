"""Tests for the Replicate wrapper. Network calls are mocked."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from image_agent import replicate_client  # noqa: E402


class _FakeFileOutput:
    def __init__(self, data: bytes) -> None:
        self._data = data

    def read(self) -> bytes:
        return self._data


def test_generate_images_calls_model_per_image(monkeypatch):
    calls = []

    def fake_run(model_id, input):  # noqa: A002 - match replicate signature
        calls.append((model_id, input))
        return _FakeFileOutput(b"fake-image-bytes")

    monkeypatch.setattr(replicate_client.config, "REPLICATE_API_TOKEN", "test-token")
    monkeypatch.setattr(replicate_client.replicate, "run", fake_run)

    out = replicate_client.generate_images("a cat", num_images=3)

    assert out == [b"fake-image-bytes"] * 3
    assert len(calls) == 3
    assert calls[0][0] == replicate_client.config.MODEL_ID
    assert calls[0][1]["prompt"] == "a cat"


def test_generate_images_rejects_empty_prompt(monkeypatch):
    monkeypatch.setattr(replicate_client.config, "REPLICATE_API_TOKEN", "test-token")
    with pytest.raises(ValueError):
        replicate_client.generate_images("   ")


def test_generate_images_handles_list_output(monkeypatch):
    def fake_run(model_id, input):  # noqa: A002
        return [_FakeFileOutput(b"a"), _FakeFileOutput(b"b")]

    monkeypatch.setattr(replicate_client.config, "REPLICATE_API_TOKEN", "test-token")
    monkeypatch.setattr(replicate_client.replicate, "run", fake_run)

    out = replicate_client.generate_images("x", num_images=1)
    assert out == [b"a", b"b"]
