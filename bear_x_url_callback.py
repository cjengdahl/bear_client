"""
bear_x_url_callback.py
A simple script to get the contents of a note from MacOS Bear App using the x-callback-url scheme.
This script sets up a local HTTP server to handle the callback from Bear after opening a note.
A custom callback handler can be provided to process the note content.
"""
import http.server
import threading
import time
import subprocess
import urllib

PORT = 8080

class BearCallbackHandler(http.server.BaseHTTPRequestHandler):

    # prevent ddos-ing the callback
    handled = False 

    def __init__(self, *args, callback_handler=None, **kwargs):
        self.callback_handler = callback_handler
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if BearCallbackHandler.handled:
            self.send_response(429)
            return
        BearCallbackHandler.handled = True
        parsed_path = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed_path.query)
        if parsed_path.path == "/success":
            try:    
                self.callback_handler(self)
            except Exception as e:
                self.send_response(500)
                self.wfile.write(str(e).encode())
            else:
                self.send_response(204)
        elif parsed_path.path == "/error":
            self.send_response(500)
            print("Bear x-error callback received.")
            print("Error Code:", query.get("errorCode", ["<none>"])[0])
            print("Error Message:", query.get("errorMessage", ["<none>"])[0])
        else:
            print("Unknown path:", parsed_path.path)
        # stop the server after handling the request
        threading.Thread(target=shutdown_server, daemon=True).start()


    def log_message(self, format, *args):
        pass  # override to suppress logging

def run_server(callback_handler):
    server = http.server.HTTPServer(
        ("localhost", PORT),
        lambda *args, **kwargs: BearCallbackHandler(*args, callback_handler=callback_handler, **kwargs)
    )
    # store the server instance so it can be shut down later
    global httpd
    httpd = server
    server.serve_forever()

def shutdown_server():
    time.sleep(1)  # give some time for the response to complete
    httpd.shutdown()

# Start a timer to shut down if no request is received within `timeout` seconds
def shutdown_if_idle(timeout=5):
    time.sleep(timeout)
    print(f"No callback received in {timeout} seconds. Shutting down.")
    httpd.shutdown()

def get_note(note_id=None, title=None):
    # annoyingly the Bear app will get launched to the target note
    subprocess.run(["open", generate_url(note_id=note_id, title=title)], timeout=5)

def generate_url(note_id=None, title=None):
    # annoyingly macOs will launch the browser to our success URL
    # this is only useful if our handler runs into an error
    callback_url = f"http://localhost:{PORT}/success"
    bear_url = f"bear://x-callback-url/open-note?new_window=no&show_window=no&open_note=no&x-success={callback_url}"
    if note_id is None and title is None:
        raise ValueError("either note_id or title must be provided")
    if note_id is not None and title is not None:
        raise ValueError("only one of note_id or title can be provided")
    if note_id is not None:
        bear_url += f"&id={note_id}"
    elif title is not None:
        bear_url += f"&title={title}"
    return bear_url

def run(callback_handler, note_id=None, title=None):
    server_thread = threading.Thread(target=run_server, args=[callback_handler], daemon=True)
    server_thread.start()
    shutdown_if_idle_thread = threading.Thread(target=shutdown_if_idle, kwargs={"timeout":4},daemon=True)
    shutdown_if_idle_thread.start()
    get_note(note_id=note_id, title=title)

    # wait for the server thread to finish (which will happen after shutdown)
    server_thread.join()


if __name__ == "__main__":

    def callback_handler(BearCallbackHandler):
        query = urllib.parse.urlparse(BearCallbackHandler.path).query
        content = urllib.parse.parse_qs(query)
        note = content.get("note")
        print(note)
    
    run(callback_handler, title="A Wonderful New Note")