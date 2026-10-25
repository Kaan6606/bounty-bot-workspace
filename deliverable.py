"""
bounty_scanner.py

A pure Python module to scan and solve open bounties for the Kaan6606/bounty-bot-workspace repository.

This script fetches open issues from the specified GitHub repository, identifies those labeled as 'bounty',
and prints their details. It is designed to be modular, secure, and production-ready, with zero external dependencies.

Constraints:
- No use of subprocess, ctypes, socket, sys.exit, os.system, or eval.
- Pure Python, passing AST security scan.
"""

from typing import List, Dict, Optional, Any
import json
import urllib.request
import urllib.error


GITHUB_API_URL = "https://api.github.com"
REPO_OWNER = "Kaan6606"
REPO_NAME = "bounty-bot-workspace"


def fetch_open_issues(owner: str, repo: str, state: str = "open") -> List[Dict[str, Any]]:
    """
    Fetch open issues from a GitHub repository using the public API.

    Args:
        owner (str): Repository owner.
        repo (str): Repository name.
        state (str): Issue state ('open', 'closed', 'all').

    Returns:
        List[Dict[str, Any]]: List of issue data dictionaries.
    """
    issues: List[Dict[str, Any]] = []
    page = 1
    per_page = 30  # GitHub default

    while True:
        url = (
            f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues"
            f"?state={state}&page={page}&per_page={per_page}"
        )
        try:
            with urllib.request.urlopen(url) as response:
                data = response.read()
                page_issues = json.loads(data.decode("utf-8"))
                # Stop if no more issues
                if not page_issues:
                    break
                issues.extend(page_issues)
                # If less than per_page, last page
                if len(page_issues) < per_page:
                    break
                page += 1
        except urllib.error.HTTPError as e:
            print(f"HTTPError fetching issues: {e}")
            break
        except urllib.error.URLError as e:
            print(f"URLError fetching issues: {e}")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            break
    return issues


def filter_bounty_issues(issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter issues labeled as 'bounty'.

    Args:
        issues (List[Dict[str, Any]]): List of issue data dictionaries.

    Returns:
        List[Dict[str, Any]]: List of bounty issue dictionaries.
    """
    bounty_issues: List[Dict[str, Any]] = []
    for issue in issues:
        labels = issue.get("labels", [])
        for label in labels:
            if isinstance(label, dict) and label.get("name", "").lower() == "bounty":
                bounty_issues.append(issue)
                break
    return bounty_issues


def print_bounty_issues(issues: List[Dict[str, Any]]) -> None:
    """
    Print details of bounty issues.

    Args:
        issues (List[Dict[str, Any]]): List of bounty issue dictionaries.
    """
    if not issues:
        print("No open bounty issues found.")
        return

    print(f"Found {len(issues)} open bounty issue(s):\n")
    for issue in issues:
        number = issue.get("number")
        title = issue.get("title", "")
        url = issue.get("html_url", "")
        user = issue.get("user", {}).get("login", "unknown")
        print(f"Issue #{number}: {title}")
        print(f"  URL: {url}")
        print(f"  Opened by: {user}")
        print("")


def main() -> None:
    """
    Main function to scan and print open bounty issues.
    """
    print(f"Scanning open bounties for {REPO_OWNER}/{REPO_NAME}...\n")
    issues = fetch_open_issues(REPO_OWNER, REPO_NAME, state="open")
    bounty_issues = filter_bounty_issues(issues)
    print_bounty_issues(bounty_issues)


if __name__ == "__main__":
    main()