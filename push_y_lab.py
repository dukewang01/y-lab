"""
Push y-lab to GitHub via API (works when git://github.com:443 is blocked)
"""
import os, sys, base64, json
from pathlib import Path
import urllib.request

OWNER = "dukewang01"
REPO = "y-lab"
TOKEN = os.environ.get("GH_TOKEN", "")
ROOT = Path(r"C:\Users\Y\.openclaw\workspace\projects\y-lab")
API = f"https://api.github.com/repos/{OWNER}/{REPO}"

if not TOKEN:
    print("Set GH_TOKEN first")
    sys.exit(1)

def gh(method, path, data=None):
    url = API + "/" + path if path else API
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"token {TOKEN}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    if data:
        req.add_header("Content-Type", "application/json")
        body = json.dumps(data).encode()
    else:
        body = None
    try:
        resp = urllib.request.urlopen(req, data=body, timeout=30)
        return json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        r = e.read().decode()
        print(f"  HTTP {e.code}: {r[:300]}")
        return None

# Get latest commit on branch
print("Getting current state...")
# Check if repo has commits already
branches = gh("GET", "branches")
if branches is None or len(branches) == 0:
    print("Repo is empty, creating initial files...")
    # Upload all files one by one via contents API
    files = []
    for f in ROOT.rglob("*"):
        if not f.is_file(): continue
        rel = str(f.relative_to(ROOT)).replace("\\", "/")
        if rel.startswith(".git/") or "__pycache__" in rel or rel.endswith(".pyc"):
            continue
        files.append((rel, f.read_bytes()))
    
    # Sort: root files first, then deeper
    files.sort(key=lambda x: (x[0].count("/"), x[0]))
    
    for rel, content in files:
        encoded = base64.b64encode(content).decode()
        # Try contents API
        result = gh("PUT", "contents/" + rel, {
            "message": f"add {rel}",
            "content": encoded,
            "branch": "main",
        })
        if result:
            print(f"  + {rel}")
        else:
            print(f"  x {rel}")
else:
    # Repo has content, get latest SHA
    ref = gh("GET", "git/ref/heads/main")
    if not ref:
        print("Failed to get ref")
        sys.exit(1)
    
    latest_sha = ref["object"]["sha"]
    print(f"Latest commit: {latest_sha[:8]}")
    
    # Get current tree
    tree = gh("GET", f"git/trees/{latest_sha}")
    if not tree:
        print("Failed to get tree")
        sys.exit(1)
    
    # Remove old files and add new ones
    new_files = []
    for f in ROOT.rglob("*"):
        if not f.is_file(): continue
        rel = str(f.relative_to(ROOT)).replace("\\", "/")
        if rel.startswith(".git/") or "__pycache__" in rel or rel.endswith(".pyc"):
            continue
        encoded = base64.b64encode(f.read_bytes()).decode()
        blob = gh("POST", "git/blobs", {"content": encoded, "encoding": "base64"})
        if blob:
            new_files.append({
                "path": rel, "mode": "100644",
                "type": "blob", "sha": blob["sha"]
            })
            print(f"  blob {rel}")
    
    # Create new tree
    new_tree = gh("POST", "git/trees", {
        "base_tree": tree["sha"],
        "tree": new_files
    })
    if not new_tree:
        print("Tree creation failed")
        sys.exit(1)
    print(f"New tree: {new_tree['sha'][:8]}")
    
    # Create commit
    commit = gh("POST", "git/commits", {
        "message": "y-lab: 23 projects (10 v0.1 dev + 13 planning)",
        "tree": new_tree["sha"],
        "parents": [latest_sha]
    })
    if not commit:
        print("Commit failed")
        sys.exit(1)
    print(f"New commit: {commit['sha'][:8]}")
    
    # Update ref
    result = gh("PATCH", "git/refs/heads/main", {
        "sha": commit["sha"],
        "force": True
    })
    if result:
        print(f"\nDone! https://github.com/{OWNER}/{REPO}")
    else:
        print("Ref update failed")

print("Session done")
