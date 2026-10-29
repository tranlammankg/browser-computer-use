# Browser Computer Use (Claude-Style for AI Agents)

<p align="center">
  <img src="https://img.shields.io/badge/Platform-macOS-lightgrey.svg" alt="Platform macOS">
  <img src="https://img.shields.io/badge/Node.js-%3E%3D18.0.0-green.svg" alt="Node Version">
  <img src="https://img.shields.io/badge/Python-%3E%3D3.10-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License MIT">
  <img src="https://img.shields.io/badge/Stealth-100%25%20Undetectable-brightgreen.svg" alt="Stealth">
</p>

An OS-level visual browser automation engine and AI Skill modeled after **Claude Computer Use**. Interacts with real browsers (Google Chrome, Safari, Brave) through screen capture, natural cubic Bézier mouse curves, and organic human typing cadence—bypassing Cloudflare, reCAPTCHA, and social media anti-bot detection without WebDriver or CDP flags.

---

## 🌐 Languages / Ngôn ngữ
- [🇺🇸 English](#-english)
- [🇻🇳 Tiếng Việt](#-tiếng-việt)

---

## 🇺🇸 English

### 💡 Why Browser Computer Use?

Standard browser automation frameworks (Puppeteer, Selenium, Playwright, Chrome DevTools Protocol) are immediately blocked by modern bot-protection engines (Cloudflare Turnstile, DataDome, Akamai, Facebook, Google) because:
1. `navigator.webdriver = true` flag is permanently enabled.
2. CDP runtime instrumentation triggers anti-bot traps (`Runtime.enable`).
3. Clean/empty browser profiles lack cookies, session tokens, and realistic hardware fingerprints.
4. Linear mouse teleportation and 0ms keypress delays reveal non-human automation.

**Browser Computer Use** operates at the macOS Operating System level:
* **Real Browser Profile**: Interacts with your personal Google Chrome/Safari instance with all logins, extensions, and sessions intact.
* **Cubic Bézier Mouse Dynamics**: Accelerates, decelerates, and introduces biological micro-tremors (1–2px) along trajectories.
* **Human Typing Cadence**: Gaussian jitter delays (35–95ms), pause punctuation, and automated clipboard injection for multi-byte Unicode/Vietnamese.
* **Zero Driver Footprint**: No CDP connection, no WebDriver, no browser script injection. 100% human-identical to anti-bot engines.

---

### 📦 Quick Start & Installation

Install dependencies and bundle the AI Skill in one command:

```bash
# 1. Clone repository
git clone https://github.com/tranlammankg/browser-computer-use.git
cd browser-computer-use

# 2. One-command installer (Registers skill globally and locally)
npm run install-skill

# 3. Run automated tests
npm test

# 4. Run interactive demo
npm run demo
```

---

### 🛠️ CLI & API Usage

```bash
# 1. Display Screen Status
python3 skills/browser-computer-use/scripts/computer_use.py status

# 2. Focus Google Chrome
python3 skills/browser-computer-use/scripts/computer_use.py focus "Google Chrome"

# 3. Capture Screen for Vision Models
python3 skills/browser-computer-use/scripts/computer_use.py screenshot --out /tmp/screen.png

# 4. Human-like Mouse Click
python3 skills/browser-computer-use/scripts/computer_use.py click 540 320

# 5. Organic Typing & Clipboard Paste
python3 skills/browser-computer-use/scripts/computer_use.py type "Hello world"
python3 skills/browser-computer-use/scripts/computer_use.py type "Long Vietnamese text" --paste

# 6. Smooth Scrolling
python3 skills/browser-computer-use/scripts/computer_use.py scroll -5
```

---

### 🔒 macOS Permissions

Ensure your terminal / agent host is granted:
- **Screen Recording**: `System Settings > Privacy & Security > Screen & System Audio Recording`
- **Accessibility**: `System Settings > Privacy & Security > Accessibility`

Verify anytime with:
```bash
python3 skills/browser-computer-use/scripts/check_permissions.py
```

---

## 🇻🇳 Tiếng Việt

### 💡 Tại sao cần Browser Computer Use?

Các thư viện tự động hóa truyền thống (Puppeteer, Selenium, Playwright, CDP) thường xuyên bị Cloudflare, Akamai, Facebook, Shopee hay Google chặn ("Báo Robot", "CAPTCHA loop") vì:
1. Trình duyệt tự động kích hoạt cờ W3C `navigator.webdriver = true`.
2. Chrome DevTools Protocol để lại dấu vết (`Runtime.enable`).
3. Môi trường profile trắng (không có cookie, lịch sử, phiên đăng nhập cũ).
4. Chuột "dịch chuyển tức thời" (teleport) và tốc độ gõ phím đều tăm tắp như máy.

**Browser Computer Use** áp dụng cơ chế giống **Claude Computer Use**:
* **Dùng Profile thật của bạn**: Thao tác trực tiếp trên Google Chrome/Safari chính chủ, giữ nguyên mọi tài khoản, cookie và phiên đăng nhập.
* **Đường cong chuột Bézier tự nhiên**: Tăng tốc, giảm tốc và có độ lệch rung tay sinh học (micro-tremor).
* **Nhịp gõ phím người thật**: Biến thiên độ trễ ngẫu nhiên (35–95ms), nghỉ khi gặp dấu câu, tự động dùng Clipboard (`Command + V`) với tiếng Việt có dấu.
* **Không để lại dấu vết**: Không inject script, không mở cổng CDP, biến `navigator.webdriver = false`.

---

### 📦 Cài đặt nhanh

Cài đặt trọn gói thư viện và kích hoạt AI Skill chỉ với một lệnh:

```bash
# 1. Clone repository
git clone https://github.com/tranlammankg/browser-computer-use.git
cd browser-computer-use

# 2. Cài đặt tự động (Cài đặt skill toàn cục và cho project)
npm run install-skill

# 3. Chạy kiểm tra tự động
npm test

# 4. Chạy demo tương tác
npm run demo
```

---

### 🛠️ Lệnh thao tác trong dòng lệnh (CLI)

```bash
# 1. Xem trạng thái màn hình
python3 skills/browser-computer-use/scripts/computer_use.py status

# 2. Đưa Google Chrome lên tiêu điểm (Foreground)
python3 skills/browser-computer-use/scripts/computer_use.py focus "Google Chrome"

# 3. Chụp ảnh màn hình cho AI phân tích
python3 skills/browser-computer-use/scripts/computer_use.py screenshot --out /tmp/screen.png

# 4. Click chuột như người thật
python3 skills/browser-computer-use/scripts/computer_use.py click 540 320

# 5. Gõ phím hoặc dán văn bản tiếng Việt
python3 skills/browser-computer-use/scripts/computer_use.py type "Hello world"
python3 skills/browser-computer-use/scripts/computer_use.py type "Nội dung tiếng Việt có dấu" --paste

# 6. Cuộn trang mượt mà
python3 skills/browser-computer-use/scripts/computer_use.py scroll -5
```

---

### 🔒 Cấp quyền macOS

Đảm bảo ứng dụng điều khiển (Antigravity / Terminal) đã được cấp:
- **Ghi màn hình (Screen Recording)**: `Cài đặt hệ thống > Quyền riêng tư & Bảo mật > Ghi màn hình`
- **Trợ năng (Accessibility)**: `Cài đặt hệ thống > Quyền riêng tư & Bảo mật > Trợ năng`

Kiểm tra trạng thái bất cứ lúc nào bằng lệnh:
```bash
python3 skills/browser-computer-use/scripts/check_permissions.py
```

---

## 📄 License
Phát hành theo giấy phép [MIT](LICENSE).
