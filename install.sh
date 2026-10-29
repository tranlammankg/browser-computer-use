#!/bin/bash
# ==============================================================================
# Script cài đặt Browser Computer Use (Claude-Style) cho macOS
# Sử dụng:
#   chmod +x install.sh
#   ./install.sh [--global | --project]
# ==============================================================================

set -e

MODE="${1:---global}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 Bắt đầu cài đặt Browser Computer Use (Claude-Style)..."

# 1. Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Lỗi: Chưa cài Python 3. Vui lòng cài Python 3 trước."
    exit 1
fi

echo "📦 1. Đang cài đặt thư viện phụ trợ (pyautogui, pynput, Pillow)..."
python3 -m pip install -q pyautogui pynput Pillow pyobjc-framework-quartz pyobjc-framework-ApplicationServices

# 2. Cài đặt theo mode
if [ "$MODE" = "--global" ]; then
    TARGET_DIR="$HOME/.gemini/config/skills/browser-computer-use"
    PLUGIN_DIR="$HOME/.gemini/config/plugins/browser-computer-use"
    
    echo "🌐 2. Đang cài đặt Global (dùng cho MỌI project trên máy này)..."
    mkdir -p "$TARGET_DIR/scripts"
    mkdir -p "$PLUGIN_DIR/skills/browser-computer-use/scripts"
    
    cp "$SCRIPT_DIR/.agents/skills/browser-computer-use/SKILL.md" "$TARGET_DIR/"
    cp "$SCRIPT_DIR/.agents/skills/browser-computer-use/scripts/"* "$TARGET_DIR/scripts/"
    chmod +x "$TARGET_DIR/scripts/"*.py
    
    # Cài plugin
    cp "$SCRIPT_DIR/.agents/skills/browser-computer-use/SKILL.md" "$PLUGIN_DIR/skills/browser-computer-use/"
    cp "$SCRIPT_DIR/.agents/skills/browser-computer-use/scripts/"* "$PLUGIN_DIR/skills/browser-computer-use/scripts/"
    chmod +x "$PLUGIN_DIR/skills/browser-computer-use/scripts/"*.py
    
    echo "✅ Đã cài đặt vào: $TARGET_DIR"
else
    echo "📁 2. Đang cài đặt cho Project cục bộ..."
    mkdir -p "$SCRIPT_DIR/.agents/skills/browser-computer-use/scripts"
    chmod +x "$SCRIPT_DIR/.agents/skills/browser-computer-use/scripts/"*.py
    echo "✅ Đã cấu hình tại .agents/skills/browser-computer-use/"
fi

# 3. Kiểm tra quyền
echo "🔍 3. Kiểm tra quyền hệ thống macOS (Screen Recording & Accessibility)..."
python3 "$SCRIPT_DIR/.agents/skills/browser-computer-use/scripts/check_permissions.py"

echo ""
echo "🎉 CÀI ĐẶT HOÀN TẤT!"
echo "Bạn có thể chạy thử ngay bằng lệnh: python3 demo.py"
