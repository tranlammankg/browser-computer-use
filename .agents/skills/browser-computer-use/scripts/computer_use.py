#!/usr/bin/env python3
"""
Computer Use Engine for macOS (Human-like GUI Automation)
Emulates Claude Computer Use:
- Retina display coordinate scaling
- Cubic Bezier curve mouse movements with human acceleration & micro-jitters
- Natural typing cadence with organic pauses
- Window focus & state management
"""

import sys
import os
import time
import math
import random
import argparse
import subprocess
import json

try:
    import pyautogui
    # Configure pyautogui defaults
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.05
except ImportError:
    pyautogui = None


def get_screen_info():
    """Returns display dimensions and retina scaling factor."""
    if not pyautogui:
        return {"error": "pyautogui not installed"}
    
    logical_w, logical_h = pyautogui.size()
    return {
        "width": logical_w,
        "height": logical_h,
        "mouse_x": pyautogui.position().x,
        "mouse_y": pyautogui.position().y,
    }


def focus_app(app_name="Google Chrome"):
    """Brings the targeted application to the foreground using AppleScript."""
    script = f'''
    tell application "{app_name}"
        activate
    end tell
    '''
    res = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if res.returncode == 0:
        time.sleep(0.3)
        return True, f"Focused {app_name}"
    return False, res.stderr.strip()


def take_screenshot(output_path="/tmp/screen.png", crop_active_window=False):
    """
    Captures the screen using macOS screencapture tool.
    Output image can be inspected by Vision models.
    """
    cmd = ["screencapture", "-x"]
    if crop_active_window:
        # Capture the active window only
        cmd.append("-w")
    cmd.append(output_path)
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(output_path):
        size_bytes = os.path.getsize(output_path)
        return True, {
            "path": output_path,
            "bytes": size_bytes
        }
    return False, {
        "error": res.stderr.strip() or "Screen recording permission missing in macOS Settings."
    }


def _bezier_point(p0, p1, p2, p3, t):
    """Calculate point along cubic Bezier curve."""
    return (
        (1 - t) ** 3 * p0 +
        3 * (1 - t) ** 2 * t * p1 +
        3 * (1 - t) * t ** 2 * p2 +
        t ** 3 * p3
    )


def human_move(target_x, target_y, duration=None):
    """
    Moves mouse from current position to (target_x, target_y)
    using a natural cubic Bezier curve with easing and organic micro-variations.
    """
    if not pyautogui:
        raise RuntimeError("pyautogui is required for mouse operations")
    
    start_x, start_y = pyautogui.position()
    distance = math.hypot(target_x - start_x, target_y - start_y)
    
    if distance < 3:
        pyautogui.moveTo(target_x, target_y)
        return
    
    if duration is None:
        # Base duration proportional to distance + human variability
        base_dur = 0.2 + (distance / 1800.0) * 0.4
        duration = random.uniform(base_dur * 0.85, base_dur * 1.15)
        duration = max(0.15, min(duration, 0.9))
    
    # Calculate control points with human curve deviation
    deviation = min(distance * 0.25, 120)
    angle = math.atan2(target_y - start_y, target_x - start_x)
    normal_angle = angle + (math.pi / 2 if random.random() > 0.5 else -math.pi / 2)
    
    dev_dist1 = random.uniform(0.1, 1.0) * deviation
    dev_dist2 = random.uniform(0.1, 1.0) * deviation
    
    ctrl1_x = start_x + (target_x - start_x) * 0.33 + math.cos(normal_angle) * dev_dist1
    ctrl1_y = start_y + (target_y - start_y) * 0.33 + math.sin(normal_angle) * dev_dist1
    ctrl2_x = start_x + (target_x - start_x) * 0.66 + math.cos(normal_angle) * dev_dist2
    ctrl2_y = start_y + (target_y - start_y) * 0.66 + math.sin(normal_angle) * dev_dist2
    
    steps = max(int(distance / 15), 18)
    start_time = time.time()
    
    for i in range(1, steps + 1):
        # S-curve easing (ease-in-out-quad)
        t = i / steps
        if t < 0.5:
            eased_t = 2 * t * t
        else:
            eased_t = -1 + (4 - 2 * t) * t
        
        cur_x = _bezier_point(start_x, ctrl1_x, ctrl2_x, target_x, eased_t)
        cur_y = _bezier_point(start_y, ctrl1_y, ctrl2_y, target_y, eased_t)
        
        # Add micro tremor (jitter)
        if 0.1 < t < 0.9:
            cur_x += random.uniform(-0.8, 0.8)
            cur_y += random.uniform(-0.8, 0.8)
            
        pyautogui.moveTo(round(cur_x), round(cur_y))
        
        elapsed = time.time() - start_time
        target_elapsed = (i / steps) * duration
        if target_elapsed > elapsed:
            time.sleep(target_elapsed - elapsed)
            
    pyautogui.moveTo(target_x, target_y)
    # Brief pause after arriving at target
    time.sleep(random.uniform(0.04, 0.12))


def human_click(x=None, y=None, button="left", clicks=1):
    """
    Clicks at (x, y) with human movement and realistic mouse press duration.
    """
    if x is not None and y is not None:
        human_move(x, y)
        
    for i in range(clicks):
        pyautogui.mouseDown(button=button)
        # Mouse click hold time (typical human click duration 60-140ms)
        time.sleep(random.uniform(0.06, 0.14))
        pyautogui.mouseUp(button=button)
        if i < clicks - 1:
            time.sleep(random.uniform(0.08, 0.18))
            
    time.sleep(random.uniform(0.05, 0.15))


