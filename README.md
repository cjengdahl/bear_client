# Bear x-callback-url Client

`bear_x_url_callback.py` is a simple Python script to **fetch the contents of a note** from the Bear app on macOS using the [x-callback-url scheme](https://bear.app/faq/X-callback-url%20scheme%20documentation/).
It sets up a lightweight local HTTP server to handle Bear's callback after opening a note, and allows you to define a **custom handler** for processing the returned note content.

---

## Requirements

- **macOS** with the Bear app installed.
- **Python 3.7+**.

---

## Installation

Clone this repository (or just copy `bear_x_url_callback.py`):
- `git clone https://github.com/cjengdahl/bear_client.git` and reference directly
- or `pip install git+https://github.com/cjengdahl/bear_client.git@v0.1.0`
