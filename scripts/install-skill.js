#!/usr/bin/env node

/**
 * One-command installer for browser-computer-use AI Skill
 * Compatible with Antigravity, Claude, and standalone automation.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const os = require('os');

const rootDir = path.resolve(__dirname, '..');
const sourceSkillDir = path.join(rootDir, 'skills', 'browser-computer-use');
const homeDir = os.homedir();
const globalTargetDir = path.join(homeDir, '.gemini', 'config', 'skills', 'browser-computer-use');
const globalPluginDir = path.join(homeDir, '.gemini', 'config', 'plugins', 'browser-computer-use');
const localAgentDir = path.join(rootDir, '.agents', 'skills', 'browser-computer-use');

function copyRecursiveSync(src, dest) {
  const exists = fs.existsSync(src);
  const stats = exists && fs.statSync(src);
  const isDirectory = exists && stats.isDirectory();
  if (isDirectory) {
    fs.mkdirSync(dest, { recursive: true });
    fs.readdirSync(src).forEach((childItemName) => {
      copyRecursiveSync(path.join(src, childItemName), path.join(dest, childItemName));
    });
  } else {
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.copyFileSync(src, dest);
  }
}

console.log('🚀 Installing browser-computer-use AI Skill...');

// 1. Copy to local workspace
console.log(`📦 Copying to workspace: ${localAgentDir}`);
copyRecursiveSync(sourceSkillDir, localAgentDir);

// 2. Copy to global Antigravity config
console.log(`🌐 Copying to global config: ${globalTargetDir}`);
copyRecursiveSync(sourceSkillDir, globalTargetDir);

// 3. Copy to global plugin
const pluginScriptsDir = path.join(globalPluginDir, 'skills', 'browser-computer-use');
copyRecursiveSync(sourceSkillDir, pluginScriptsDir);

// 4. Ensure permissions on scripts
const chmodTarget = path.join(sourceSkillDir, 'scripts');
if (fs.existsSync(chmodTarget)) {
  fs.readdirSync(chmodTarget).forEach((file) => {
    if (file.endsWith('.py')) {
      try {
        fs.chmodSync(path.join(chmodTarget, file), 0o755);
        fs.chmodSync(path.join(localAgentDir, 'scripts', file), 0o755);
        fs.chmodSync(path.join(globalTargetDir, 'scripts', file), 0o755);
      } catch (e) {}
    }
  });
}

// 5. Install python dependencies
console.log('🐍 Checking & installing Python dependencies (pyautogui, pynput, Pillow)...');
try {
  execSync('python3 -m pip install -q pyautogui pynput Pillow pyobjc-framework-quartz pyobjc-framework-ApplicationServices', { stdio: 'inherit' });
} catch (err) {
  console.warn('⚠️ Warning: Could not auto-install Python packages via pip. Please ensure pyautogui and pynput are installed.');
}

// 6. Run permission check
console.log('🔍 Checking macOS permissions...');
try {
  execSync('python3 skills/browser-computer-use/scripts/check_permissions.py', { stdio: 'inherit' });
} catch (err) {
  // Ignored if permissions are not yet granted
}

console.log('\n🎉 browser-computer-use skill installed successfully!');
console.log('Run `npm test` to verify or `npm run demo` to see it in action.');
