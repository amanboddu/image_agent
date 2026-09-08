# Image Generator Agent

Simple Streamlit app. User types image description → Replicate model
(`google/nano-banana-2`) generates image → user downloads it.

## Layout

```
image_agent/
├── app.py                        # Streamlit UI (entry point)
├── requirements.txt              # pip deps
├── pytest.ini                    # test config
├── .env.example                  # copy to .env, add Replicate token
├── scripts/
│   └── run.sh                    # launch helper
├── src/
│   └── image_agent/
│       ├── __init__.py
│       ├── config.py             # env vars + constants
│       └── replicate_client.py   # generate_images()
├── tests/
│   └── test_replicate_client.py  # mocked, no network
└── outputs/                      # (gitignored) local saves if you add them
```

## Setup

**Requires Python 3.12** (3.10–3.13 also work). Python 3.14+ does **not**
work: `replicate` 1.x uses the pydantic v1 compat shim, which is
incompatible with 3.14 (`pydantic.v1.errors.ConfigError: unable to infer
type for attribute "previous"` on import).

```bash
# 1. create a 3.12 virtualenv (use an explicit interpreter path if
#    `python3.12` is not on PATH, e.g. /opt/homebrew/bin/python3.12)
python3.12 -m venv .venv
source .venv/bin/activate

# 2. confirm the venv is 3.12, not 3.14
python --version        # -> Python 3.12.x

# 3. install deps
pip install -r requirements.txt

# 4. add your Replicate token
cp .env.example .env
# edit .env, set REPLICATE_API_TOKEN (get one at
# https://replicate.com/account/api-tokens)
```

## Run

```bash
streamlit run app.py
# or
./scripts/run.sh
```

## Test

```bash
pip install pytest
pytest
```

## Config

Env vars (see `.env.example`):

| Var                   | Required | Default                | Purpose               |
|-----------------------|----------|------------------------|-----------------------|
| `REPLICATE_API_TOKEN` | yes      | –                      | Replicate auth        |
| `MODEL_ID`            | no       | `google/nano-banana-2` | model to run          |

UI controls: prompt text + number of images (1–4). nano-banana-2 makes
one image per call, so N images = N calls.
