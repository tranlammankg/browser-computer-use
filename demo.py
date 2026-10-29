#!/usr/bin/env python3
"""
Demo nhanh Computer Use: Mở Chrome, mở tab mới, và gõ thử tìm kiếm
"""

import sys
import os
import time

# Đường dẫn script
SKILL_DIR = os.path.expanduser("~/.gemini/config/skills/browser-computer-use/scripts")
sys.path.append(SKILL_DIR)

from computer_use import focus_app, human_type, human_click, get_screen_info, take_screenshot
import pyautogui

def main():
    print("1. Kiểm tra màn hình...")
    info = get_screen_info()
    print("   Độ phân giải màn hình:", info)

    print("\n2. Chuyển sang Google Chrome...")
    ok, msg = focus_app("Google Chrome")
    print(f"   {msg}")

    print("\n3. Mở thanh địa chỉ bằng phím tắt (Command + L)...")
    pyautogui.hotkey("command", "l")
    time.sleep(0.5)

    print("\n4. Gõ thử tìm kiếm với tốc độ người thật...")
    human_type("https://www.google.com")
    time.sleep(0.3)
    pyautogui.press("enter")

    print("\n🎉 Hoàn thành demo cơ bản!")

if __name__ == "__main__":
    main()
