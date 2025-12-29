This README explains the sandbox URL format and how to migrate your existing `data/collections.json` to the new `data/sandbox_urls.json` format.

Files added by helper:
- `migrate_collections_to_sandbox.py` - migration script. Run with Python 3.
- `data/sandbox_urls.json` - example output file with three sample entries.
- `crawler_loader_snippet.txt` - a short snippet showing how to load and iterate the new file.

Environment IDs supported:
- 400: Mac Catalina 64 bit (x86)
- 310: Linux (Ubuntu 20.04, 64 bit)
- 200: Android Static Analysis
- 160: Windows 10 64 bit
- 140: Windows 11 64 bit
- 120: Windows 7 64 bit
- 110: Windows 7 32 bit (HWP Support)
- 100: Windows 7 32 bit

How to run the migration (Windows PowerShell):

```powershell
# from the project root (where migrate_collections_to_sandbox.py lives):
python .\migrate_collections_to_sandbox.py .\data\collections.json
# or specify a custom output path:
python .\migrate_collections_to_sandbox.py .\data\collections.json .\data\sandbox_urls.json
```

After migration, update your crawler to load `data/sandbox_urls.json` and use `file`, `file_to_submit`, and `environment_id` from each entry. See `crawler_loader_snippet.txt` for a minimal example.
