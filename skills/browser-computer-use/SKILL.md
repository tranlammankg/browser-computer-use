---
name: browser-computer-use
description: >-
  Use this skill to automate web browsers and desktop apps using OS-level visual interaction (like Claude Computer Use).
  Operates on the user's real browser profile via screen capture, human-like Bezier mouse movements, and natural typing,
  completely bypassing anti-bot systems, Cloudflare, CAPTCHAs, and social media bot detection.
---

# Browser Computer Use (Claude-Style OS Automation)

This skill enables visual, human-like browser automation at the operating system level on macOS.
Unlike Puppeteer, Selenium, or CDP tools which set `navigator.webdriver=true` and leak automation flags, this skill interacts directly through screen capture and OS mouse/keyboard input on the user's actual browser (Google Chrome, Safari, Brave) with their existing profiles, cookies, and login sessions.

## Architecture & How It Works

1. **Vision Feedback Loop**: Takes screenshots via macOS `screencapture`.
2. **Human Mouse Movement**: Computes cubic Bézier paths with acceleration, deceleration, and micro-tremors (never teleports).
3. **Organic Keystrokes**: Types with variable inter-key delays (35ms - 100ms) and natural punctuation pauses, or pastes via clipboard for large text.
4. **Zero Driver Footprint**: No CDP, no webdriver, no injected scripts. Undetectable by Cloudflare, Akamai, Facebook, Google, or Shopee.

---

## Tool CLI Reference

The helper script is located at:
`scripts/computer_use.py`

### 1. Check Screen & Status
```bash
python3 <skill-dir>/scripts/computer_use.py status
```
Returns JSON containing screen width, height, and current mouse position.

### 2. Focus the Browser
Brings Google Chrome (or Safari/Brave) to the foreground before interacting:
```bash
python3 <skill-dir>/scripts/computer_use.py focus "Google Chrome"
```

### 3. Capture Screen (Vision)
```bash
python3 <skill-dir>/scripts/computer_use.py screenshot --out /tmp/screen.png
```
Read the screenshot using vision tools to identify coordinates $(x, y)$ of target buttons, input fields, or links.

### 4. Human Mouse Click
```bash
# Single left click
python3 <skill-dir>/scripts/computer_use.py click <X> <Y>

# Double click
python3 <skill-dir>/scripts/computer_use.py click <X> <Y> --double

# Right click
python3 <skill-dir>/scripts/computer_use.py click <X> <Y> --button right
```

### 5. Human-like Typing
```bash
# Type text with natural delays
python3 <skill-dir>/scripts/computer_use.py type "Hello world"

# Paste text via clipboard (recommended for long paragraphs or Vietnamese text)
python3 <skill-dir>/scripts/computer_use.py type "Nội dung tiếng Việt hoặc đoạn văn dài" --paste
```

### 6. Keyboard Shortcuts & Special Keys
```bash
# Press single key (enter, tab, esc, space, backspace, up, down)
python3 <skill-dir>/scripts/computer_use.py press enter

# Hotkeys (combination with +)
python3 <skill-dir>/scripts/computer_use.py press "command+t"
python3 <skill-dir>/scripts/computer_use.py press "command+l"
python3 <skill-dir>/scripts/computer_use.py press "command+w"
```

### 7. Smooth Scrolling
```bash
# Scroll down
python3 <skill-dir>/scripts/computer_use.py scroll -5

# Scroll up
python3 <skill-dir>/scripts/computer_use.py scroll 5
```

---

## Typical Automation Workflow

When performing a web task (e.g. searching, navigating, logging in, posting):

1. **Focus Browser**: Run `focus "Google Chrome"`.
2. **Navigate**:
   - Run `press "command+l"` to focus the address bar.
   - Run `type "https://example.com" --paste` followed by `press enter`.
3. **Wait & Observe**: Wait 2-3 seconds, then take a `screenshot`.
4. **Locate Target**: Read the screenshot to calculate the $(x, y)$ coordinate of the target element.
5. **Act**:
   - Call `click <x> <y>` to click.
   - Or `type "<text>"` to input text.
6. **Verify**: Capture a follow-up screenshot to confirm the action succeeded before proceeding to the next step.

---

## macOS Permissions Check

If screenshot or click actions fail, verify permissions:
```bash
python3 <skill-dir>/scripts/check_permissions.py
```
- **Screen Recording**: `System Settings -> Privacy & Security -> Screen & System Audio Recording` -> Enable `Antigravity`.
- **Accessibility**: `System Settings -> Privacy & Security -> Accessibility` -> Enable `Antigravity`.
