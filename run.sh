#!/usr/bin/bash -eu

VAULT=~/Vault
# VAULT=~/ObsidianVault
# VAULT=~/repos/ankify/test_vault
VAULT_COPY=$(mktemp -d)

# --preserve makes the creation time be kept.
# --no-target-directory means we don't create the ObsidianVault directory inside temp.
cp --preserve --no-target-directory -r $VAULT $VAULT_COPY

./.venv/bin/python3 ankify/main.py $VAULT_COPY

diff --recursive --color $VAULT $VAULT_COPY || true

# read -p "Continue? " -n 1 -r </dev/tty
read -r -p "Continue? " answer
echo # (optional) move to a new line
if [[ $answer =~ ^[Yy]$ ]]; then
  cp --preserve --no-target-directory -r $VAULT_COPY $VAULT
  nautilus .
fi
