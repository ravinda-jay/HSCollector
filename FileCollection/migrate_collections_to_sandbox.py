import json
import sys
from pathlib import Path

# Usage:
# python migrate_collections_to_sandbox.py path/to/collections.json [path/to/output.json]
# If output path omitted -> data/sandbox_urls.json (next to input file)

ENV_IDS = {400, 310, 200, 160, 140, 120, 110, 100}
ENV_DESC = {
    400: "Mac Catalina 64 bit (x86)",
    310: "Linux (Ubuntu 20.04, 64 bit)",
    200: "Android Static Analysis",
    160: "Windows 10 64 bit",
    140: "Windows 11 64 bit",
    120: "Windows 7 64 bit",
    110: "Windows 7 32 bit (HWP Support)",
    100: "Windows 7 32 bit"
}


def normalize_entry(entry):
    # Known possible source keys: 'file', 'filepath', 'filename', 'file_to_submit', 'submit_file', 'environment_id'
    file_val = entry.get("file") or entry.get("filename") or entry.get("filepath") or ""
    file_to_submit = entry.get("file_to_submit") or entry.get("submit_file") or file_val
    env = entry.get("environment_id") or entry.get("env") or entry.get("environment") or None
    # Try to cast env to int if provided as string
    try:
        env_int = int(env) if env is not None and env != "" else None
    except Exception:
        env_int = None

    # Validate environment id; if missing or invalid, set to None
    if env_int not in ENV_IDS:
        env_int = None

    return {
        "file": file_val,
        "file_to_submit": file_to_submit,
        "environment_id": env_int
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python migrate_collections_to_sandbox.py path/to/collections.json [path/to/output.json]")
        sys.exit(2)
    in_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2]) if len(sys.argv) >= 3 else in_path.parent / "sandbox_urls.json"

    if not in_path.exists():
        print(f"Input file not found: {in_path}")
        sys.exit(2)

    with in_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # If data is an object with top-level collections list, try to find it.
    if isinstance(data, dict):
        candidate_keys = ["collections", "items", "files", "data"]
        list_val = None
        for k in candidate_keys:
            if k in data and isinstance(data[k], list):
                list_val = data[k]
                break
        if list_val is None:
            for k, v in data.items():
                if isinstance(v, list):
                    list_val = v
                    break
        if list_val is None:
            if isinstance(data, dict):
                list_val = [data]
            else:
                raise RuntimeError("Could not find a collections list in the input file.")
        entries = list_val
    elif isinstance(data, list):
        entries = data
    else:
        raise RuntimeError("Unexpected JSON structure in input file.")

    transformed = [normalize_entry(e) for e in entries]

    # Write output
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump({"sandbox_urls": transformed}, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(transformed)} entries to {out_path}")
    used_envs = sorted({e["environment_id"] for e in transformed if e["environment_id"] is not None})
    print("Detected environment IDs in output:", used_envs)
    print("Valid environment IDs:", sorted(ENV_IDS))
    unknowns = [i for i,e in enumerate(transformed) if e["environment_id"] is None]
    if unknowns:
        print(f"{len(unknowns)} entries had missing/invalid environment_id and were set to null. Please review them.")


if __name__ == "__main__":
    main()
