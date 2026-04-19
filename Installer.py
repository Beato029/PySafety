import requests
import time
import sys

url = "https://raw.githubusercontent.com/Beato029/PySafezty/main/main.py"
output_file = "main.py"

response = requests.get(url, stream=True)

if response.status_code != 200:
    print("Errore:", response.status_code)
    exit()

total_size = int(response.headers.get("content-length", 0))
downloaded = 0
chunk_size = 1024

start_time = time.time()

with open(output_file, "wb") as f:
    for chunk in response.iter_content(chunk_size=chunk_size):
        if chunk:
            f.write(chunk)
            downloaded += len(chunk)

            elapsed = time.time() - start_time
            speed = downloaded / elapsed if elapsed > 0 else 0

            eta = (total_size - downloaded) / speed if speed > 0 else 0
            percent = (downloaded / total_size) * 100 if total_size else 0

            sys.stdout.write(
                f"\r[{percent:.2f}%] "
                f"{downloaded/1024:.1f}KB / {total_size/1024:.1f}KB | "
                f"{speed/1024:.1f} KB/s | "
                f"ETA: {eta:.1f}s"
            )
            sys.stdout.flush()

print("\nDownload completato!")