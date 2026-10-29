#!/usr/bin/env python3
"""
Checks macOS Accessibility & Screen Recording permissions required for Computer Use.
"""

import sys
import subprocess
import os

def check_screen_recording():
    test_path = "/tmp/test_screen_perm.png"
    if os.path.exists(test_path):
        os.remove(test_path)
    res = subprocess.run(["screencapture", "-x", test_path], capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(test_path):
        os.remove(test_path)
        return True
    return False

def check_accessibility():
    # Test if mouse position / event post works
    try:
        import pyautogui
        pos = pyautogui.position()
        return True if pos else False
    except Exception:
        return False

def open_settings_panel(panel_type):
    if panel_type == "screen":
        subprocess.run(["open", "x-apple.systempreferences:com.apple.preference.security?Privacy_ScreenCapture"])
    elif panel_type == "accessibility":
        subprocess.run(["open", "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"])

def main():
    print("=== KIỂM TRA QUYỀN TRÊN MACOS (COMPUTER USE) ===")
    
    screen_ok = check_screen_recording()
    print(f"1. Quyền Ghi màn hình (Screen Recording): {'✅ ĐÃ CẤP' if screen_ok else '❌ CHƯA CẤP'}")
    
    acc_ok = check_accessibility()
    print(f"2. Quyền Trợ năng (Accessibility / Chuột & Phím): {'✅ ĐÃ CẤP' if acc_ok else '❌ CẦN KIỂM TRA'}")

    if not screen_ok:
        print("\n👉 CÁCH BẬT QUYỀN GHI MÀN HÌNH:")
        print("  1. Mở Cài đặt hệ thống (System Settings) -> Quyền riêng tư & Bảo mật (Privacy & Security).")
        print("  2. Chọn 'Ghi màn hình & Âm thanh hệ thống' (Screen & System Audio Recording).")
        print("  3. Bật công tắc cho ứng dụng 'Antigravity' (hoặc Terminal/IDE của bạn).")
        print("\nĐang mở bảng Cài đặt...")
        open_settings_panel("screen")

    if not acc_ok:
        print("\n👉 CÁCH BẬT QUYỀN TRỢ NĂNG (Accessibility):")
        print("  1. Mở Cài đặt hệ thống -> Quyền riêng tư & Bảo mật -> Trợ năng (Accessibility).")
        print("  2. Bật công tắc cho ứng dụng 'Antigravity' (hoặc Terminal).")

    if screen_ok and acc_ok:
        print("\n🎉 Tất cả quyền đã sẵn sàng! Bạn có thể sử dụng Computer Use ngay bây giờ.")

if __name__ == "__main__":
    main()
