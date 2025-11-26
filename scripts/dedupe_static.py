#!/usr/bin/env python
"""
Deduplicate static files across STATICFILES_DIRS.
Keeps the first occurrence (by order in STATICFILES_DIRS) and moves duplicates to a backup folder.
"""
import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

def setup_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
    try:
        import django
        django.setup()
    except Exception as e:
        print("Error setting up Django:", e)
        sys.exit(1)

def main(dry_run=True):
    setup_django()
    from django.conf import settings

    static_dirs = list(getattr(settings, 'STATICFILES_DIRS', []))
    if not static_dirs:
        print("No STATICFILES_DIRS configured in settings.")
        return

    # Normalize to Path
    static_dirs = [Path(p) for p in static_dirs]

    relmap = {}  # relpath -> list of (dir_index, abs_path)
    for idx, base in enumerate(static_dirs):
        if not base.exists():
            print(f"Warning: static dir does not exist: {base}")
            continue
        for root, dirs, files in os.walk(base):
            for f in files:
                abs_path = Path(root) / f
                rel = abs_path.relative_to(base)
                rel_str = str(rel).replace('\\', '/')
                relmap.setdefault(rel_str, []).append((idx, abs_path))

    duplicates = {k: v for k, v in relmap.items() if len(v) > 1}
    if not duplicates:
        print("No duplicate static files found.")
        return

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    backup_root = Path(settings.BASE_DIR) / 'static_duplicates_backup' / timestamp
    print(f"Found {len(duplicates)} duplicate paths. Backup dir: {backup_root}")
    if dry_run:
        print("Dry run mode (no files moved). Run with --apply to move duplicates.")

    for rel, entries in duplicates.items():
        # Sort by dir index (preserve first occurrence)
        entries_sorted = sorted(entries, key=lambda x: x[0])
        keeper = entries_sorted[0][1]
        extras = [p for _, p in entries_sorted[1:]]
        print(f"\nDuplicate: {rel}")
        print(f"  Keeper: {keeper}")
        for ex in extras:
            print(f"  Extra:  {ex}")
            if not dry_run:
                dest = backup_root / ex.relative_to(Path(settings.BASE_DIR))
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(ex), str(dest))
                print(f"    Moved to backup: {dest}")

    print("\nDone. Review the backup folder before removing or re-adding files.")

if __name__ == '__main__':
    apply_flag = '--apply' in sys.argv
    main(dry_run=not apply_flag)


