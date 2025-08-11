import redis
import json
import time
import asyncio
import os
import sys
import webbrowser
import subprocess
import pyautogui
import pytesseract
from PIL import Image
from bs4 import BeautifulSoup
from requests_html import AsyncHTMLSession
import nest_asyncio

# Asyncio fix for Jupyter
nest_asyncio.apply()

# ===== CONFIG =====
URL = "https://portfolio-praveen-gupta.vercel.app/"
SCROLL_AMOUNT = -50
SCROLL_DELAY = 0.2
SCROLL_LIMIT = 200
REDIS_TTL = 60 * 60 * 4  # 4 hours

# Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Screenshot helper
def take_screenshot():
    screenshot_path = "/home/praveen/Desktop/My-Projects/interview_p/imgs/outputs/screen.png"
    time.sleep(0.5)
    subprocess.run(["gnome-screenshot", "-f", screenshot_path])
    return screenshot_path

# OCR helper
def find_text_coordinate_in_image(image_path, search_text):
    img = Image.open(image_path).convert("L")
    img = img.point(lambda x: 0 if x < 130 else 255)
    boxes = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    for i in range(len(boxes['text'])):
        if search_text.lower() in boxes['text'][i].lower():
            x, y, w, h = boxes['left'][i], boxes['top'][i] + 25, boxes['width'][i], boxes['height'][i] + 25
            center_x = x + w // 2
            center_y = y + h // 2
            return (center_x, center_y)
    return None

# Type and tab
def fill_field(value):
    pyautogui.typewrite(value)
    pyautogui.press("tab")
    time.sleep(0.5)

# Fetch form fields
async def fetch_form():
    session = AsyncHTMLSession()
    webbrowser.open(URL)
    r = await session.get(URL)
    await r.html.arender(timeout=20, sleep=2)
    soup = BeautifulSoup(r.html.html, "html.parser")
    form = soup.find("form")
    if not form:
        print("[ERROR] No form found.")
        return []
    fields = []
    for tag in form.find_all(["input", "textarea"]):
        if tag.get("type") in ["submit", "hidden", "checkbox", "radio"]:
            continue
        name = tag.get("name") or tag.get("id") or tag.get("placeholder") or tag.text
        if name:
            fields.append(name.strip())
    print("[INFO] Required fields:", fields)
    return fields

# Main logic
async def main():
    field_names = await fetch_form()
    if not field_names:
        return

    # Try Redis first
    cached_data = redis_client.get("form_data")
    if cached_data:
        cached_data = json.loads(cached_data)
        # use_cache = input("[?] Use saved data? (y/n): ").strip().lower()
        # if use_cache == 'y':
        if True:
            input_data = cached_data
            print('please go to browser!!!')
            time.sleep(3)
        else:
            input_data = {}
            for name in field_names:
                input_data[name] = input(f"Enter value for {name}: ")
            redis_client.setex("form_data", REDIS_TTL, json.dumps(input_data))
            time.sleep(3)
    else:
        input_data = {}
        for name in field_names:
            input_data[name] = input(f"Enter value for {name}: ")
        redis_client.setex("form_data", REDIS_TTL, json.dumps(input_data))

    # Locate first field and fill
    first_field = field_names[0]
    for attempt in range(SCROLL_LIMIT):
        shot = take_screenshot()
        coord = find_text_coordinate_in_image(shot, first_field)
        if coord:
            print(f"[FOUND] '{first_field}' at {coord}")
            pyautogui.click(coord[0], coord[1])
            fill_field(input_data[first_field])
            break
        pyautogui.scroll(SCROLL_AMOUNT)
        time.sleep(SCROLL_DELAY)

    # Fill remaining fields
    for name in field_names[1:]:
        fill_field(input_data[name])

    pyautogui.press('enter')

if __name__ == "__main__":
    asyncio.run(main())
