"""Thin wrapper around the Replicate client for image generation."""

from __future__ import annotations

import os

import replicate

from . import config


def _to_bytes(item: object) -> bytes:
    """Normalize one Replicate output item into raw image bytes.

    Replicate may return a FileOutput object, a URL string, or bytes
    depending on the model / client version.
    """
    if isinstance(item, bytes):
        return item
    read = getattr(item, "read", None)
    if callable(read):
        return read()
    if isinstance(item, str):
        import urllib.request

        with urllib.request.urlopen(item) as resp:  # noqa: S310 - trusted Replicate URL
            return resp.read()
    raise TypeError(f"Unexpected Replicate output type: {type(item)!r}")


def generate_images(
    prompt: str,
    num_images: int = 1,
    output_format: str = config.OUTPUT_FORMAT,
) -> list[bytes]:
    """Generate `num_images` images for `prompt`. Returns a list of image bytes.

    nano-banana-2 returns a single image per run, so we call it once per
    requested image.
    """
    if not prompt.strip():
        raise ValueError("Prompt is empty.")

    os.environ["REPLICATE_API_TOKEN"] = config.require_token()

    images: list[bytes] = []
    for _ in range(num_images):
        output = replicate.run(
            config.MODEL_ID,
            input={"prompt": prompt, "output_format": output_format},
        )
        if isinstance(output, list):
            images.extend(_to_bytes(o) for o in output)
        else:
            images.append(_to_bytes(output))

    return images
