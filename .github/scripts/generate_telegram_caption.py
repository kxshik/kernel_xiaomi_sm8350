#!/usr/bin/env python3
import html
import os
import subprocess

kernel = os.environ.get('KERNEL_NAME', '')
device = os.environ.get('DEVICE_NAME', '')
branch = os.environ.get('BRANCH_NAME', '')
builder = os.environ.get('KBUILD_BUILD_USER', 'batman')
host = os.environ.get('KBUILD_BUILD_HOST', 'darkknight')
commit_hash = os.environ.get('COMMIT_HASH', '')
commit_msg = html.escape(os.environ.get('COMMIT_MSG', ''))
min_dur = os.environ.get('MIN', '0')
sec_dur = os.environ.get('SEC', '0')
size = os.environ.get('FILE_SIZE', '')
md5 = os.environ.get('MD5_SUM', '')
compiler = os.environ.get('CLANG_VERSION', '')
repo = os.environ.get('GITHUB_REPOSITORY', '')
sha = os.environ.get('GITHUB_SHA', '')

base = (
    f"✅ <b>Kernel Build Succeeded!</b>\n\n"
    f"⚡ <b>Kernel:</b> <code>{kernel}</code>\n"
    f"📱 <b>Device:</b> <code>{device}</code>\n"
    f"🌿 <b>Branch:</b> <code>{branch}</code>\n"
    f"🦇 <b>Host:</b> <code>{builder}@{host}</code>\n"
    f"🔧 <b>Commit:</b> <a href=\"https://github.com/{repo}/commit/{sha}\">{commit_hash}</a> ({commit_msg})\n"
    f"⏱️ <b>Duration:</b> <code>{min_dur}m {sec_dur}s</code>\n"
    f"📦 <b>Size:</b> <code>{size}</code>\n"
    f"🛡️ <b>MD5:</b> <code>{md5}</code>\n"
    f"🛠️ <b>Compiler:</b> <code>{compiler}</code>\n\n"
    f"📝 <b>Changelog:</b>\n"
)

log_cmd = ['git', 'log', '-n', '15', '--no-merges', '--pretty=format:%h\t%s']
commits = subprocess.check_output(log_cmd, text=True).strip().splitlines()
emojis = ['✨', '🚀', '⚡', '🔧', '🛠️', '🎯', '💡', '🌟', '🔥', '⚙️', '💫', '💎', '🔋', '📌', '🎉']

lines = []
curr_len = len(base)
for i, line in enumerate(commits):
    if not line.strip():
        continue
    parts = line.split('\t', 1)
    h = parts[0]
    s = html.escape(parts[1]) if len(parts) > 1 else ''
    emoji = emojis[i % len(emojis)]
    entry = f"• {emoji} {s} (<code>{h}</code>)\n"
    if curr_len + len(entry) + 30 > 960:
        lines.append("• ➕ <i>...and more</i>\n")
        break
    lines.append(entry)
    curr_len += len(entry)

caption = base + ''.join(lines)
with open('caption.txt', 'w', encoding='utf-8') as f:
    f.write(caption)
