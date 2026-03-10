#!/usr/bin/env python3
"""
publish.py
==========
Quantum Relaxation Ordering — simulation publish pipeline.

Usage
-----
    python3 scripts/publish.py --module m01
    python3 scripts/publish.py --module m01 --dry-run

What it does
------------
1. Runs the module's simulation script  (scripts/run_{module_id}.py)
2. Writes output to data/latest/{module_id}_*.json
3. Archives a timestamped copy to data/archive/
4. Updates data/manifest.json (generated, status → needs_quality_check)
5. Prints a summary

Conventions
-----------
- Each simulation script must accept --output-dir as an argument
  and write exactly the JSON files declared in manifest.json.
- Scripts are canonical. Notebooks are exploratory.
- Archive copies are never overwritten.
- The manifest is the single source of truth for the dashboard.

Stewards: Colla, A. & Warring, U.
Affiliation: Theory · Numerical · Experimental Quantum & Atomic Physics, Freiburg
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone

REPO_ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LATEST_DIR = os.path.join(REPO_ROOT, 'data', 'latest')
ARCHIVE_DIR= os.path.join(REPO_ROOT, 'data', 'archive')
MANIFEST   = os.path.join(REPO_ROOT, 'data', 'manifest.json')
SCRIPTS    = os.path.join(REPO_ROOT, 'scripts')

os.makedirs(LATEST_DIR,  exist_ok=True)
os.makedirs(ARCHIVE_DIR, exist_ok=True)


def load_manifest():
    with open(MANIFEST) as f:
        return json.load(f)


def save_manifest(manifest):
    with open(MANIFEST, 'w') as f:
        json.dump(manifest, f, indent=2)


def get_module(manifest, module_id):
    for m in manifest['modules']:
        if m['id'] == module_id:
            return m
    return None


def archive(module_id, ts_str):
    """Copy all data/latest/{module_id}_*.json to archive with timestamp prefix."""
    archived = []
    for fname in os.listdir(LATEST_DIR):
        if fname.startswith(module_id + '_') and fname.endswith('.json'):
            src = os.path.join(LATEST_DIR, fname)
            dst = os.path.join(ARCHIVE_DIR, f"{ts_str}_{fname}")
            shutil.copy2(src, dst)
            archived.append(dst)
    return archived


def run_module(module, dry_run=False):
    script = module.get('script')
    if not script:
        print(f"  [!] No script defined for {module['id']}")
        return False

    script_path = os.path.join(REPO_ROOT, script)
    if not os.path.exists(script_path):
        print(f"  [!] Script not found: {script_path}")
        return False

    cmd = [sys.executable, script_path,
           '--output-dir', LATEST_DIR,
           '--module-id', module['id']]

    print(f"  Command: {' '.join(cmd)}")
    if dry_run:
        print("  [dry-run] Skipping execution.")
        return True

    result = subprocess.run(cmd, cwd=REPO_ROOT)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description='Publish simulation results.')
    parser.add_argument('--module', required=True,
                        help='Module ID to run (e.g. m01)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Print what would happen without executing')
    parser.add_argument('--skip-run', action='store_true',
                        help='Skip simulation, just archive current latest and update manifest')
    args = parser.parse_args()

    ts = datetime.now(timezone.utc)
    ts_str = ts.strftime('%Y-%m-%dT%H-%M-%S')

    print(f"\n{'='*60}")
    print(f"  quantum-relaxation-ordering · publish pipeline")
    print(f"  Module  : {args.module}")
    print(f"  Time    : {ts.isoformat()}")
    print(f"  Dry-run : {args.dry_run}")
    print(f"{'='*60}\n")

    # Load manifest
    manifest = load_manifest()
    module   = get_module(manifest, args.module)
    if not module:
        print(f"[ERROR] Module '{args.module}' not found in manifest.json")
        print(f"  Available: {[m['id'] for m in manifest['modules']]}")
        sys.exit(1)

    print(f"[1] Module: {module['label']}")
    print(f"    Status: {module['status']}")
    print(f"    Script: {module.get('script', 'none')}")

    # Archive current latest (before overwriting)
    if not args.dry_run:
        archived = archive(args.module, ts_str)
        if archived:
            print(f"\n[2] Archived {len(archived)} file(s):")
            for a in archived:
                print(f"    {os.path.relpath(a, REPO_ROOT)}")
        else:
            print(f"\n[2] No existing latest files to archive.")

    # Run simulation
    if not args.skip_run:
        print(f"\n[3] Running simulation...")
        success = run_module(module, dry_run=args.dry_run)
        if not success:
            print("[ERROR] Simulation failed. Manifest not updated.")
            sys.exit(1)
        print("    Simulation complete.")
    else:
        print(f"\n[3] Skipping simulation (--skip-run).")

    # Update manifest
    if not args.dry_run:
        for m in manifest['modules']:
            if m['id'] == args.module:
                m['generated']  = ts.isoformat()
                m['status']     = 'needs_quality_check'
                m['status_label'] = 'needs quality check & discussion'
                manifest['meta']['last_updated'] = ts.strftime('%Y-%m-%d')
                break
        save_manifest(manifest)
        print(f"\n[4] Manifest updated.")

    print(f"\n{'='*60}")
    print(f"  Done. Push data/latest/ and data/manifest.json to update dashboard.")
    print(f"  data/archive/ stays local (not committed — add to .gitignore if large).")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
