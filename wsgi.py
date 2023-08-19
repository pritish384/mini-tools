from waitress import serve
from app import app  # Import your Flask app instance
import time
import threading

def alive():
    while True:
        print("Heartbeat 💖")
        time.sleep(5)


threading.Thread(target=alive).start()

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=80)