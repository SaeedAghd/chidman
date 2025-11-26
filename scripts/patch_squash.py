#!/usr/bin/env python3
import re
from pathlib import Path

P = Path("store_analysis/migrations/0001_initial_squashed_0115_add_review_reminder_model.py")
if not P.exists():
    print("squashed migration not found:", P)
    raise SystemExit(1)

text = P.read_text(encoding="utf-8")

# Insert resolver helper after the 'import uuid' line (first occurrence)
if "\nimport uuid\n" in text:
    insert_at = text.find("\nimport uuid\n")
    # find end of that line
    end_line = text.find("\n", insert_at + 1)
    helper = (
        "\nimport importlib\n\n"
        "def _resolve(modpath, attr_path):\n"
        "    mod = importlib.import_module(modpath)\n"
        "    obj = mod\n"
        "    for part in attr_path.split('.'):\n"
        "        obj = getattr(obj, part)\n"
        "    return obj\n\n"
    )
    text = text[: end_line + 1] + helper + text[end_line + 1 :]
else:
    helper = (
        "import importlib\n\n"
        "def _resolve(modpath, attr_path):\n"
        "    mod = importlib.import_module(modpath)\n"
        "    obj = mod\n"
        "    for part in attr_path.split('.'):\n"
        "        obj = getattr(obj, part)\n"
        "    return obj\n\n"
    )
    text = helper + text

# Replace occurrences like: code=store_analysis.migrations.0009_... .func,
pattern = re.compile(r"code=store_analysis\.migrations\.([0-9A-Za-z_]+)\.([A-Za-z0-9_\.]+),")

def repl(m):
    mod = m.group(1)
    attr = m.group(2)
    return "code=_resolve('store_analysis.migrations.%s','%s')," % (mod, attr)

new_text = pattern.sub(repl, text)
P.write_text(new_text, encoding="utf-8")
print("patched squashed migration")


