"""Streamlit image generator agent.

Run: streamlit run app.py
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import streamlit as st

# Make `src/` importable without installing the package.
sys.path.insert(0, str(Path(__file__).parent / "src"))

from image_agent import config  # noqa: E402
from image_agent.replicate_client import generate_images  # noqa: E402

st.set_page_config(page_title="Image Generator Agent", page_icon="🎨")

st.title("🎨 Image Generator Agent")
st.caption(f"Model: `{config.MODEL_ID}` via Replicate")

if not config.REPLICATE_API_TOKEN:
    st.error("REPLICATE_API_TOKEN not set. Copy `.env.example` to `.env` and add your token.")
    st.stop()

with st.form("gen"):
    prompt = st.text_area(
        "Describe the image you want",
        placeholder="A cozy café interior at golden hour, warm light, film grain",
        height=120,
    )
    num_images = st.slider(
        "Number of images",
        min_value=config.MIN_IMAGES,
        max_value=config.MAX_IMAGES,
        value=1,
    )
    submitted = st.form_submit_button("Generate")

if submitted:
    if not prompt.strip():
        st.warning("Enter a prompt first.")
        st.stop()

    with st.spinner(f"Generating {num_images} image(s)…"):
        try:
            images = generate_images(prompt, num_images=num_images)
        except Exception as exc:  # noqa: BLE001 - surface any error to the user
            st.error(f"Generation failed: {exc}")
            st.stop()

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    for i, data in enumerate(images, start=1):
        st.image(data, caption=f"{prompt[:80]} ({i}/{len(images)})")
        st.download_button(
            "Download",
            data=data,
            file_name=f"image-{stamp}-{i}.{config.OUTPUT_FORMAT}",
            mime=f"image/{config.OUTPUT_FORMAT}",
            key=f"dl-{i}",
        )
