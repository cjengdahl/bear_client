# Bear x-callback-url Fetcher

`bear_x_url_callback.py` is a simple Python script to **fetch the contents of a note** from the Bear app on macOS using the [x-callback-url scheme](https://bear.app/faq/X-callback-url%20scheme%20documentation/).
It sets up a lightweight local HTTP server to handle Bear's callback after opening a note, and allows you to define a **custom handler** for processing the returned note content.

---

## Features

- Fetch a note by **ID** or **title** from Bear.
- Set up a **temporary HTTP server** to listen for Bear's `x-success` callback.
- Handle success and error callbacks cleanly.
- Provide a **custom callback function** to process note content however you want.
- **Automatic timeout** and shutdown if Bear does not respond within a few seconds.
- **Lightweight** — uses only standard Python libraries.

---

## Requirements

- **macOS** with the Bear app installed.
- **Python 3.7+**.

---

## Installation

Clone this repository (or just copy `bear_x_url_callback.py`):

```bash
git clone https://github.com/yourusername/bear-x-callback-fetcher
