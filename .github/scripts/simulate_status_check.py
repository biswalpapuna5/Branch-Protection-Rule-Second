import os
import requests
import sys

GITHUB_API = "https://api.github.com"
TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("REPO")
PR_NUMBER = os.getenv("PR_NUMBER")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

def get_pr_commit_sha():
    url = f"{GITHUB_API}/repos/{REPO}/pulls/{PR_NUMBER}"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()["head"]["sha"]

def is_even_last_char(sha):
    last_char = sha[-1]
    try:
        return int(last_char, 16) % 2 == 0
    except ValueError:
        return False

def comment_on_pr(message):
    url = f"{GITHUB_API}/repos/{REPO}/issues/{PR_NUMBER}/comments"
    data = {"body": message}
    resp = requests.post(url, headers=headers, json=data)
    if resp.status_code != 201:
        print(f"❌ Failed to post comment: {resp.status_code} - {resp.text}")
    else:
        print("💬 Comment posted on PR.")

def main():
    sha = get_pr_commit_sha()
    print(f"🔍 Commit SHA: {sha}")
    if is_even_last_char(sha):
        comment_on_pr(f"✅ Commit `{sha}` ends with even digit. Status check passed. Merge is allowed.")
        sys.exit(0)
    else:
        comment_on_pr(f"❌ Commit `{sha}` ends with odd digit. Status check failed. Merge is blocked.")
        sys.exit(1)

if __name__ == "__main__":
    main()
