#!/bin/bash
cd ~/printer_data/config

# Ajouter toutes les modifs
git add .

# Commit avec date/heure
git commit -m "Auto-backup: $(date '+%Y-%m-%d %H:%M:%S')" || exit 0

# Push
git push origin main