def human_type(text, use_clipboard=False):
    """
    Types text with human cadence, random keystroke delays, and occasional short pauses.
    If use_clipboard is True or text has non-ASCII characters, uses clipboard paste (Command+V).
    """
    # Check if text contains complex non-ASCII or is very long
    has_non_ascii = any(ord(c) > 127 for c in text)
    if use_clipboard or has_non_ascii or len(text) > 80:
        # Use pbcopy on macOS
        proc = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
        proc.communicate(text.encode("utf-8"))
        time.sleep(random.uniform(0.05, 0.1))
        # Command + V
        pyautogui.hotkey("command", "v")
        time.sleep(random.uniform(0.08, 0.18))
        return

    for char in text:
        pyautogui.write(char)
        # Jitter delay per keystroke
        delay = random.uniform(0.035, 0.095)
        # Punctuation pauses
        if char in ".,!?;\n":
            delay += random.uniform(0.12, 0.28)
        elif char == " ":
            delay += random.uniform(0.04, 0.09)
        time.sleep(delay)


def human_scroll(clicks_vertical):
    """
    Scrolls with smooth incremental steps instead of single abrupt jump.
    Negative = down, Positive = up.
    """
    sign = 1 if clicks_vertical > 0 else -1
    total = abs(clicks_vertical)
    remaining = total
    
    while remaining > 0:
        step = min(remaining, random.randint(1, 3))
        pyautogui.scroll(sign * step)
        remaining -= step
        time.sleep(random.uniform(0.03, 0.07))


def main():
    parser = argparse.ArgumentParser(description="Claude-Style Computer Use for macOS")
    subparsers = parser.add_subparsers(dest="command")

    # Status
    subparsers.add_parser("status", help="Get display dimensions and status")

    # Screenshot
    shot_parser = subparsers.add_parser("screenshot", help="Capture screen")
    shot_parser.add_argument("--out", default="/tmp/screen.png", help="Output file path")
    shot_parser.add_argument("--window", action="store_true", help="Capture active window only")

    # Focus
    focus_parser = subparsers.add_parser("focus", help="Focus an application")
    focus_parser.add_argument("app", default="Google Chrome", nargs="?", help="Application name")

    # Click
    click_parser = subparsers.add_parser("click", help="Human-like click at (x, y)")
    click_parser.add_argument("x", type=int, help="X coordinate")
    click_parser.add_argument("y", type=int, help="Y coordinate")
    click_parser.add_argument("--button", default="left", choices=["left", "right", "middle"])
    click_parser.add_argument("--double", action="store_true", help="Double click")

    # Move
    move_parser = subparsers.add_parser("move", help="Human-like mouse movement")
    move_parser.add_argument("x", type=int, help="Target X coordinate")
    move_parser.add_argument("y", type=int, help="Target Y coordinate")

    # Drag
    drag_parser = subparsers.add_parser("drag", help="Drag mouse from (x1, y1) to (x2, y2)")
    drag_parser.add_argument("x1", type=int)
    drag_parser.add_argument("y1", type=int)
    drag_parser.add_argument("x2", type=int)
    drag_parser.add_argument("y2", type=int)

    # Type
    type_parser = subparsers.add_parser("type", help="Human-like typing")
    type_parser.add_argument("text", type=str, help="Text to type")
    type_parser.add_argument("--paste", action="store_true", help="Paste via clipboard")

    # Press
    press_parser = subparsers.add_parser("press", help="Press key or combination (e.g. enter, tab, command+t)")
    press_parser.add_argument("key", type=str, help="Key name or combination separated by +")

    # Scroll
    scroll_parser = subparsers.add_parser("scroll", help="Smooth scroll")
    scroll_parser.add_argument("amount", type=int, help="Amount (negative=down, positive=up)")

    args = parser.parse_args()

    if args.command == "status":
        info = get_screen_info()
        print(json.dumps(info, indent=2))

    elif args.command == "screenshot":
        ok, res = take_screenshot(args.out, crop_active_window=args.window)
        print(json.dumps({"success": ok, "result": res}, indent=2))

    elif args.command == "focus":
        ok, msg = focus_app(args.app)
        print(json.dumps({"success": ok, "message": msg}, indent=2))

    elif args.command == "click":
        clicks = 2 if args.double else 1
        human_click(args.x, args.y, button=args.button, clicks=clicks)
        print(json.dumps({"success": True, "action": "click", "x": args.x, "y": args.y, "button": args.button, "clicks": clicks}))

    elif args.command == "move":
        human_move(args.x, args.y)
        print(json.dumps({"success": True, "action": "move", "x": args.x, "y": args.y}))

    elif args.command == "drag":
        human_move(args.x1, args.y1)
        pyautogui.mouseDown()
        time.sleep(0.1)
        human_move(args.x2, args.y2)
        pyautogui.mouseUp()
        print(json.dumps({"success": True, "action": "drag", "from": [args.x1, args.y1], "to": [args.x2, args.y2]}))

    elif args.command == "type":
        human_type(args.text, use_clipboard=args.paste)
        print(json.dumps({"success": True, "action": "type", "text": args.text}))

    elif args.command == "press":
        keys = [k.strip() for k in args.key.split("+")]
        if len(keys) == 1:
            pyautogui.press(keys[0])
        else:
            pyautogui.hotkey(*keys)
        print(json.dumps({"success": True, "action": "press", "keys": keys}))

    elif args.command == "scroll":
        human_scroll(args.amount)
        print(json.dumps({"success": True, "action": "scroll", "amount": args.amount}))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
