#!/bin/sh
export PATH="$HOME/.local/bin:$PATH"

source .venv/bin/activate

if ! grep -q "$PATH" /home/user/.bashrc; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> /home/user/.bashrc
fi

python -u src/main.py