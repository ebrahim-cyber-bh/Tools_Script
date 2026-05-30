import time
import threading
from pynput import mouse, keyboard

# --- Config ---
DOUBLE_CLICK_INTERVAL = 0.4  # Max seconds between two clicks to count as double-click

last_click_time = 0
click_count = 0
lock = threading.Lock()

kb = keyboard.Controller()

def trigger_snip():
    """Press Win + Shift + S"""
    with kb.pressed(keyboard.Key.cmd):
        with kb.pressed(keyboard.Key.shift):
            kb.press('s')
            kb.release('s')
    print("📸 Snip & Sketch triggered!")

def on_click(x, y, button, pressed):
    global last_click_time, click_count

    # Button.x1 is the back side button on most mice
    if button == mouse.Button.x1 and pressed:
        with lock:
            now = time.time()
            if now - last_click_time <= DOUBLE_CLICK_INTERVAL:
                click_count += 1
            else:
                click_count = 1
            last_click_time = now

            if click_count >= 2:
                click_count = 0
                threading.Thread(target=trigger_snip, daemon=True).start()

print("✅ Running — double-click the mouse BACK button to take a screenshot (Win+Shift+S)")
print("   Press Ctrl+C to stop.\n")

with mouse.Listener(on_click=on_click) as listener:
    listener.join()
