#!/usr/bin/env python3
import html
import os
import subprocess

emojis = ['✨', '🚀', '⚡', '🔧', '🛠️', '🎯', '💡', '🌟', '🔥', '⚙️', '💫', '💎', '🔋', '📌', '🎉']
log_cmd = ['git', 'log', '-n', '15', '--no-merges', '--pretty=format:%h\t%H\t%s']
commits = subprocess.check_output(log_cmd, text=True).strip().splitlines()
repo = os.environ.get('GITHUB_REPOSITORY', '')

with open('changelog.txt', 'w', encoding='utf-8') as f:
    f.write('### 📝 Changelog\n\n')
    for i, line in enumerate(commits):
        if not line.strip():
            continue
        parts = line.split('\t', 2)
        h = parts[0]
        full_h = parts[1]
        s = parts[2] if len(parts) > 2 else ''
        emoji = emojis[i % len(emojis)]
        f.write(f'* {emoji} {s} ([{h}](https://github.com/{repo}/commit/{full_h}))\n')
