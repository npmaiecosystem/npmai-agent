"""
tools_developer_cli.py
NPM Agent — Developer CLI Vertical
Covers: Git, GitHub, GitLab, Docker, PackageManager, VSCode,
        Terminal, Makefile, CMake, Debugger
"""

import os, sys, json, re, shutil, subprocess, tempfile, traceback, platform
from pathlib import Path
from typing import Optional

# ── auto-install deps ──────────────────────────────────────────────────────────
def _ensure(pkg: str, imp: str = None):
    n = imp or pkg
    try:
        __import__(n)
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", pkg, "-q"], check=False)

for _p, _i in [
    ("gitpython",    "git"),
    ("PyGithub",     "github"),
    ("python-gitlab","gitlab"),
    ("docker",       "docker"),
    ("psutil",       "psutil"),
    ("cryptography", "cryptography"),
]:
    _ensure(_p, _i)

# ── imports from agent_core ────────────────────────────────────────────────────
from agent_core import ToolResult, CredStore


# ══════════════════════════════════════════════════════════════════════════════
# 1. GitTool
# ══════════════════════════════════════════════════════════════════════════════
class GitTool:
    name = "git"
    description = (
        "Full local Git operations: init, clone, commit, push, pull, branch, "
        "merge, rebase, stash, tag, diff, log, blame, cherry-pick, submodules"
    )

    # ── helpers ────────────────────────────────────────────────────────────────
    @staticmethod
    def _run(args: list, cwd: str = None) -> tuple:
        """Returns (returncode, stdout+stderr)"""
        r = subprocess.run(
            ["git"] + args, cwd=cwd,
            capture_output=True, text=True
        )
        return r.returncode, (r.stdout + r.stderr).strip()

    # ── core ──────────────────────────────────────────────────────────────────
    @staticmethod
    def init(path: str) -> ToolResult:
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            rc, out = GitTool._run(["init"], cwd=path)
            return ToolResult(rc == 0, f"✓ Initialized repo at {path}\n{out}" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ git init failed: {e}")

    @staticmethod
    def clone(url: str, dest: str) -> ToolResult:
        try:
            rc, out = GitTool._run(["clone", url, dest])
            return ToolResult(rc == 0, f"✓ Cloned {url} → {dest}" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ git clone failed: {e}")

    @staticmethod
    def status(path: str) -> ToolResult:
        try:
            rc, out = GitTool._run(["status", "--short"], cwd=path)
            return ToolResult(rc == 0, out or "✓ Working tree clean", out)
        except Exception as e:
            return ToolResult(False, f"✗ git status failed: {e}")

    @staticmethod
    def add(path: str, files: str = ".") -> ToolResult:
        try:
            targets = files if isinstance(files, list) else [files]
            rc, out = GitTool._run(["add"] + targets, cwd=path)
            return ToolResult(rc == 0, f"✓ Staged: {files}" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ git add failed: {e}")

    @staticmethod
    def commit(path: str, message: str, all: bool = True) -> ToolResult:
        try:
            args = ["commit", "-m", message]
            if all:
                args.insert(1, "-a")
            rc, out = GitTool._run(args, cwd=path)
            return ToolResult(rc == 0, f"✓ Committed: {message}\n{out}" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ git commit failed: {e}")

    @staticmethod
    def push(path: str, remote: str = "origin", branch: str = "main") -> ToolResult:
        try:
            rc, out = GitTool._run(["push", remote, branch], cwd=path)
            return ToolResult(rc == 0, f"✓ Pushed to {remote}/{branch}" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ git push failed: {e}")

    @staticmethod
    def pull(path: str, remote: str = "origin", branch: str = "main") -> ToolResult:
        try:
            rc, out = GitTool._run(["pull", remote, branch], cwd=path)
            return ToolResult(rc == 0, f"✓ Pulled {remote}/{branch}\n{out}" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ git pull failed: {e}")

    @staticmethod
    def fetch(path: str, remote: str = "origin") -> ToolResult:
        try:
            rc, out = GitTool._run(["fetch", remote], cwd=path)
            return ToolResult(rc == 0, f"✓ Fetched {remote}" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ git fetch failed: {e}")

    @staticmethod
    def create_branch(path: str, name: str) -> ToolResult:
        try:
            rc, out = GitTool._run(["checkout", "-b", name], cwd=path)
            return ToolResult(rc == 0, f"✓ Created and switched to branch '{name}'" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ create branch failed: {e}")

    @staticmethod
    def checkout(path: str, branch: str) -> ToolResult:
        try:
            rc, out = GitTool._run(["checkout", branch], cwd=path)
            return ToolResult(rc == 0, f"✓ Switched to '{branch}'" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ git checkout failed: {e}")

    @staticmethod
    def merge(path: str, branch: str) -> ToolResult:
        try:
            rc, out = GitTool._run(["merge", branch], cwd=path)
            return ToolResult(rc == 0, f"✓ Merged '{branch}'\n{out}" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ git merge failed: {e}")

    @staticmethod
    def log(path: str, n: int = 10) -> ToolResult:
        try:
            fmt = "--pretty=format:%h %an %ar %s"
            rc, out = GitTool._run(["log", fmt, f"-{n}"], cwd=path)
            lines = out.splitlines()
            return ToolResult(rc == 0, f"✓ Last {len(lines)} commits", lines)
        except Exception as e:
            return ToolResult(False, f"✗ git log failed: {e}")

    @staticmethod
    def diff(path: str, file: str = None) -> ToolResult:
        try:
            args = ["diff"] + ([file] if file else [])
            rc, out = GitTool._run(args, cwd=path)
            return ToolResult(True, out or "✓ No differences", out)
        except Exception as e:
            return ToolResult(False, f"✗ git diff failed: {e}")

    @staticmethod
    def stash(path: str) -> ToolResult:
        try:
            rc, out = GitTool._run(["stash"], cwd=path)
            return ToolResult(rc == 0, f"✓ Stashed changes\n{out}" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ git stash failed: {e}")

    @staticmethod
    def stash_pop(path: str) -> ToolResult:
        try:
            rc, out = GitTool._run(["stash", "pop"], cwd=path)
            return ToolResult(rc == 0, f"✓ Stash popped\n{out}" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ git stash pop failed: {e}")

    @staticmethod
    def tag(path: str, name: str, message: str = "") -> ToolResult:
        try:
            args = ["tag", "-a", name, "-m", message or name]
            rc, out = GitTool._run(args, cwd=path)
            return ToolResult(rc == 0, f"✓ Tagged '{name}'" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ git tag failed: {e}")

    @staticmethod
    def reset(path: str, mode: str = "--soft", commit: str = "HEAD~1") -> ToolResult:
        try:
            rc, out = GitTool._run(["reset", mode, commit], cwd=path)
            return ToolResult(rc == 0, f"✓ Reset {mode} to {commit}" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ git reset failed: {e}")

    @staticmethod
    def rebase(path: str, branch: str) -> ToolResult:
        try:
            rc, out = GitTool._run(["rebase", branch], cwd=path)
            return ToolResult(rc == 0, f"✓ Rebased onto '{branch}'\n{out}" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ git rebase failed: {e}")

    @staticmethod
    def cherry_pick(path: str, commit: str) -> ToolResult:
        try:
            rc, out = GitTool._run(["cherry-pick", commit], cwd=path)
            return ToolResult(rc == 0, f"✓ Cherry-picked {commit}" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ git cherry-pick failed: {e}")

    @staticmethod
    def blame(path: str, file: str) -> ToolResult:
        try:
            rc, out = GitTool._run(["blame", "--porcelain", file], cwd=path)
            return ToolResult(rc == 0, f"✓ Blame for {file}", out)
        except Exception as e:
            return ToolResult(False, f"✗ git blame failed: {e}")

    @staticmethod
    def show(path: str, commit: str) -> ToolResult:
        try:
            rc, out = GitTool._run(["show", commit], cwd=path)
            return ToolResult(rc == 0, out[:3000], out)
        except Exception as e:
            return ToolResult(False, f"✗ git show failed: {e}")

    @staticmethod
    def remote_add(path: str, name: str, url: str) -> ToolResult:
        try:
            rc, out = GitTool._run(["remote", "add", name, url], cwd=path)
            return ToolResult(rc == 0, f"✓ Remote '{name}' added → {url}" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ remote add failed: {e}")

    @staticmethod
    def remote_list(path: str) -> ToolResult:
        try:
            rc, out = GitTool._run(["remote", "-v"], cwd=path)
            remotes = [l for l in out.splitlines() if l]
            return ToolResult(rc == 0, f"✓ {len(remotes)} remote entries", remotes)
        except Exception as e:
            return ToolResult(False, f"✗ remote list failed: {e}")

    @staticmethod
    def submodule_init(path: str) -> ToolResult:
        try:
            rc1, o1 = GitTool._run(["submodule", "init"], cwd=path)
            rc2, o2 = GitTool._run(["submodule", "update"], cwd=path)
            ok = rc1 == 0 and rc2 == 0
            return ToolResult(ok, f"✓ Submodules initialized\n{o1}\n{o2}" if ok else f"✗ {o1}\n{o2}")
        except Exception as e:
            return ToolResult(False, f"✗ submodule init failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# 2. GitHubTool (full API)
# ══════════════════════════════════════════════════════════════════════════════
class GitHubTool:
    name = "github"
    description = (
        "Full GitHub API: repos, issues, PRs, files, releases, Actions, "
        "branches, collaborators, gists, stars, forks"
    )
    use = (
            """
Name of Tool:- GitHubTool,

Purpose of Tool:- 
The GitHubTool provides a comprehensive interface to interact with the GitHub API. 
It supports full repository management (create, delete, fork), issue tracking (create, close, list), 
pull request lifecycle (create, merge, list, review), file operations (push, get, delete, list), 
releases, GitHub Actions workflows, branch management, collaborators, gists, starring, watching, 
and user information retrieval. 
All operations use authenticated access via a GitHub personal access token stored through CredStore. 
This tool is designed for automation, agentic workflows, and remote GitHub repository management without needing local git clones.

Methods:-
- _gh: Internal helper to initialize authenticated GitHub client.
- create_repo: Creates a new repository for the authenticated user.
- delete_repo: Permanently deletes a repository.
- fork_repo: Creates a fork of an existing repository.
- create_issue: Creates a new issue in a repository.
- close_issue: Closes an existing issue.
- list_issues: Retrieves a list of issues with optional filtering.
- create_pr: Creates a new pull request.
- merge_pr: Merges an existing pull request.
- list_prs: Lists pull requests in a repository.
- review_pr: Submits a review on a pull request.
- push_file: Creates or updates a single file in the repository.
- delete_file: Deletes a file from the repository.
- get_file: Retrieves the content of a file from the repository.
- list_files: Lists files and directories at a given path.
- create_release: Creates a new GitHub release.
- get_actions_status: Gets recent workflow run status.
- trigger_workflow: Triggers a GitHub Actions workflow.
- list_branches: Lists all branches in a repository.
- protect_branch: Applies basic protection rules to a branch.
- add_collaborator: Adds a collaborator to a repository with specified permissions.
- create_gist: Creates a new gist with one or more files.
- get_user_info: Retrieves public information about a GitHub user.
- star_repo: Stars a repository.
- watch_repo: Watches (subscribes to notifications) a repository.

How to use Tool Methods:-

1. _gh (Internal Authentication Helper):
   - Purpose: Creates and returns an authenticated PyGithub Github client instance.
   - Arguments:
     a) cred_key: str (default: "github") - The key used to load credentials from CredStore.
   - Note: This method is called internally by all other methods. You generally do not call it directly.
   - Requirement: A valid GitHub token must be saved using CredStore.save('github', {'token': 'ghp_...'})

2. create_repo:
   - Purpose: Creates a new GitHub repository for the authenticated user with automatic initialization.
   - Arguments:
     a) name: str - Name of the repository to create (required).
     b) private: bool (default: True) - Whether the repo should be private.
     c) description: str (default: "") - Short description of the repository.
     d) cred_key: str (default: "github") - Credential key for authentication.
   - Returns: ToolResult with success status, message, and repo details (url, full_name).
   - How to call: GitHubTool.create_repo(name="my-awesome-project", private=True, description="Project description")

3. delete_repo:
   - Purpose: Permanently deletes a repository (use with caution).
   - Arguments:
     a) repo: str - Full name of the repository in "owner/repo" format (required).
     b) cred_key: str (default: "github").
   - How to call: GitHubTool.delete_repo(repo="username/my-repo")

4. fork_repo:
   - Purpose: Creates a fork of any public or accessible repository under the authenticated user.
   - Arguments:
     a) repo: str - Repository to fork in "owner/repo" format.
     b) cred_key: str (default: "github").
   - How to call: GitHubTool.fork_repo(repo="octocat/Hello-World")

5. create_issue:
   - Purpose: Opens a new issue in a repository.
   - Arguments:
     a) repo: str - Target repository "owner/repo".
     b) title: str - Issue title (required).
     c) body: str (default: "") - Detailed issue description.
     d) labels: list (default: None) - List of label names.
     e) assignees: list (default: None) - List of usernames to assign.
     f) cred_key: str (default: "github").
   - How to call: GitHubTool.create_issue(repo="owner/repo", title="Bug found", body="Details...", labels=["bug"])

6. close_issue:
   - Purpose: Closes an open issue.
   - Arguments:
     a) repo: str - Repository "owner/repo".
     b) number: int - Issue number.
     c) cred_key: str (default: "github").
   - How to call: GitHubTool.close_issue(repo="owner/repo", number=42)

7. list_issues:
   - Purpose: Lists issues with optional state and label filters.
   - Arguments:
     a) repo: str - Repository "owner/repo".
     b) state: str (default: "open") - "open", "closed", or "all".
     c) labels: list (default: None) - Filter by labels.
     d) cred_key: str (default: "github").
   - Returns: List of issues with number, title, state, and URL.
   - How to call: GitHubTool.list_issues(repo="owner/repo", state="open")

8. create_pr:
   - Purpose: Creates a new pull request.
   - Arguments:
     a) repo: str - Target repository.
     b) title: str - PR title.
     c) body: str - PR description.
     d) head: str - Source branch (e.g., "feature-branch").
     e) base: str (default: "main") - Target branch.
     f) cred_key: str (default: "github").
   - How to call: GitHubTool.create_pr(repo="owner/repo", title="New feature", body="...", head="feature-x", base="main")

9. merge_pr:
   - Purpose: Merges a pull request using specified method.
   - Arguments:
     a) repo: str
     b) number: int - PR number.
     c) method: str (default: "squash") - Can be "merge", "squash", or "rebase".
     d) cred_key: str (default: "github").
   - How to call: GitHubTool.merge_pr(repo="owner/repo", number=5, method="squash")

10. list_prs:
    - Purpose: Lists open or closed pull requests.
    - Arguments: repo, state (default "open"), cred_key.
    - How to call: GitHubTool.list_prs(repo="owner/repo", state="open")

11. review_pr:
    - Purpose: Submits a review comment/approval on a PR.
    - Arguments:
      a) repo: str
      b) number: int
      c) body: str - Review comment.
      d) event: str (default: "COMMENT") - Can be "APPROVE", "REQUEST_CHANGES", "COMMENT".
      e) cred_key.
    - How to call: GitHubTool.review_pr(repo="owner/repo", number=10, body="Looks good!", event="APPROVE")

12. push_file:
    - Purpose: Creates a new file or updates an existing file in the repository.
    - Arguments:
      a) repo: str
      b) path: str - File path in repo (e.g., "folder/file.py").
      c) content: str - Full file content.
      d) message: str (default: "Update via NPM Agent") - Commit message.
      e) cred_key.
    - How to call: GitHubTool.push_file(repo="owner/repo", path="README.md", content="# Title", message="Update readme")

13. delete_file:
    - Purpose: Deletes a file from the repository.
    - Arguments: repo, path, message, cred_key.
    - How to call: GitHubTool.delete_file(repo="owner/repo", path="oldfile.txt", message="Remove obsolete file")

14. get_file:
    - Purpose: Retrieves the decoded content of a file.
    - Arguments: repo, path, cred_key.
    - Returns: File content as string.
    - How to call: GitHubTool.get_file(repo="owner/repo", path="src/main.py")

15. list_files:
    - Purpose: Lists contents of a directory in the repository.
    - Arguments:
      a) repo: str
      b) path: str (default: "") - Directory path (empty = root).
      c) cred_key.
    - How to call: GitHubTool.list_files(repo="owner/repo", path="src")

16. create_release:
    - Purpose: Creates a new GitHub release.
    - Arguments: repo, tag, name, body, cred_key.
    - How to call: GitHubTool.create_release(repo="owner/repo", tag="v1.0.0", name="Version 1.0", body="Release notes")

17. get_actions_status:
    - Purpose: Gets the status of the most recent workflow runs.
    - Arguments: repo, cred_key.
    - How to call: GitHubTool.get_actions_status(repo="owner/repo")

18. trigger_workflow:
    - Purpose: Manually triggers a GitHub Actions workflow.
    - Arguments:
      a) repo: str
      b) workflow_id: str - Workflow filename or ID.
      c) ref: str (default: "main") - Branch or tag to run on.
      d) cred_key.
    - How to call: GitHubTool.trigger_workflow(repo="owner/repo", workflow_id="ci.yml", ref="main")

19. list_branches:
    - Purpose: Lists all branches in the repository.
    - Arguments: repo, cred_key.
    - How to call: GitHubTool.list_branches(repo="owner/repo")

20. protect_branch:
    - Purpose: Enables basic branch protection (requires 1 approving review).
    - Arguments: repo, branch, cred_key.
    - How to call: GitHubTool.protect_branch(repo="owner/repo", branch="main")

21. add_collaborator:
    - Purpose: Invites a user as collaborator with specified permission level.
    - Arguments:
      a) repo: str
      b) user: str - GitHub username.
      c) permission: str (default: "push") - "pull", "push", "triage", "maintain", "admin".
      d) cred_key.
    - How to call: GitHubTool.add_collaborator(repo="owner/repo", user="friend", permission="push")

22. create_gist:
    - Purpose: Creates a new public or secret gist.
    - Arguments:
      a) files: dict - {"filename.ext": "file content", ...}
      b) description: str (default: "")
      c) public: bool (default: True)
      d) cred_key.
    - How to call: GitHubTool.create_gist(files={"hello.py": "print('Hello')"}, description="My gist", public=True)

23. get_user_info:
    - Purpose: Gets basic information about any GitHub user.
    - Arguments: username: str, cred_key.
    - How to call: GitHubTool.get_user_info(username="octocat")

24. star_repo:
    - Purpose: Stars a repository for the authenticated user.
    - Arguments: repo, cred_key.
    - How to call: GitHubTool.star_repo(repo="owner/repo")

25. watch_repo:
    - Purpose: Watches a repository to receive notifications.
    - Arguments: repo, cred_key.
    - How to call: GitHubTool.watch_repo(repo="owner/repo")
""")

    @staticmethod
    def _gh(cred_key: str = "github"):
        from github import Github
        token = CredStore.load(cred_key).get("token", "")
        if not token:
            raise ValueError("No GitHub token. Save via CredStore.save('github', {'token':'...'}).")
        return Github(token)

    @staticmethod
    def create_repo(name: str, private: bool = True, description: str = "",
                    cred_key: str = "github") -> ToolResult:
        try:
            gh = GitHubTool._gh(cred_key)
            user = gh.get_user()
            repo = user.create_repo(name=name, private=private, description=description, auto_init=True)
            return ToolResult(True, f"✓ Repo created: {repo.html_url}", {"url": repo.html_url, "full_name": repo.full_name})
        except Exception as e:
            return ToolResult(False, f"✗ create_repo failed: {e}")

    @staticmethod
    def delete_repo(repo: str, cred_key: str = "github") -> ToolResult:
        try:
            gh = GitHubTool._gh(cred_key)
            gh.get_repo(repo).delete()
            return ToolResult(True, f"✓ Repo '{repo}' deleted")
        except Exception as e:
            return ToolResult(False, f"✗ delete_repo failed: {e}")

    @staticmethod
    def fork_repo(repo: str, cred_key: str = "github") -> ToolResult:
        try:
            gh = GitHubTool._gh(cred_key)
            fork = gh.get_user().create_fork(gh.get_repo(repo))
            return ToolResult(True, f"✓ Forked → {fork.html_url}", {"url": fork.html_url})
        except Exception as e:
            return ToolResult(False, f"✗ fork_repo failed: {e}")

    @staticmethod
    def create_issue(repo: str, title: str, body: str = "",
                     labels: list = None, assignees: list = None,
                     cred_key: str = "github") -> ToolResult:
        try:
            gh = GitHubTool._gh(cred_key)
            issue = gh.get_repo(repo).create_issue(
                title=title, body=body,
                labels=labels or [], assignees=assignees or []
            )
            return ToolResult(True, f"✓ Issue #{issue.number}: {issue.html_url}", {"number": issue.number, "url": issue.html_url})
        except Exception as e:
            return ToolResult(False, f"✗ create_issue failed: {e}")

    @staticmethod
    def close_issue(repo: str, number: int, cred_key: str = "github") -> ToolResult:
        try:
            gh = GitHubTool._gh(cred_key)
            gh.get_repo(repo).get_issue(number).edit(state="closed")
            return ToolResult(True, f"✓ Issue #{number} closed")
        except Exception as e:
            return ToolResult(False, f"✗ close_issue failed: {e}")

    @staticmethod
    def list_issues(repo: str, state: str = "open", labels: list = None,
                    cred_key: str = "github") -> ToolResult:
        try:
            gh = GitHubTool._gh(cred_key)
            kwargs = {"state": state}
            if labels:
                kwargs["labels"] = labels
            issues = gh.get_repo(repo).get_issues(**kwargs)
            data = [{"#": i.number, "title": i.title, "state": i.state, "url": i.html_url} for i in issues]
            return ToolResult(True, f"✓ {len(data)} issues", data)
        except Exception as e:
            return ToolResult(False, f"✗ list_issues failed: {e}")

    @staticmethod
    def create_pr(repo: str, title: str, body: str, head: str, base: str = "main",
                  cred_key: str = "github") -> ToolResult:
        try:
            gh = GitHubTool._gh(cred_key)
            pr = gh.get_repo(repo).create_pull(title=title, body=body, head=head, base=base)
            return ToolResult(True, f"✓ PR #{pr.number}: {pr.html_url}", {"number": pr.number, "url": pr.html_url})
        except Exception as e:
            return ToolResult(False, f"✗ create_pr failed: {e}")

    @staticmethod
    def merge_pr(repo: str, number: int, method: str = "squash",
                 cred_key: str = "github") -> ToolResult:
        try:
            gh = GitHubTool._gh(cred_key)
            pr = gh.get_repo(repo).get_pull(number)
            result = pr.merge(merge_method=method)
            return ToolResult(result.merged, f"✓ PR #{number} merged" if result.merged else f"✗ Merge failed: {result.message}")
        except Exception as e:
            return ToolResult(False, f"✗ merge_pr failed: {e}")

    @staticmethod
    def list_prs(repo: str, state: str = "open", cred_key: str = "github") -> ToolResult:
        try:
            gh = GitHubTool._gh(cred_key)
            prs = gh.get_repo(repo).get_pulls(state=state)
            data = [{"#": p.number, "title": p.title, "head": p.head.ref, "base": p.base.ref, "url": p.html_url} for p in prs]
            return ToolResult(True, f"✓ {len(data)} PRs", data)
        except Exception as e:
            return ToolResult(False, f"✗ list_prs failed: {e}")

    @staticmethod
    def review_pr(repo: str, number: int, body: str, event: str = "COMMENT",
                  cred_key: str = "github") -> ToolResult:
        try:
            gh = GitHubTool._gh(cred_key)
            pr = gh.get_repo(repo).get_pull(number)
            review = pr.create_review(body=body, event=event)
            return ToolResult(True, f"✓ Review submitted on PR #{number}", {"id": review.id})
        except Exception as e:
            return ToolResult(False, f"✗ review_pr failed: {e}")

    @staticmethod
    def push_file(repo: str, path: str, content: str,
                  message: str = "Update via NPM Agent",
                  cred_key: str = "github") -> ToolResult:
        try:
            gh = GitHubTool._gh(cred_key)
            r = gh.get_repo(repo)
            try:
                existing = r.get_contents(path)
                r.update_file(path, message, content, existing.sha)
                return ToolResult(True, f"✓ Updated {path} in {repo}")
            except Exception:
                r.create_file(path, message, content)
                return ToolResult(True, f"✓ Created {path} in {repo}")
        except Exception as e:
            return ToolResult(False, f"✗ push_file failed: {e}")

    @staticmethod
    def delete_file(repo: str, path: str, message: str = "Delete via NPM Agent",
                    cred_key: str = "github") -> ToolResult:
        try:
            gh = GitHubTool._gh(cred_key)
            r = gh.get_repo(repo)
            contents = r.get_contents(path)
            r.delete_file(path, message, contents.sha)
            return ToolResult(True, f"✓ Deleted {path} from {repo}")
        except Exception as e:
            return ToolResult(False, f"✗ delete_file failed: {e}")

    @staticmethod
    def get_file(repo: str, path: str, cred_key: str = "github") -> ToolResult:
        try:
            import base64
            gh = GitHubTool._gh(cred_key)
            f = gh.get_repo(repo).get_contents(path)
            content = base64.b64decode(f.content).decode(errors="replace")
            return ToolResult(True, f"✓ Got {path}", content)
        except Exception as e:
            return ToolResult(False, f"✗ get_file failed: {e}")

    @staticmethod
    def list_files(repo: str, path: str = "", cred_key: str = "github") -> ToolResult:
        try:
            gh = GitHubTool._gh(cred_key)
            contents = gh.get_repo(repo).get_contents(path)
            files = [{"name": f.name, "type": f.type, "path": f.path} for f in contents]
            return ToolResult(True, f"✓ {len(files)} entries in '{path or '/'}'", files)
        except Exception as e:
            return ToolResult(False, f"✗ list_files failed: {e}")

    @staticmethod
    def create_release(repo: str, tag: str, name: str, body: str = "",
                       cred_key: str = "github") -> ToolResult:
        try:
            gh = GitHubTool._gh(cred_key)
            rel = gh.get_repo(repo).create_git_release(tag=tag, name=name, message=body)
            return ToolResult(True, f"✓ Release '{name}' created: {rel.html_url}", {"url": rel.html_url})
        except Exception as e:
            return ToolResult(False, f"✗ create_release failed: {e}")

    @staticmethod
    def get_actions_status(repo: str, cred_key: str = "github") -> ToolResult:
        try:
            gh = GitHubTool._gh(cred_key)
            runs = list(gh.get_repo(repo).get_workflow_runs())[:10]
            data = [{"id": r.id, "name": r.name, "status": r.status, "conclusion": r.conclusion} for r in runs]
            return ToolResult(True, f"✓ {len(data)} recent workflow runs", data)
        except Exception as e:
            return ToolResult(False, f"✗ get_actions_status failed: {e}")

    @staticmethod
    def trigger_workflow(repo: str, workflow_id: str, ref: str = "main",
                         cred_key: str = "github") -> ToolResult:
        try:
            import requests
            token = CredStore.load(cred_key).get("token", "")
            url = f"https://api.github.com/repos/{repo}/actions/workflows/{workflow_id}/dispatches"
            r = requests.post(url, headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
                              json={"ref": ref}, timeout=15)
            return ToolResult(r.status_code == 204, f"✓ Workflow triggered" if r.status_code == 204 else f"✗ {r.text}")
        except Exception as e:
            return ToolResult(False, f"✗ trigger_workflow failed: {e}")

    @staticmethod
    def list_branches(repo: str, cred_key: str = "github") -> ToolResult:
        try:
            gh = GitHubTool._gh(cred_key)
            branches = [b.name for b in gh.get_repo(repo).get_branches()]
            return ToolResult(True, f"✓ {len(branches)} branches", branches)
        except Exception as e:
            return ToolResult(False, f"✗ list_branches failed: {e}")

    @staticmethod
    def protect_branch(repo: str, branch: str, cred_key: str = "github") -> ToolResult:
        try:
            gh = GitHubTool._gh(cred_key)
            b = gh.get_repo(repo).get_branch(branch)
            b.edit_protection(required_approving_review_count=1)
            return ToolResult(True, f"✓ Branch '{branch}' protected")
        except Exception as e:
            return ToolResult(False, f"✗ protect_branch failed: {e}")

    @staticmethod
    def add_collaborator(repo: str, user: str, permission: str = "push",
                         cred_key: str = "github") -> ToolResult:
        try:
            gh = GitHubTool._gh(cred_key)
            gh.get_repo(repo).add_to_collaborators(user, permission=permission)
            return ToolResult(True, f"✓ Added '{user}' as collaborator with '{permission}' permission")
        except Exception as e:
            return ToolResult(False, f"✗ add_collaborator failed: {e}")

    @staticmethod
    def create_gist(files: dict, description: str = "", public: bool = True,
                    cred_key: str = "github") -> ToolResult:
        try:
            from github import InputFileContent
            gh = GitHubTool._gh(cred_key)
            gist_files = {name: InputFileContent(content) for name, content in files.items()}
            gist = gh.get_user().create_gist(public=public, files=gist_files, description=description)
            return ToolResult(True, f"✓ Gist created: {gist.html_url}", {"url": gist.html_url})
        except Exception as e:
            return ToolResult(False, f"✗ create_gist failed: {e}")

    @staticmethod
    def get_user_info(username: str, cred_key: str = "github") -> ToolResult:
        try:
            gh = GitHubTool._gh(cred_key)
            u = gh.get_user(username)
            data = {"login": u.login, "name": u.name, "bio": u.bio,
                    "public_repos": u.public_repos, "followers": u.followers}
            return ToolResult(True, f"✓ User info for '{username}'", data)
        except Exception as e:
            return ToolResult(False, f"✗ get_user_info failed: {e}")

    @staticmethod
    def star_repo(repo: str, cred_key: str = "github") -> ToolResult:
        try:
            gh = GitHubTool._gh(cred_key)
            gh.get_user().add_to_starred(gh.get_repo(repo))
            return ToolResult(True, f"✓ Starred '{repo}'")
        except Exception as e:
            return ToolResult(False, f"✗ star_repo failed: {e}")

    @staticmethod
    def watch_repo(repo: str, cred_key: str = "github") -> ToolResult:
        try:
            gh = GitHubTool._gh(cred_key)
            gh.get_user().add_to_watched(gh.get_repo(repo))
            return ToolResult(True, f"✓ Now watching '{repo}'")
        except Exception as e:
            return ToolResult(False, f"✗ watch_repo failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# 3. GitLabTool
# ══════════════════════════════════════════════════════════════════════════════
class GitLabTool:
    name = "gitlab"
    description = (
        "Full GitLab API: projects, issues, merge requests, pipelines, "
        "jobs, files, branches, members")
    use = (
            """
Name of Tool:- GitLabTool,

Purpose of Tool:- 
The GitLabTool provides a comprehensive interface to interact with the GitLab API (self-hosted or gitlab.com). 
It supports complete project management (create, list, get), issue tracking (create, close), merge requests (create, merge), 
CI/CD pipelines and jobs (list, trigger, retry), file operations (push/create/update), branch management, 
and project member management. 
All operations use authenticated access via a GitLab private token (and optional custom URL) stored through CredStore. 
This tool is ideal for automation, agentic workflows, DevOps pipelines, and remote GitLab project management.

Methods:-
- _gl: Internal helper to initialize authenticated GitLab client.
- create_project: Creates a new GitLab project.
- list_projects: Lists projects owned by the authenticated user.
- get_project: Retrieves detailed information about a specific project.
- create_issue: Creates a new issue in a project.
- close_issue: Closes an existing issue.
- create_mr: Creates a new merge request.
- merge_mr: Merges a merge request.
- list_pipelines: Lists recent pipelines for a project.
- trigger_pipeline: Triggers a new pipeline run.
- get_pipeline_jobs: Gets jobs for a specific pipeline.
- retry_job: Retries a failed or canceled job.
- push_file: Creates or updates a file in the repository.
- list_branches: Lists all branches in a project.
- create_branch: Creates a new branch.
- list_members: Lists project members.
- add_member: Adds a new member to a project with specified access level.

How to use Tool Methods:-

1. _gl (Internal Authentication Helper):
   - Purpose: Creates and returns an authenticated python-gitlab client instance. Handles both gitlab.com and self-hosted instances.
   - Arguments:
     a) cred_key: str (default: "gitlab") - The key used to load credentials from CredStore.
   - Credential format expected in CredStore: {'token': 'glpat-...', 'url': 'https://gitlab.example.com'} (url is optional, defaults to https://gitlab.com).
   - Note: This method is called internally by all other methods. You generally do not call it directly.
   - Requirement: A valid private token must be saved using CredStore.save('gitlab', {'token': 'glpat-...', 'url': 'https://...'}).

2. create_project:
   - Purpose: Creates a new project (repository) under the authenticated user.
   - Arguments:
     a) name: str - Name of the project (required).
     b) visibility: str (default: "private") - Visibility level: "private", "internal", or "public".
     c) cred_key: str (default: "gitlab").
   - Returns: ToolResult with success status, message, and project details (id, url).
   - How to call: GitLabTool.create_project(name="my-awesome-project", visibility="private")

3. list_projects:
   - Purpose: Lists all projects owned by the authenticated user.
   - Arguments:
     a) cred_key: str (default: "gitlab").
   - Returns: List of projects with id, name, and web_url.
   - How to call: GitLabTool.list_projects()

4. get_project:
   - Purpose: Retrieves detailed metadata for a specific project by its numeric ID.
   - Arguments:
     a) id: int - Project ID (numeric, not path).
     b) cred_key: str (default: "gitlab").
   - Returns: Project details including id, name, description, url, default_branch.
   - How to call: GitLabTool.get_project(id=123456)

5. create_issue:
   - Purpose: Opens a new issue in a project.
   - Arguments:
     a) project_id: int - Project ID (required).
     b) title: str - Issue title (required).
     c) description: str (default: "") - Detailed description of the issue.
     d) labels: list (default: None) - List of label names.
     e) cred_key: str (default: "gitlab").
   - Returns: Issue IID and web_url.
   - How to call: GitLabTool.create_issue(project_id=123, title="Bug found", description="Details here", labels=["bug", "backend"])

6. close_issue:
   - Purpose: Closes an open issue using its IID.
   - Arguments:
     a) project_id: int
     b) iid: int - Internal Issue ID (not global ID).
     c) cred_key: str (default: "gitlab").
   - How to call: GitLabTool.close_issue(project_id=123, iid=45)

7. create_mr:
   - Purpose: Creates a new merge request (equivalent to Pull Request).
   - Arguments:
     a) project_id: int
     b) title: str - MR title.
     c) source: str - Source branch name.
     d) target: str - Target branch name (usually "main" or "master").
     e) description: str (default: "") - MR description.
     f) cred_key: str (default: "gitlab").
   - Returns: MR IID and web_url.
   - How to call: GitLabTool.create_mr(project_id=123, title="Add new feature", source="feature-branch", target="main", description="...")

8. merge_mr:
   - Purpose: Merges an open merge request.
   - Arguments:
     a) project_id: int
     b) iid: int - Merge Request IID.
     c) cred_key: str (default: "gitlab").
   - How to call: GitLabTool.merge_mr(project_id=123, iid=67)

9. list_pipelines:
   - Purpose: Lists recent pipelines (CI/CD runs) for a project (limited to latest 20).
   - Arguments:
     a) project_id: int
     b) cred_key: str (default: "gitlab").
   - Returns: List of pipelines with id, status, and ref.
   - How to call: GitLabTool.list_pipelines(project_id=123)

10. trigger_pipeline:
    - Purpose: Manually triggers a new pipeline on a specific branch or tag.
    - Arguments:
      a) project_id: int
      b) ref: str (default: "main") - Branch, tag, or commit SHA.
      c) cred_key: str (default: "gitlab").
    - How to call: GitLabTool.trigger_pipeline(project_id=123, ref="main")

11. get_pipeline_jobs:
    - Purpose: Retrieves all jobs for a specific pipeline.
    - Arguments:
      a) project_id: int
      b) pipeline_id: int
      c) cred_key: str (default: "gitlab").
    - Returns: List of jobs with id, name, status, stage.
    - How to call: GitLabTool.get_pipeline_jobs(project_id=123, pipeline_id=456)

12. retry_job:
    - Purpose: Retries a failed or canceled CI/CD job.
    - Arguments:
      a) project_id: int
      b) job_id: int
      c) cred_key: str (default: "gitlab").
    - How to call: GitLabTool.retry_job(project_id=123, job_id=789)

13. push_file:
    - Purpose: Creates a new file or updates an existing file in the repository using base64 encoding.
    - Arguments:
      a) project_id: int
      b) file_path: str - Full path to the file in the repo (e.g., "src/main.py").
      c) content: str - Plain text content of the file.
      d) message: str (default: "Update via NPM Agent") - Commit message.
      e) branch: str (default: "main") - Target branch.
      f) cred_key: str (default: "gitlab").
    - How to call: GitLabTool.push_file(project_id=123, file_path="README.md", content="# My Project", message="Update readme", branch="main")

14. list_branches:
    - Purpose: Lists all branches in the project.
    - Arguments:
      a) project_id: int
      b) cred_key: str (default: "gitlab").
    - Returns: List of branch names.
    - How to call: GitLabTool.list_branches(project_id=123)

15. create_branch:
    - Purpose: Creates a new branch from an existing reference (branch, tag, or commit).
    - Arguments:
      a) project_id: int
      b) name: str - Name of the new branch.
      c) ref: str (default: "main") - Source reference.
      d) cred_key: str (default: "gitlab").
    - How to call: GitLabTool.create_branch(project_id=123, name="feature-new-ui", ref="main")

16. list_members:
    - Purpose: Lists all members of a project with their access levels.
    - Arguments:
      a) project_id: int
      b) cred_key: str (default: "gitlab").
    - Returns: List of members with id, username, access_level.
    - How to call: GitLabTool.list_members(project_id=123)

17. add_member:
    - Purpose: Adds a user as a member to the project with a specific access level.
    - Arguments:
      a) project_id: int
      b) user_id: int - GitLab user ID (numeric).
      c) access_level: int (default: 30) - 10=Guest, 20=Reporter, 30=Developer, 40=Maintainer, 50=Owner.
      d) cred_key: str (default: "gitlab").
    - How to call: GitLabTool.add_member(project_id=123, user_id=456, access_level=30)
""")
   

    @staticmethod
    def _gl(cred_key: str = "gitlab"):
        import gitlab
        c = CredStore.load(cred_key)
        url = c.get("url", "https://gitlab.com")
        token = c.get("token", "")
        if not token:
            raise ValueError("No GitLab token. Save via CredStore.save('gitlab', {'token':'...','url':'...'}).")
        gl = gitlab.Gitlab(url, private_token=token)
        gl.auth()
        return gl

    @staticmethod
    def create_project(name: str, visibility: str = "private",
                       cred_key: str = "gitlab") -> ToolResult:
        try:
            gl = GitLabTool._gl(cred_key)
            p = gl.projects.create({"name": name, "visibility": visibility})
            return ToolResult(True, f"✓ Project '{name}' created: {p.web_url}", {"id": p.id, "url": p.web_url})
        except Exception as e:
            return ToolResult(False, f"✗ create_project failed: {e}")

    @staticmethod
    def list_projects(cred_key: str = "gitlab") -> ToolResult:
        try:
            gl = GitLabTool._gl(cred_key)
            projects = gl.projects.list(owned=True)
            data = [{"id": p.id, "name": p.name, "url": p.web_url} for p in projects]
            return ToolResult(True, f"✓ {len(data)} projects", data)
        except Exception as e:
            return ToolResult(False, f"✗ list_projects failed: {e}")

    @staticmethod
    def get_project(id: int, cred_key: str = "gitlab") -> ToolResult:
        try:
            gl = GitLabTool._gl(cred_key)
            p = gl.projects.get(id)
            data = {"id": p.id, "name": p.name, "description": p.description,
                    "url": p.web_url, "default_branch": p.default_branch}
            return ToolResult(True, f"✓ Project {id}", data)
        except Exception as e:
            return ToolResult(False, f"✗ get_project failed: {e}")

    @staticmethod
    def create_issue(project_id: int, title: str, description: str = "",
                     labels: list = None, cred_key: str = "gitlab") -> ToolResult:
        try:
            gl = GitLabTool._gl(cred_key)
            p = gl.projects.get(project_id)
            issue = p.issues.create({"title": title, "description": description,
                                     "labels": labels or []})
            return ToolResult(True, f"✓ Issue #{issue.iid} created: {issue.web_url}", {"iid": issue.iid})
        except Exception as e:
            return ToolResult(False, f"✗ GitLab create_issue failed: {e}")

    @staticmethod
    def close_issue(project_id: int, iid: int, cred_key: str = "gitlab") -> ToolResult:
        try:
            gl = GitLabTool._gl(cred_key)
            p = gl.projects.get(project_id)
            issue = p.issues.get(iid)
            issue.state_event = "close"
            issue.save()
            return ToolResult(True, f"✓ Issue #{iid} closed")
        except Exception as e:
            return ToolResult(False, f"✗ close_issue failed: {e}")

    @staticmethod
    def create_mr(project_id: int, title: str, source: str, target: str,
                  description: str = "", cred_key: str = "gitlab") -> ToolResult:
        try:
            gl = GitLabTool._gl(cred_key)
            p = gl.projects.get(project_id)
            mr = p.mergerequests.create({"title": title, "source_branch": source,
                                         "target_branch": target, "description": description})
            return ToolResult(True, f"✓ MR #{mr.iid}: {mr.web_url}", {"iid": mr.iid, "url": mr.web_url})
        except Exception as e:
            return ToolResult(False, f"✗ create_mr failed: {e}")

    @staticmethod
    def merge_mr(project_id: int, iid: int, cred_key: str = "gitlab") -> ToolResult:
        try:
            gl = GitLabTool._gl(cred_key)
            mr = gl.projects.get(project_id).mergerequests.get(iid)
            mr.merge()
            return ToolResult(True, f"✓ MR #{iid} merged")
        except Exception as e:
            return ToolResult(False, f"✗ merge_mr failed: {e}")

    @staticmethod
    def list_pipelines(project_id: int, cred_key: str = "gitlab") -> ToolResult:
        try:
            gl = GitLabTool._gl(cred_key)
            pipelines = gl.projects.get(project_id).pipelines.list()
            data = [{"id": p.id, "status": p.status, "ref": p.ref} for p in pipelines[:20]]
            return ToolResult(True, f"✓ {len(data)} pipelines", data)
        except Exception as e:
            return ToolResult(False, f"✗ list_pipelines failed: {e}")

    @staticmethod
    def trigger_pipeline(project_id: int, ref: str = "main",
                         cred_key: str = "gitlab") -> ToolResult:
        try:
            gl = GitLabTool._gl(cred_key)
            pipeline = gl.projects.get(project_id).pipelines.create({"ref": ref})
            return ToolResult(True, f"✓ Pipeline #{pipeline.id} triggered on '{ref}'", {"id": pipeline.id})
        except Exception as e:
            return ToolResult(False, f"✗ trigger_pipeline failed: {e}")

    @staticmethod
    def get_pipeline_jobs(project_id: int, pipeline_id: int,
                          cred_key: str = "gitlab") -> ToolResult:
        try:
            gl = GitLabTool._gl(cred_key)
            pipeline = gl.projects.get(project_id).pipelines.get(pipeline_id)
            jobs = pipeline.jobs.list()
            data = [{"id": j.id, "name": j.name, "status": j.status, "stage": j.stage} for j in jobs]
            return ToolResult(True, f"✓ {len(data)} jobs in pipeline #{pipeline_id}", data)
        except Exception as e:
            return ToolResult(False, f"✗ get_pipeline_jobs failed: {e}")

    @staticmethod
    def retry_job(project_id: int, job_id: int, cred_key: str = "gitlab") -> ToolResult:
        try:
            gl = GitLabTool._gl(cred_key)
            job = gl.projects.get(project_id).jobs.get(job_id)
            job.retry()
            return ToolResult(True, f"✓ Job #{job_id} retried")
        except Exception as e:
            return ToolResult(False, f"✗ retry_job failed: {e}")

    @staticmethod
    def push_file(project_id: int, file_path: str, content: str,
                  message: str = "Update via NPM Agent", branch: str = "main",
                  cred_key: str = "gitlab") -> ToolResult:
        try:
            import base64
            gl = GitLabTool._gl(cred_key)
            p = gl.projects.get(project_id)
            encoded = base64.b64encode(content.encode()).decode()
            try:
                f = p.files.get(file_path=file_path, ref=branch)
                p.files.update(file_path=file_path, branch=branch,
                               content=encoded, commit_message=message, encoding="base64")
                return ToolResult(True, f"✓ Updated '{file_path}' on '{branch}'")
            except Exception:
                p.files.create({"file_path": file_path, "branch": branch,
                                "content": encoded, "commit_message": message, "encoding": "base64"})
                return ToolResult(True, f"✓ Created '{file_path}' on '{branch}'")
        except Exception as e:
            return ToolResult(False, f"✗ push_file failed: {e}")

    @staticmethod
    def list_branches(project_id: int, cred_key: str = "gitlab") -> ToolResult:
        try:
            gl = GitLabTool._gl(cred_key)
            branches = [b.name for b in gl.projects.get(project_id).branches.list()]
            return ToolResult(True, f"✓ {len(branches)} branches", branches)
        except Exception as e:
            return ToolResult(False, f"✗ list_branches failed: {e}")

    @staticmethod
    def create_branch(project_id: int, name: str, ref: str = "main",
                      cred_key: str = "gitlab") -> ToolResult:
        try:
            gl = GitLabTool._gl(cred_key)
            b = gl.projects.get(project_id).branches.create({"branch": name, "ref": ref})
            return ToolResult(True, f"✓ Branch '{name}' created from '{ref}'")
        except Exception as e:
            return ToolResult(False, f"✗ create_branch failed: {e}")

    @staticmethod
    def list_members(project_id: int, cred_key: str = "gitlab") -> ToolResult:
        try:
            gl = GitLabTool._gl(cred_key)
            members = gl.projects.get(project_id).members.list()
            data = [{"id": m.id, "username": m.username, "access_level": m.access_level} for m in members]
            return ToolResult(True, f"✓ {len(data)} members", data)
        except Exception as e:
            return ToolResult(False, f"✗ list_members failed: {e}")

    @staticmethod
    def add_member(project_id: int, user_id: int, access_level: int = 30,
                   cred_key: str = "gitlab") -> ToolResult:
        try:
            gl = GitLabTool._gl(cred_key)
            gl.projects.get(project_id).members.create({"user_id": user_id, "access_level": access_level})
            return ToolResult(True, f"✓ User {user_id} added with access level {access_level}")
        except Exception as e:
            return ToolResult(False, f"✗ add_member failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# 4. DockerTool
# ══════════════════════════════════════════════════════════════════════════════
class DockerTool:
    name = "docker"
    description = (
        "Full Docker operations: build, push, pull, run, exec, logs, "
        "networks, volumes, docker-compose, system prune"
    )
    use = (
            """
Name of Tool:- DockerTool

Purpose of Tool:-
The DockerTool provides a comprehensive programmatic interface to perform full Docker operations.
It supports image management (build, push, pull, tag, remove, list), container life-cycle management (run, start, stop, remove, exec, logs, list, inspect), network management (create, list, remove), volume management (create, list, remove), multi-container orchestration via docker-compose (up, down, logs, ps), authentication handling, and system cleanups (prune).
All operations are executed either using the official Docker SDK for Python or via fallback CLI shell executions for complex commands like compose and system pruning.

Methods:-

* _client: Internal helper to initialize the Docker SDK client from the host environment.
* _run_docker: Internal helper to execute fallback Docker CLI commands using subprocesses.
* build_image: Builds a Docker image from a local development context or Dockerfile.
* push_image: Pushes a local image to DockerHub or a specified private container registry.
* pull_image: Pulls a target image from a remote registry.
* tag_image: Tags an existing local source image with a new target repository and tag.
* remove_image: Deletes an image from the local Docker host memory.
* list_images: Retrieves and returns all available local Docker images with metadata.
* run_container: Creates, configures, and provisions a new running container instance.
* stop_container: Gracefully stops a currently running Docker container.
* start_container: Boots up an existing stopped Docker container.
* remove_container: Deletes an existing container from the system storage.
* exec_in_container: Executes an arbitrary shell command live inside a running container context.
* get_logs: Retrieves stdout/stderr execution log snapshots from a targeted container.
* list_containers: Queries and aggregates current running or inactive container processes.
* inspect_container: Fetches full structured, low-level configuration details of a container.
* create_network: Provisions a new isolated Docker virtual network with custom drivers.
* list_networks: Summarizes all existing operational networks on the host machine.
* remove_network: Deletes an unused custom Docker network stack.
* create_volume: Sets up a persistent directory storage volume managed by Docker daemon.
* list_volumes: Lists details of all active Docker-managed persistent volumes.
* remove_volume: Permanently destroys a Docker volume entry.
* compose_up: Instructs Docker Compose to parse structural files and spin up multi-container applications.
* compose_down: Powers down and tears down a multi-container network configuration created by Compose.
* compose_logs: Aggregates historical logs across all or explicit components inside a Docker Compose setup.
* compose_ps: Displays runtime statuses and details of container clusters managed by Compose.
* login: Performs a session authentication handshake against DockerHub or private remote registries.
* system_prune: Reclaims system memory by clearing stopped containers, networks, and unused imagery.

How to use Tool Methods:-

1. _client:
* Purpose: Internal factory method initializing and returning a docker client configured from environment variables.
* Arguments: None.
* Note: Used strictly as an internal backend connector helper.
* How to call: DockerTool._client()


2. _run_docker:
* Purpose: Internal helper method executing external Docker subcommands via system shells.
* Arguments:
a) args: list - Sequential parameters following the base 'docker' command binary structure.
* Returns: A tuple container containing exit code representation (int) alongside standard out/err streams (str).
* How to call: DockerTool._run_docker(["version"])


3. build_image:
* Purpose: Generates operational docker images from file context definitions.
* Arguments:
a) path: str - Target directory directory containing code context workspace.
b) tag: str - The identifying label string repository string target.
c) dockerfile: str (default: "Dockerfile") - Alternative Dockerfile identifier mapping path filename.
d) build_args: dict (default: None) - Variable mapping definitions to pass build time flags.
* Returns: ToolResult holding configuration flag status, validation message, and dictionary configuration holding image identity hashes.
* How to call: DockerTool.build_image(path="./app", tag="myapp:v1", dockerfile="prod.Dockerfile", build_args={"ENV": "production"})


4. push_image:
* Purpose: Publishes local images upwards to external storage centers.
* Arguments:
a) image: str - The source target string image mapping.
b) registry: str (default: "") - Alternative hostname target identifier tracking private hosting endpoints.
c) cred_key: str (default: "docker") - Internal identity credential flag key mapping reference.
* Returns: ToolResult highlighting success, target push summary metadata logs, and verification fields.
* How to call: DockerTool.push_image(image="myapp:v1", registry="myregistry.azurecr.io")


5. pull_image:
* Purpose: Downloads external source images from public/private container stores.
* Arguments:
a) image: str - Full path destination pattern to fetch down from registries.
* Returns: ToolResult indicating operation completion metadata and dictionary containing image registry IDs.
* How to call: DockerTool.pull_image(image="ubuntu:latest")


6. tag_image:
* Purpose: Rewrites mapping structures or assigns new tag definitions onto existing images.
* Arguments:
a) source: str - Initial tracking locator name.
b) target: str - Expected full string repository and explicit version structure output definition.
* Returns: ToolResult capturing operations confirmation.
* How to call: DockerTool.tag_image(source="myapp:v1", target="myuser/myapp:latest")


7. remove_image:
* Purpose: Deletes cached image references from host environments.
* Arguments:
a) image: str - Identity string or locator reference name.
b) force: bool (default: False) - Flag dictating whether to drop layers active on stopped items.
* Returns: ToolResult with tracking notification confirmation updates.
* How to call: DockerTool.remove_image(image="myapp:v1", force=True)


8. list_images:
* Purpose: Collects current stored local filesystem imagery layers.
* Arguments:
a) filter: str (default: None) - Repository pattern parameter tracking reference strings.
* Returns: ToolResult displaying total item counts, alongside nested object dictionary arrays detailing id, tag references, and sizes in megabytes.
* How to call: DockerTool.list_images(filter="nginx")


9. run_container:
* Purpose: Spins up brand new containers running execution profiles from standard image patterns.
* Arguments:
a) image: str - Base target template component.
b) name: str (default: None) - String target to name the target runtime execution layer.
b) ports: dict (default: None) - Mappings configuring inside/outside port interfaces (e.g., {"80/tcp": 8080}).
c) volumes: dict (default: None) - Host filesystem or persistent volume mounting directories.
d) env: dict (default: None) - Environment string configurations inject runtime logic.
e) detach: bool (default: True) - Determines whether process flows run background tasks.
f) command: str (default: None) - Override initialization sequence arguments.
* Returns: ToolResult with success confirmation mapping output variables along short container identifiers.
* How to call: DockerTool.run_container(image="redis:alpine", name="my-redis", ports={"6379/tcp": 6379})


10. stop_container:
* Purpose: Stops running instances safely using signal cycles.
* Arguments:
a) name: str - Target runtime application identifier.
* Returns: ToolResult showing target system modification metrics.
* How to call: DockerTool.stop_container(name="my-redis")


11. start_container:
* Purpose: Starts or resumes previously paused/stopped structures.
* Arguments:
a) name: str - Target specific workspace label.
* Returns: ToolResult output tracking details.
* How to call: DockerTool.start_container(name="my-redis")


12. remove_container:
* Purpose: Deletes container definition maps out of system engine stores.
* Arguments:
a) name: str - Target entity reference tracking tag.
b) force: bool (default: False) - Erases target container processes even while active.
* Returns: ToolResult verification strings.
* How to call: DockerTool.remove_container(name="my-redis", force=True)


13. exec_in_container:
* Purpose: Triggers commands live into operational running container terminals.
* Arguments:
a) name: str - Running system target container component.
b) command: str - Executable target commands (e.g., "ls -la").
* Returns: ToolResult capturing binary text transformations or system runtime responses.
* How to call: DockerTool.exec_in_container(name="web-app", command="python manage.py migrate")


14. get_logs:
* Purpose: Aggregates system stream data generated by runtime assets.
* Arguments:
a) name: str - Core container tracking reference string.
b) tail: int (default: 100) - Number limit tracking log response lengths.
c) follow: bool (default: False) - Flag requesting stream locks on execution paths.
* Returns: ToolResult holding complete textual trace outputs.
* How to call: DockerTool.get_logs(name="web-app", tail=50)


15. list_containers:
* Purpose: Audits host space to view running or stopped system containers.
* Arguments:
a) all: bool (default: False) - Pulls both actively working and dormant items.
b) filter: str (default: None) - Target name substring filter match configuration flags.
* Returns: ToolResult aggregating structural object information (id, name, status, image details).
* How to call: DockerTool.list_containers(all=True, filter="web")


16. inspect_container:
* Purpose: Exposes fully detailed configuration JSON schemas regarding active operational assets.
* Arguments:
a) name: str - Unique target name tracking string variable identifiers.
* Returns: ToolResult embedding raw container schema attribute metadata.
* How to call: DockerTool.inspect_container(name="web-app")


17. create_network:
* Purpose: Configures customized virtual networks allowing interconnected container mappings.
* Arguments:
a) name: str - Designated networking identifier name.
b) driver: str (default: "bridge") - Underlying virtual driver architecture (e.g., "bridge", "overlay").
* Returns: ToolResult mapping data confirmations along string network tracking id keys.
* How to call: DockerTool.create_network(name="app-tier", driver="bridge")


18. list_networks:
* Purpose: Summarizes host system network configurations.
* Arguments: None.
* Returns: ToolResult showcasing mapping dictionaries exposing id, name, and driver specifics.
* How to call: DockerTool.list_networks()


19. remove_network:
* Purpose: Dismantles a network configuration layer from memory spaces.
* Arguments:
a) name: str - Specific name representing the network space.
* Returns: ToolResult stating structural results.
* How to call: DockerTool.remove_network(name="app-tier")


20. create_volume:
* Purpose: Provisions managed space on storage blocks for data persistence layer interactions.
* Arguments:
a) name: str - Target filesystem volume layout system name.
* Returns: ToolResult declaring operational status along mapping details.
* How to call: DockerTool.create_volume(name="db-data")


21. list_volumes:
* Purpose: Displays local volume maps initialized through engine components.
* Arguments: None.
* Returns: ToolResult embedding arrays detailing object maps containing name and driver structures.
* How to call: DockerTool.list_volumes()


22. remove_volume:
* Purpose: Completely discards persistent volume objects from file trees.
* Arguments:
a) name: str - Targeted volume component signature.
* Returns: ToolResult showing termination validation strings.
* How to call: DockerTool.remove_volume(name="db-data")


23. compose_up:
* Purpose: Evaluates single compose files to establish, provision, and group interconnected containers.
* Arguments:
a) path: str - Workspace path addressing the `docker-compose.yml` structure directly.
b) detach: bool (default: True) - Leaves target processes active within baseline system background tasks.
c) services: list (default: None) - Optional item array filtering explicit targeted services to spin up.
* Returns: ToolResult recording exit codes tracking CLI system process operations.
* How to call: DockerTool.compose_up(path="./docker-compose.yml", services=["web", "db"])


24. compose_down:
* Purpose: Safely drops multi-container setups provisioning system cleanups.
* Arguments:
a) path: str - Complete configuration directory route pointing to the docker-compose source target.
b) volumes: bool (default: False) - Declares whether associated data storage structures should be dropped instantly.
* Returns: ToolResult verifying shell return tracking output definitions.
* How to call: DockerTool.compose_down(path="./docker-compose.yml", volumes=True)


25. compose_logs:
* Purpose: Gathers consolidated textual logs generated through cluster architectures mapped in Compose.
* Arguments:
a) path: str - Storage direction address guiding engine towards tracking configurations.
b) services: list (default: None) - Target explicit string collection tags filtering targeted tracking outputs.
c) tail: int (default: 50) - Total baseline record lines returned back per process component.
* Returns: ToolResult encapsulating aggregated multi-container application console logs.
* How to call: DockerTool.compose_logs(path="./docker-compose.yml", services=["web"])


26. compose_ps:
* Purpose: Queries cluster composition matrix mappings to trace process loops.
* Arguments:
a) path: str - Location mapping to target configuration components.
* Returns: ToolResult indicating health matrix mapping text reports.
* How to call: DockerTool.compose_ps(path="./docker-compose.yml")


27. login:
* Purpose: Passes user authentication identities onto active network container registry hosts.
* Arguments:
a) registry: str - Destination target string mapping hosting platforms (e.g., registry.hub.docker.com).
b) username: str - Account login string credential identifier.
c) password: str - Private token secret phrase validation mapping.
* Returns: ToolResult mapping tracking authentication responses.
* How to call: DockerTool.login(registry="myregistry.azurecr.io", username="admin", password="password123")


28. system_prune:
* Purpose: Reclaims system volumes by purging cached objects, stopped layers, or dead system containers.
* Arguments:
a) all: bool (default: False) - Flag dictating whether unused images are scrubbed globally.
b) volumes: bool (default: False) - Controls deletion logic regarding detached data volume spaces.
* Returns: ToolResult indicating total space recovery metrics and CLI output traces.
* How to call: DockerTool.system_prune(all=True, volumes=True)
""")

    @staticmethod
    def _client():
        import docker
        return docker.from_env()

    @staticmethod
    def _run_docker(args: list) -> tuple:
        r = subprocess.run(["docker"] + args, capture_output=True, text=True)
        return r.returncode, (r.stdout + r.stderr).strip()

    @staticmethod
    def build_image(path: str, tag: str, dockerfile: str = "Dockerfile",
                    build_args: dict = None) -> ToolResult:
        try:
            client = DockerTool._client()
            ba = build_args or {}
            image, logs = client.images.build(path=path, tag=tag, dockerfile=dockerfile, buildargs=ba, rm=True)
            log_text = "\n".join(l.get("stream", "") for l in logs if "stream" in l).strip()
            return ToolResult(True, f"✓ Image '{tag}' built\n{log_text[-500:]}", {"id": image.id})
        except Exception as e:
            return ToolResult(False, f"✗ build_image failed: {e}")

    @staticmethod
    def push_image(image: str, registry: str = "", cred_key: str = "docker") -> ToolResult:
        try:
            client = DockerTool._client()
            full_tag = f"{registry}/{image}" if registry else image
            result = client.images.push(full_tag)
            return ToolResult(True, f"✓ Pushed '{full_tag}'", result)
        except Exception as e:
            return ToolResult(False, f"✗ push_image failed: {e}")

    @staticmethod
    def pull_image(image: str) -> ToolResult:
        try:
            client = DockerTool._client()
            img = client.images.pull(image)
            return ToolResult(True, f"✓ Pulled '{image}'", {"id": img.id})
        except Exception as e:
            return ToolResult(False, f"✗ pull_image failed: {e}")

    @staticmethod
    def tag_image(source: str, target: str) -> ToolResult:
        try:
            client = DockerTool._client()
            img = client.images.get(source)
            repo, _, tag = target.rpartition(":")
            img.tag(repo or target, tag=tag or "latest")
            return ToolResult(True, f"✓ Tagged '{source}' → '{target}'")
        except Exception as e:
            return ToolResult(False, f"✗ tag_image failed: {e}")

    @staticmethod
    def remove_image(image: str, force: bool = False) -> ToolResult:
        try:
            client = DockerTool._client()
            client.images.remove(image, force=force)
            return ToolResult(True, f"✓ Image '{image}' removed")
        except Exception as e:
            return ToolResult(False, f"✗ remove_image failed: {e}")

    @staticmethod
    def list_images(filter: str = None) -> ToolResult:
        try:
            client = DockerTool._client()
            images = client.images.list(filters={"reference": filter} if filter else {})
            data = [{"id": i.short_id, "tags": i.tags, "size_mb": round(i.attrs["Size"] / 1e6, 1)} for i in images]
            return ToolResult(True, f"✓ {len(data)} images", data)
        except Exception as e:
            return ToolResult(False, f"✗ list_images failed: {e}")

    @staticmethod
    def run_container(image: str, name: str = None, ports: dict = None,
                      volumes: dict = None, env: dict = None,
                      detach: bool = True, command: str = None) -> ToolResult:
        try:
            client = DockerTool._client()
            kwargs = {
                "image": image, "detach": detach,
                "ports": ports or {}, "volumes": volumes or {},
                "environment": env or {},
            }
            if name:
                kwargs["name"] = name
            if command:
                kwargs["command"] = command
            container = client.containers.run(**kwargs)
            cid = container.id[:12] if detach else "completed"
            return ToolResult(True, f"✓ Container started: {cid}", {"id": cid})
        except Exception as e:
            return ToolResult(False, f"✗ run_container failed: {e}")

    @staticmethod
    def stop_container(name: str) -> ToolResult:
        try:
            DockerTool._client().containers.get(name).stop()
            return ToolResult(True, f"✓ Container '{name}' stopped")
        except Exception as e:
            return ToolResult(False, f"✗ stop_container failed: {e}")

    @staticmethod
    def start_container(name: str) -> ToolResult:
        try:
            DockerTool._client().containers.get(name).start()
            return ToolResult(True, f"✓ Container '{name}' started")
        except Exception as e:
            return ToolResult(False, f"✗ start_container failed: {e}")

    @staticmethod
    def remove_container(name: str, force: bool = False) -> ToolResult:
        try:
            DockerTool._client().containers.get(name).remove(force=force)
            return ToolResult(True, f"✓ Container '{name}' removed")
        except Exception as e:
            return ToolResult(False, f"✗ remove_container failed: {e}")

    @staticmethod
    def exec_in_container(name: str, command: str) -> ToolResult:
        try:
            container = DockerTool._client().containers.get(name)
            exit_code, output = container.exec_run(command, demux=False)
            out = output.decode(errors="replace") if isinstance(output, bytes) else str(output)
            return ToolResult(exit_code == 0, out.strip() or "✓ Done", out)
        except Exception as e:
            return ToolResult(False, f"✗ exec_in_container failed: {e}")

    @staticmethod
    def get_logs(name: str, tail: int = 100, follow: bool = False) -> ToolResult:
        try:
            container = DockerTool._client().containers.get(name)
            logs = container.logs(tail=tail, follow=follow, timestamps=True)
            out = logs.decode(errors="replace") if isinstance(logs, bytes) else str(logs)
            return ToolResult(True, f"✓ Logs from '{name}'", out)
        except Exception as e:
            return ToolResult(False, f"✗ get_logs failed: {e}")

    @staticmethod
    def list_containers(all: bool = False, filter: str = None) -> ToolResult:
        try:
            client = DockerTool._client()
            kwargs = {"all": all}
            if filter:
                kwargs["filters"] = {"name": filter}
            containers = client.containers.list(**kwargs)
            data = [{"id": c.short_id, "name": c.name, "status": c.status, "image": c.image.tags} for c in containers]
            return ToolResult(True, f"✓ {len(data)} containers", data)
        except Exception as e:
            return ToolResult(False, f"✗ list_containers failed: {e}")

    @staticmethod
    def inspect_container(name: str) -> ToolResult:
        try:
            container = DockerTool._client().containers.get(name)
            return ToolResult(True, f"✓ Inspected '{name}'", container.attrs)
        except Exception as e:
            return ToolResult(False, f"✗ inspect_container failed: {e}")

    @staticmethod
    def create_network(name: str, driver: str = "bridge") -> ToolResult:
        try:
            net = DockerTool._client().networks.create(name, driver=driver)
            return ToolResult(True, f"✓ Network '{name}' created (driver: {driver})", {"id": net.id})
        except Exception as e:
            return ToolResult(False, f"✗ create_network failed: {e}")

    @staticmethod
    def list_networks() -> ToolResult:
        try:
            nets = DockerTool._client().networks.list()
            data = [{"id": n.short_id, "name": n.name, "driver": n.attrs["Driver"]} for n in nets]
            return ToolResult(True, f"✓ {len(data)} networks", data)
        except Exception as e:
            return ToolResult(False, f"✗ list_networks failed: {e}")

    @staticmethod
    def remove_network(name: str) -> ToolResult:
        try:
            DockerTool._client().networks.get(name).remove()
            return ToolResult(True, f"✓ Network '{name}' removed")
        except Exception as e:
            return ToolResult(False, f"✗ remove_network failed: {e}")

    @staticmethod
    def create_volume(name: str) -> ToolResult:
        try:
            v = DockerTool._client().volumes.create(name)
            return ToolResult(True, f"✓ Volume '{name}' created", {"name": v.name})
        except Exception as e:
            return ToolResult(False, f"✗ create_volume failed: {e}")

    @staticmethod
    def list_volumes() -> ToolResult:
        try:
            vols = DockerTool._client().volumes.list()
            data = [{"name": v.name, "driver": v.attrs["Driver"]} for v in vols]
            return ToolResult(True, f"✓ {len(data)} volumes", data)
        except Exception as e:
            return ToolResult(False, f"✗ list_volumes failed: {e}")

    @staticmethod
    def remove_volume(name: str) -> ToolResult:
        try:
            DockerTool._client().volumes.get(name).remove()
            return ToolResult(True, f"✓ Volume '{name}' removed")
        except Exception as e:
            return ToolResult(False, f"✗ remove_volume failed: {e}")

    @staticmethod
    def compose_up(path: str, detach: bool = True, services: list = None) -> ToolResult:
        try:
            args = ["compose", "-f", path, "up"]
            if detach:
                args.append("-d")
            if services:
                args += services
            rc, out = DockerTool._run_docker(args)
            return ToolResult(rc == 0, f"✓ Compose up\n{out}" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ compose_up failed: {e}")

    @staticmethod
    def compose_down(path: str, volumes: bool = False) -> ToolResult:
        try:
            args = ["compose", "-f", path, "down"]
            if volumes:
                args.append("-v")
            rc, out = DockerTool._run_docker(args)
            return ToolResult(rc == 0, f"✓ Compose down\n{out}" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ compose_down failed: {e}")

    @staticmethod
    def compose_logs(path: str, services: list = None, tail: int = 50) -> ToolResult:
        try:
            args = ["compose", "-f", path, "logs", f"--tail={tail}"] + (services or [])
            rc, out = DockerTool._run_docker(args)
            return ToolResult(rc == 0, out, out)
        except Exception as e:
            return ToolResult(False, f"✗ compose_logs failed: {e}")

    @staticmethod
    def compose_ps(path: str) -> ToolResult:
        try:
            rc, out = DockerTool._run_docker(["compose", "-f", path, "ps"])
            return ToolResult(rc == 0, out, out)
        except Exception as e:
            return ToolResult(False, f"✗ compose_ps failed: {e}")

    @staticmethod
    def login(registry: str, username: str, password: str) -> ToolResult:
        try:
            client = DockerTool._client()
            result = client.login(username=username, password=password, registry=registry)
            return ToolResult(True, f"✓ Logged into {registry or 'DockerHub'}", result)
        except Exception as e:
            return ToolResult(False, f"✗ docker login failed: {e}")

    @staticmethod
    def system_prune(all: bool = False, volumes: bool = False) -> ToolResult:
        try:
            args = ["system", "prune", "-f"]
            if all:
                args.append("-a")
            if volumes:
                args.append("--volumes")
            rc, out = DockerTool._run_docker(args)
            return ToolResult(rc == 0, f"✓ System pruned\n{out}" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ system_prune failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# 5. PackageManagerTool
# ══════════════════════════════════════════════════════════════════════════════
class PackageManagerTool:
    name = "package_manager"
    description = (
        "pip, npm, yarn, pnpm, cargo, go modules — install, uninstall, "
        "list, update, audit, build, publish"
    )
    use = (
            """
Name of Tool:- PackageManagerTool

Purpose of Tool:-
The PackageManagerTool acts as a unified programmatic controller to manage dependency lifecycles across multiple language ecosystems, including Python (pip), JavaScript/TypeScript (npm, yarn), Rust (cargo), and Go (go modules).
It provides standardized execution routes to handle installations, removals, dependency tree inspections, version lock auditing, test executions, binary packaging, and module distribution pipelines.
All operations execute downstream system binaries securely using detached subprocess runners featuring customizable processing environments and runtime timeout safety guardrails.

Methods:-

* _run: Internal utility to dispatch command arrays cleanly into shell environments with configurable tracking timeouts.
* pip_install: Downloads and integrates Python dependencies from PyPI or custom requirements manifests.
* pip_uninstall: Triggers complete cleanup loops to purge explicitly named Python packages.
* pip_list: Outputs a structured representation tracking every active Python environment dependency layer.
* pip_show: Pulls granular metadata, diagnostic properties, and licensing paths related to single target packages.
* pip_freeze: Generates production-ready dependencies listings outputting requirements string records.
* npm_install: Provisions single or complex package matrices inside project roots or global system caches.
* npm_uninstall: Discards Node modules tracking dependencies fields inside project manifests.
* npm_run: Triggers pre-configured lifecycle automation scripts stored inside `package.json` registries.
* npm_build: Runs generation build sequences to prepare production assets.
* npm_publish: Pushes compiled artifacts directly out to external Node package registries.
* npm_list: Visualizes project nested dependency structures via parsed object definitions.
* npm_update: Evaluates semantic constraints to step localized package version rules forward.
* npm_audit: Runs security vulnerability checks across dependencies trees to find risk vectors.
* yarn_install: Triggers dependency resolutions relying on localized lock file validation profiles.
* yarn_add: Modifies lock schemas to introduce targeted node modules inside Javascript environments.
* yarn_remove: Excises target node modules cleanly along tracking reference paths.
* cargo_build: Validates package source manifests to compile optimized binary layers via Rust compilers.
* cargo_test: Orchestrates asynchronous testing harnesses to evaluate multi-tiered integration suites.
* cargo_run: Executes compiled Rust workspace binaries passing extra structural argument controls.
* go_build: Groups source files to construct native executable packages across specified paths.
* go_test: Scans module components to evaluate verification code blocks inside Go projects.
* go_get: Modifies module graphs to pull, cache, and hook remote Go software dependencies.

How to use Tool Methods:-

1. _run:
* Purpose: Internal factory method managing target shell executions.
* Arguments:
a) args: list - Complete target programmatic execution positional breakdown array.
b) cwd: str (default: None) - Working directory directory target context placement path.
c) timeout: int (default: 180) - Processing lifespan seconds before triggering a kill loop.
* Returns: Tuple containing process execution integer status code and raw unified console stream data.
* How to call: PackageManagerTool._run(["pip", "--version"])


2. pip_install:
* Purpose: Directs Python environment dependency installation tracking.
* Arguments:
a) packages: list (default: None) - Array collecting targeted package identifiers.
b) upgrade: bool (default: False) - Demands dependency version updates to the newest releases.
c) user: bool (default: False) - Restricts installations to target isolated user directories.
d) requirements_file: str (default: None) - Relies on file path pointers to run manifest installations.
* Returns: ToolResult storing deployment success flags and trimmed runtime console string tracking records.
* How to call: PackageManagerTool.pip_install(requirements_file="requirements.txt", upgrade=True)


3. pip_uninstall:
* Purpose: Eliminates specified packages from local Python runtimes.
* Arguments:
a) packages: list - Collection tracking targeted package descriptors.
* Returns: ToolResult holding runtime state outcomes.
* How to call: PackageManagerTool.pip_uninstall(packages=["requests", "flask"])


4. pip_list:
* Purpose: Inspects environment definitions to identify installed package profiles.
* Arguments:
a) outdated: bool (default: False) - Filters lists to present items with newer versions available on PyPI.
* Returns: ToolResult enclosing deep structured arrays containing metadata mappings.
* How to call: PackageManagerTool.pip_list(outdated=True)


5. pip_show:
* Purpose: Obtains diagnostic breakdowns tracking target python tools.
* Arguments:
a) package: str - Core targeted identifier label name.
* Returns: ToolResult enclosing structural metadata details.
* How to call: PackageManagerTool.pip_show(package="numpy")


6. pip_freeze:
* Purpose: Captures exact version snapshots across active package targets.
* Arguments:
a) output_file: str (default: None) - Target path file destination location mapping name.
* Returns: ToolResult holding structural requirements textual records.
* How to call: PackageManagerTool.pip_freeze(output_file="./requirements.txt")


7. npm_install:
* Purpose: Resolves JavaScript node modules requirements.
* Arguments:
a) path: str (default: ".") - Context path containing targeted configurations.
b) packages: list (default: None) - Targeted software arrays to include.
c) dev: bool (default: False) - Appends structures exclusively into `devDependencies` metadata trees.
d) global_: bool (default: False) - Registers binaries into global machine storage runtimes.
* Returns: ToolResult presenting structural operational logging output strings.
* How to call: PackageManagerTool.npm_install(path="./frontend", packages=["axios"], dev=True)


8. npm_uninstall:
* Purpose: Sweeps JavaScript dependencies out of configuration files.
* Arguments:
a) path: str (default: ".") - Operating filesystem root directory map.
b) packages: list (default: None) - Targeted package arrays to drop.
c) global_: bool (default: False) - Instructs removal tools to clear system-wide binaries.
* Returns: ToolResult monitoring tracking operations.
* How to call: PackageManagerTool.npm_uninstall(path="./frontend", packages=["lodash"])


9. npm_run:
* Purpose: Dispatches custom programmatic script sequences from execution manifests.
* Arguments:
a) path: str - Target local root location.
b) script: str - Mapping key targeting automated script setups (e.g., "start", "lint").
* Returns: ToolResult tracking outcome validations.
* How to call: PackageManagerTool.npm_run(path="./frontend", script="test")


10. npm_build:
* Purpose: Bundles node architectures to render optimized build layouts.
* Arguments:
a) path: str - Root location holding targeted build code contexts.
* Returns: ToolResult displaying status summaries and execution tracking results.
* How to call: PackageManagerTool.npm_build(path="./frontend")


11. npm_publish:
* Purpose: Deploys local components up to registry distribution pipelines.
* Arguments:
a) path: str - Project root workspace destination route.
* Returns: ToolResult tracing registry transaction data logs.
* How to call: PackageManagerTool.npm_publish(path="./my-lib")


12. npm_list:
* Purpose: Maps current dependency arrays into visual trees.
* Arguments:
a) path: str (default: ".") - Target validation root.
b) depth: int (default: 0) - Constraint limit capping visibility tracking levels.
* Returns: ToolResult formatting deep structured nested mapping configuration metrics.
* How to call: PackageManagerTool.npm_list(path=".", depth=1)


13. npm_update:
* Purpose: Synchronizes local package trees with upstream updates based on manifest rules.
* Arguments:
a) path: str (default: ".") - Execution workspace folder location path.
b) packages: list (default: None) - Optional array targeting narrow explicit package selections.
* Returns: ToolResult validation results.
* How to call: PackageManagerTool.npm_update(path="./server", packages=["express"])


14. npm_audit:
* Purpose: Diagnoses project states to check for security vulnerabilities.
* Arguments:
a) path: str (default: ".") - Root location matching target codebases.
b) fix: bool (default: False) - Auto-remediates eligible package vulnerabilities.
* Returns: ToolResult conveying structural scanning summaries.
* How to call: PackageManagerTool.npm_audit(path=".", fix=True)


15. yarn_install:
* Purpose: Evaluates project definitions to settle code spaces utilizing alternative yarn layouts.
* Arguments:
a) path: str (default: ".") - Target working environment destination string.
* Returns: ToolResult updating console logs tracking validation routines.
* How to call: PackageManagerTool.yarn_install(path="./dashboard")


16. yarn_add:
* Purpose: Introduces new package items into Yarn execution graphs.
* Arguments:
a) path: str - Host project path folder directory target.
b) packages: list - Unique module string items targeting integration routines.
c) dev: bool (default: False) - Islocates dependency references inside development blocks.
* Returns: ToolResult tracking execution status outcomes.
* How to call: PackageManagerTool.yarn_add(path="./dashboard", packages=["typescript"], dev=True)


17. yarn_remove:
* Purpose: Purges specified targets from project boundaries using Yarn routines.
* Arguments:
a) path: str - Target workspace directory location.
b) packages: list - Target tracking list details.
* Returns: ToolResult detailing complete removal verification tracking info.
* How to call: PackageManagerTool.yarn_remove(path="./dashboard", packages=["moment"])


18. cargo_build:
* Purpose: Directs Rust compiler toolchains to translate projects into compiled profiles.
* Arguments:
a) path: str - Location holding the target `Cargo.toml` manifest specification.
b) release: bool (default: False) - Activates advanced compiler optimization rules for release binaries.
* Returns: ToolResult outputting compilation logs.
* How to call: PackageManagerTool.cargo_build(path="./rust-service", release=True)


19. cargo_test:
* Purpose: Excutes unit and integration checks built into Rust modules.
* Arguments:
a) path: str - Source tracking workspace destination path directory.
* Returns: ToolResult outputting testing logging blocks and diagnostic outcomes.
* How to call: PackageManagerTool.cargo_test(path="./rust-service")


20. cargo_run:
* Purpose: Compiles and immediately executes Rust binary products in one cycle.
* Arguments:
a) path: str - Path containing target Rust specifications.
b) args_extra: list (default: None) - Command line options injected into the compiled app binary at launch.
* Returns: ToolResult keeping track of terminal console events.
* How to call: PackageManagerTool.cargo_run(path="./rust-service", args_extra=["--port", "8080"])


21. go_build:
* Purpose: Consolidates Go modules to produce system executable files.
* Arguments:
a) path: str - Target directory directory storing source scripts.
b) output: str (default: None) - Custom file destination tracking build name settings.
* Returns: ToolResult verifying standard output parameters.
* How to call: PackageManagerTool.go_build(path="./go-api", output="server.bin")


22. go_test:
* Purpose: Initiates verification structures mapped into Go files.
* Arguments:
a) path: str - Working root path.
b) verbose: bool (default: False) - Activates log verbose reporting formats showcasing all tested sub-components.
* Returns: ToolResult encapsulating text tracking test evaluations.
* How to call: PackageManagerTool.go_test(path="./go-api", verbose=True)


23. go_get:
* Purpose: Downlands and maps remote package references across target Go modules trees.
* Arguments:
a) path: str - Project area workspace destination.
b) package: str - External web resource address mapping dependencies (e.g., "[github.com/gin-gonic/gin](https://github.com/gin-gonic/gin)").
* Returns: ToolResult stating structural state updates.
* How to call: PackageManagerTool.go_get(path="./go-api", package="[github.com/google/uuid](https://github.com/google/uuid)")
""")

    @staticmethod
    def _run(args: list, cwd: str = None, timeout: int = 180) -> tuple:
        r = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout + r.stderr).strip()

    # ── pip ───────────────────────────────────────────────────────────────────
    @staticmethod
    def pip_install(packages: list = None, upgrade: bool = False,
                    user: bool = False, requirements_file: str = None) -> ToolResult:
        try:
            args = [sys.executable, "-m", "pip", "install"]
            if upgrade:
                args.append("--upgrade")
            if user:
                args.append("--user")
            if requirements_file:
                args += ["-r", requirements_file]
            elif packages:
                args += packages
            else:
                return ToolResult(False, "✗ No packages or requirements file specified")
            rc, out = PackageManagerTool._run(args)
            return ToolResult(rc == 0, f"✓ pip install done\n{out[-500:]}" if rc == 0 else f"✗ {out[-500:]}")
        except Exception as e:
            return ToolResult(False, f"✗ pip install failed: {e}")

    @staticmethod
    def pip_uninstall(packages: list) -> ToolResult:
        try:
            args = [sys.executable, "-m", "pip", "uninstall", "-y"] + packages
            rc, out = PackageManagerTool._run(args)
            return ToolResult(rc == 0, f"✓ Uninstalled {packages}" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ pip uninstall failed: {e}")

    @staticmethod
    def pip_list(outdated: bool = False) -> ToolResult:
        try:
            args = [sys.executable, "-m", "pip", "list", "--format=json"]
            if outdated:
                args.append("--outdated")
            rc, out = PackageManagerTool._run(args)
            data = json.loads(out) if rc == 0 else []
            return ToolResult(rc == 0, f"✓ {len(data)} packages", data)
        except Exception as e:
            return ToolResult(False, f"✗ pip list failed: {e}")

    @staticmethod
    def pip_show(package: str) -> ToolResult:
        try:
            rc, out = PackageManagerTool._run([sys.executable, "-m", "pip", "show", package])
            return ToolResult(rc == 0, out, out)
        except Exception as e:
            return ToolResult(False, f"✗ pip show failed: {e}")

    @staticmethod
    def pip_freeze(output_file: str = None) -> ToolResult:
        try:
            rc, out = PackageManagerTool._run([sys.executable, "-m", "pip", "freeze"])
            if output_file and rc == 0:
                Path(output_file).write_text(out)
                return ToolResult(True, f"✓ requirements saved to {output_file}", out)
            return ToolResult(rc == 0, out, out)
        except Exception as e:
            return ToolResult(False, f"✗ pip freeze failed: {e}")

    # ── npm ───────────────────────────────────────────────────────────────────
    @staticmethod
    def npm_install(path: str = ".", packages: list = None,
                    dev: bool = False, global_: bool = False) -> ToolResult:
        try:
            args = ["npm", "install"]
            if global_:
                args.append("-g")
            if packages:
                args += packages
                if dev:
                    args.append("--save-dev")
            rc, out = PackageManagerTool._run(args, cwd=None if global_ else path)
            return ToolResult(rc == 0, f"✓ npm install done\n{out[-400:]}" if rc == 0 else f"✗ {out[-400:]}")
        except Exception as e:
            return ToolResult(False, f"✗ npm install failed: {e}")

    @staticmethod
    def npm_uninstall(path: str = ".", packages: list = None, global_: bool = False) -> ToolResult:
        try:
            args = ["npm", "uninstall"] + (packages or [])
            if global_:
                args.append("-g")
            rc, out = PackageManagerTool._run(args, cwd=None if global_ else path)
            return ToolResult(rc == 0, f"✓ npm uninstall done" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ npm uninstall failed: {e}")

    @staticmethod
    def npm_run(path: str, script: str) -> ToolResult:
        try:
            rc, out = PackageManagerTool._run(["npm", "run", script], cwd=path)
            return ToolResult(rc == 0, out[-1000:] if rc == 0 else f"✗ {out[-500:]}")
        except Exception as e:
            return ToolResult(False, f"✗ npm run failed: {e}")

    @staticmethod
    def npm_build(path: str) -> ToolResult:
        try:
            rc, out = PackageManagerTool._run(["npm", "run", "build"], cwd=path)
            return ToolResult(rc == 0, f"✓ Build done\n{out[-400:]}" if rc == 0 else f"✗ {out[-400:]}")
        except Exception as e:
            return ToolResult(False, f"✗ npm build failed: {e}")

    @staticmethod
    def npm_publish(path: str) -> ToolResult:
        try:
            rc, out = PackageManagerTool._run(["npm", "publish"], cwd=path)
            return ToolResult(rc == 0, f"✓ Package published\n{out}" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ npm publish failed: {e}")

    @staticmethod
    def npm_list(path: str = ".", depth: int = 0) -> ToolResult:
        try:
            rc, out = PackageManagerTool._run(["npm", "list", f"--depth={depth}", "--json"], cwd=path)
            try:
                data = json.loads(out)
            except Exception:
                data = out
            return ToolResult(rc == 0, f"✓ npm list", data)
        except Exception as e:
            return ToolResult(False, f"✗ npm list failed: {e}")

    @staticmethod
    def npm_update(path: str = ".", packages: list = None) -> ToolResult:
        try:
            args = ["npm", "update"] + (packages or [])
            rc, out = PackageManagerTool._run(args, cwd=path)
            return ToolResult(rc == 0, f"✓ npm update done" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ npm update failed: {e}")

    @staticmethod
    def npm_audit(path: str = ".", fix: bool = False) -> ToolResult:
        try:
            args = ["npm", "audit"] + (["--fix"] if fix else [])
            rc, out = PackageManagerTool._run(args, cwd=path)
            return ToolResult(True, out[-1000:], out)
        except Exception as e:
            return ToolResult(False, f"✗ npm audit failed: {e}")

    # ── yarn ──────────────────────────────────────────────────────────────────
    @staticmethod
    def yarn_install(path: str = ".") -> ToolResult:
        try:
            rc, out = PackageManagerTool._run(["yarn", "install"], cwd=path)
            return ToolResult(rc == 0, f"✓ yarn install done\n{out[-400:]}" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ yarn install failed: {e}")

    @staticmethod
    def yarn_add(path: str, packages: list, dev: bool = False) -> ToolResult:
        try:
            args = ["yarn", "add"] + packages + (["--dev"] if dev else [])
            rc, out = PackageManagerTool._run(args, cwd=path)
            return ToolResult(rc == 0, f"✓ yarn add done" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ yarn add failed: {e}")

    @staticmethod
    def yarn_remove(path: str, packages: list) -> ToolResult:
        try:
            rc, out = PackageManagerTool._run(["yarn", "remove"] + packages, cwd=path)
            return ToolResult(rc == 0, f"✓ yarn remove done" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ yarn remove failed: {e}")

    # ── cargo ─────────────────────────────────────────────────────────────────
    @staticmethod
    def cargo_build(path: str, release: bool = False) -> ToolResult:
        try:
            args = ["cargo", "build"] + (["--release"] if release else [])
            rc, out = PackageManagerTool._run(args, cwd=path, timeout=300)
            return ToolResult(rc == 0, f"✓ cargo build done\n{out[-500:]}" if rc == 0 else f"✗ {out[-500:]}")
        except Exception as e:
            return ToolResult(False, f"✗ cargo build failed: {e}")

    @staticmethod
    def cargo_test(path: str) -> ToolResult:
        try:
            rc, out = PackageManagerTool._run(["cargo", "test"], cwd=path, timeout=300)
            return ToolResult(rc == 0, out[-1000:], out)
        except Exception as e:
            return ToolResult(False, f"✗ cargo test failed: {e}")

    @staticmethod
    def cargo_run(path: str, args_extra: list = None) -> ToolResult:
        try:
            args = ["cargo", "run"] + (args_extra or [])
            rc, out = PackageManagerTool._run(args, cwd=path, timeout=120)
            return ToolResult(rc == 0, out[-1000:], out)
        except Exception as e:
            return ToolResult(False, f"✗ cargo run failed: {e}")

    # ── go ────────────────────────────────────────────────────────────────────
    @staticmethod
    def go_build(path: str, output: str = None) -> ToolResult:
        try:
            args = ["go", "build"] + (["-o", output] if output else []) + ["."]
            rc, out = PackageManagerTool._run(args, cwd=path, timeout=300)
            return ToolResult(rc == 0, f"✓ go build done" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ go build failed: {e}")

    @staticmethod
    def go_test(path: str, verbose: bool = False) -> ToolResult:
        try:
            args = ["go", "test"] + (["-v"] if verbose else []) + ["./..."]
            rc, out = PackageManagerTool._run(args, cwd=path, timeout=300)
            return ToolResult(rc == 0, out[-1000:], out)
        except Exception as e:
            return ToolResult(False, f"✗ go test failed: {e}")

    @staticmethod
    def go_get(path: str, package: str) -> ToolResult:
        try:
            rc, out = PackageManagerTool._run(["go", "get", package], cwd=path)
            return ToolResult(rc == 0, f"✓ go get {package}" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ go get failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# 6. VSCodeTool
# ══════════════════════════════════════════════════════════════════════════════
class VSCodeTool:
    name = "vscode"
    description = (
        "VS Code automation: open files/folders, install/list extensions, "
        "apply settings, format, lint, create/open workspaces"
    )
    use = (
            """
Name of Tool:- VSCodeTool

Purpose of Tool:-
The VSCodeTool provides an automated interface to manage and interact with Visual Studio Code.
It supports opening files, directories, and customized multi-root workspaces; installing, uninstalling, and listing marketplace extensions; programmatically reading and applying user preferences within global configuration profiles (`settings.json`); spinning up automated workspace tasks; and interacting with VS Code's integrated terminal framework.
Additionally, it provides programmatic hooks to execute code document formatting and linting actions (utilizing platform engines like ESLint or Pylint) based on workspace code patterns. All operations run directly via the official VS Code CLI binary (`code`) or direct system file platform operations.

Methods:-

* _code: Internal helper to dispatch system CLI operations down to the VS Code runtime shell.
* _settings_path: Internal multi-platform utility to locate the target active user environment file system path for `settings.json`.
* open_file: Instructs VS Code to launch an active editor layout buffer focused on a specific file path.
* open_folder: Opens an entire project directory window context directly inside the editor instance.
* install_extension: Downloads and configures market extensions using specified marketplace identifiers.
* uninstall_extension: Removes explicit extension dependencies cleanly from the system registry cache.
* list_extensions: Pulls and compiles an array listing of all active ecosystem extensions along with version identifiers.
* run_task: Triggers pre-configured task definitions saved inside a workspace environment layer.
* open_terminal: Fires automation events forcing VS Code to spawn a new instance of an integrated terminal.
* apply_settings: Merges and commits custom structural configurations right into the target system user preferences file.
* get_settings: Loads and decrypts active operational preferences mappings out of system profiles.
* format_file: Forces specific active file buffers to process cosmetic code standard layout transformations.
* lint_workspace: Analyzes current code context trees utilizing active lint tools like ESLint or Pylint.
* create_workspace: Provisions structural multi-root mapping configurations outputting structured `.code-workspace` targets.
* open_workspace: Launches unified development windows mapped strictly to structured workspace definitions.

How to use Tool Methods:-

1. _code:
* Purpose: Internal tool utility wrapping subprocess executions focused on managing the `code` binary wrapper array.
* Arguments:
a) args: list - Positional configurations tracking command parameters dispatched downstream.
* Returns: Tuple holding execution return integer codes and clean consolidated console response buffers.
* How to call: VSCodeTool._code(["--version"])


2. _settings_path:
* Purpose: Core platform structural parser mapping target file location coordinates tracing configuration environments.
* Arguments:
a) scope: str (default: "user") - Target environmental configuration scope filter selector.
* Returns: A strict Path object pointing straight to the operational target location mapping file.
* How to call: VSCodeTool._settings_path(scope="user")


3. open_file:
* Purpose: Focuses editor workspaces directly down onto targeted files.
* Arguments:
a) path: str - Target filesystem location pointer addressing the specific file.
* Returns: ToolResult holding platform execution confirmation details.
* How to call: VSCodeTool.open_file(path="./src/main.py")


4. open_folder:
* Purpose: Directs an editor instance to register and load an entire working code repository tree directory.
* Arguments:
a) path: str - Directory folder path pointing to target workspace locations.
* Returns: ToolResult capturing platform launch execution states.
* How to call: VSCodeTool.open_folder(path="./projects/my-web-app")


5. install_extension:
* Purpose: Registers marketplace modules onto local editing suites.
* Arguments:
a) extension_id: str - Explicit publishing label registry indicator key (e.g., "ms-python.python").
* Returns: ToolResult tracking server validation, completion messages, and process output logs.
* How to call: VSCodeTool.install_extension(extension_id="dbaeumer.vscode-eslint")


6. uninstall_extension:
* Purpose: Cleans out extensions from local application profiles.
* Arguments:
a) extension_id: str - Target marker tag identifying marketplace code segments.
* Returns: ToolResult conveying termination confirmation outcomes.
* How to call: VSCodeTool.uninstall_extension(extension_id="ms-python.python")


7. list_extensions:
* Purpose: Collects diagnostic metadata profiling active platform extensions.
* Arguments: None.
* Returns: ToolResult providing a success flag along with an integrated array holding active extensions names and versions.
* How to call: VSCodeTool.list_extensions()


8. run_task:
* Purpose: Directs local workspace configurations to trigger tasks registered within internal setups.
* Arguments:
a) task_name: str - Specific task identifier label reference target string.
b) workspace: str - Target path folder pointing directly onto active project scopes.
* Returns: ToolResult capturing structural execution validation confirmations.
* How to call: VSCodeTool.run_task(task_name="build", workspace="./projects/my-web-app")


9. open_terminal:
* Purpose: Spawns clean operational platform terminal cells inside localized window views.
* Arguments:
a) workspace: str - Target destination coordinate mapping workspace paths.
* Returns: ToolResult recording validation status states.
* How to call: VSCodeTool.open_terminal(workspace="./projects/my-web-app")


10. apply_settings:
* Purpose: Injects and appends configurations right inside persistent active preference matrices.
* Arguments:
a) settings_dict: dict - Explicit parameter blocks detailing settings names and parameters (e.g., {"editor.fontSize": 14}).
b) scope: str (default: "user") - Environmental profile system boundary marker identifier.
* Returns: ToolResult stating structural state changes.
* How to call: VSCodeTool.apply_settings(settings_dict={"editor.tabSize": 2, "workbench.colorTheme": "Abyss"})


11. get_settings:
* Purpose: Extracts stored user configurations out from underlying active environment profiles.
* Arguments:
a) scope: str (default: "user") - Targeted system settings profile layer selector.
* Returns: ToolResult enclosing structural dictionaries reflecting mapped environment parameters.
* How to call: VSCodeTool.get_settings(scope="user")


12. format_file:
* Purpose: Synchronizes structural code visual layers to match standard workspace layout style choices.
* Arguments:
a) path: str - Local file mapping coordinate location target pointing to a specific document.
* Returns: ToolResult certifying process compliance outcomes.
* How to call: VSCodeTool.format_file(path="./src/utils.js")


13. lint_workspace:
* Purpose: Scans code structure to flag errors using localized analysis rulesets.
* Arguments:
a) path: str - Target codebase root location mapping folder direction.
* Returns: ToolResult mapping validation results and containing trimmed console stream diagnostic outputs.
* How to call: VSCodeTool.lint_workspace(path="./src")


14. create_workspace:
* Purpose: Compiles a custom operational multi-root configuration manifest into a workspace file.
* Arguments:
a) path: str - Target path tracking destination locations outputting workspace files.
b) folders: list - Explicit directory root tracking lists referencing mapped project component locations.
c) settings: dict (default: None) - Context configuration overrides applied to the specific workspace scope.
* Returns: ToolResult returning initialization parameters and dictionary logs mapping asset locations.
* How to call: VSCodeTool.create_workspace(path="./dev.code-workspace", folders=["./api", "./frontend"], settings={"liveServer.settings.port": 5500})


15. open_workspace:
* Purpose: Restores operational views focused onto specific workspace layouts using configuration blueprints.
* Arguments:
a) path: str - Target destination string tracking specialized project configuration components.
* Returns: ToolResult checking terminal return processes.
* How to call: VSCodeTool.open_workspace(path="./dev.code-workspace")
""")

    @staticmethod
    def _code(args: list) -> tuple:
        r = subprocess.run(["code"] + args, capture_output=True, text=True)
        return r.returncode, (r.stdout + r.stderr).strip()

    @staticmethod
    def _settings_path(scope: str = "user") -> Path:
        s = platform.system()
        if s == "Windows":
            base = Path(os.environ.get("APPDATA", "")) / "Code" / "User"
        elif s == "Darwin":
            base = Path.home() / "Library" / "Application Support" / "Code" / "User"
        else:
            base = Path.home() / ".config" / "Code" / "User"
        return base / "settings.json"

    @staticmethod
    def open_file(path: str) -> ToolResult:
        try:
            rc, out = VSCodeTool._code([path])
            return ToolResult(rc == 0, f"✓ Opened {path} in VS Code" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ open_file failed: {e}")

    @staticmethod
    def open_folder(path: str) -> ToolResult:
        try:
            rc, out = VSCodeTool._code([path])
            return ToolResult(rc == 0, f"✓ Opened folder {path}" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ open_folder failed: {e}")

    @staticmethod
    def install_extension(extension_id: str) -> ToolResult:
        try:
            rc, out = VSCodeTool._code(["--install-extension", extension_id])
            return ToolResult(rc == 0, f"✓ Extension '{extension_id}' installed\n{out}" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ install_extension failed: {e}")

    @staticmethod
    def uninstall_extension(extension_id: str) -> ToolResult:
        try:
            rc, out = VSCodeTool._code(["--uninstall-extension", extension_id])
            return ToolResult(rc == 0, f"✓ Extension '{extension_id}' uninstalled" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ uninstall_extension failed: {e}")

    @staticmethod
    def list_extensions() -> ToolResult:
        try:
            rc, out = VSCodeTool._code(["--list-extensions", "--show-versions"])
            exts = [l for l in out.splitlines() if l]
            return ToolResult(rc == 0, f"✓ {len(exts)} extensions installed", exts)
        except Exception as e:
            return ToolResult(False, f"✗ list_extensions failed: {e}")

    @staticmethod
    def run_task(task_name: str, workspace: str) -> ToolResult:
        try:
            # Use code CLI to run a task in the given workspace
            rc, out = VSCodeTool._code([workspace, "--run-task", task_name])
            return ToolResult(rc == 0, f"✓ Task '{task_name}' run" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ run_task failed: {e}")

    @staticmethod
    def open_terminal(workspace: str) -> ToolResult:
        try:
            # Open VS Code integrated terminal in the workspace
            rc, out = VSCodeTool._code([workspace, "--command", "workbench.action.terminal.new"])
            return ToolResult(rc == 0, f"✓ Terminal opened in {workspace}" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ open_terminal failed: {e}")

    @staticmethod
    def apply_settings(settings_dict: dict, scope: str = "user") -> ToolResult:
        try:
            sp = VSCodeTool._settings_path(scope)
            sp.parent.mkdir(parents=True, exist_ok=True)
            existing = {}
            if sp.exists():
                try:
                    existing = json.loads(sp.read_text())
                except Exception:
                    existing = {}
            existing.update(settings_dict)
            sp.write_text(json.dumps(existing, indent=4))
            return ToolResult(True, f"✓ Applied {len(settings_dict)} settings to {scope} settings.json")
        except Exception as e:
            return ToolResult(False, f"✗ apply_settings failed: {e}")

    @staticmethod
    def get_settings(scope: str = "user") -> ToolResult:
        try:
            sp = VSCodeTool._settings_path(scope)
            if not sp.exists():
                return ToolResult(True, "✓ No settings file found (using defaults)", {})
            data = json.loads(sp.read_text())
            return ToolResult(True, f"✓ {len(data)} settings loaded", data)
        except Exception as e:
            return ToolResult(False, f"✗ get_settings failed: {e}")

    @staticmethod
    def format_file(path: str) -> ToolResult:
        try:
            rc, out = VSCodeTool._code(["--wait", path, "--command", "editor.action.formatDocument"])
            return ToolResult(rc == 0, f"✓ Formatted {path}" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ format_file failed: {e}")

    @staticmethod
    def lint_workspace(path: str) -> ToolResult:
        try:
            # Run eslint if available, otherwise pylint for Python
            if any(Path(path).glob("*.js")) or any(Path(path).glob("*.ts")):
                rc, out = subprocess.run(["npx", "eslint", path, "--format=compact"],
                                         capture_output=True, text=True, cwd=path).returncode, ""
                r = subprocess.run(["npx", "eslint", path, "--format=compact"],
                                   capture_output=True, text=True, cwd=path)
                return ToolResult(r.returncode == 0, (r.stdout + r.stderr)[-1000:])
            else:
                r = subprocess.run([sys.executable, "-m", "pylint", path, "--output-format=text"],
                                   capture_output=True, text=True)
                return ToolResult(r.returncode in (0, 4), (r.stdout + r.stderr)[-1000:])
        except Exception as e:
            return ToolResult(False, f"✗ lint_workspace failed: {e}")

    @staticmethod
    def create_workspace(path: str, folders: list, settings: dict = None) -> ToolResult:
        try:
            ws_data = {
                "folders": [{"path": f} for f in folders],
                "settings": settings or {}
            }
            ws_path = Path(path)
            if not ws_path.suffix == ".code-workspace":
                ws_path = ws_path.with_suffix(".code-workspace")
            ws_path.parent.mkdir(parents=True, exist_ok=True)
            ws_path.write_text(json.dumps(ws_data, indent=4))
            return ToolResult(True, f"✓ Workspace created: {ws_path}", {"path": str(ws_path)})
        except Exception as e:
            return ToolResult(False, f"✗ create_workspace failed: {e}")

    @staticmethod
    def open_workspace(path: str) -> ToolResult:
        try:
            rc, out = VSCodeTool._code([path])
            return ToolResult(rc == 0, f"✓ Workspace '{path}' opened" if rc == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ open_workspace failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# 7. TerminalTool
# ══════════════════════════════════════════════════════════════════════════════
class TerminalTool:
    name = "terminal"
    description = (
        "Advanced terminal/shell: run commands, scripts, env vars, aliases, "
        "process management, which/is_installed checks"
    )
    use = (
           """Name of Tool:- TerminalTool

Purpose of Tool:- 
The TerminalTool provides an advanced programmatic bridge to interface directly with host operating system shells and lower-level execution subsystems. 
It supports standard detached command dispatches, real-time interactive stdout/stderr data streaming, and cross-platform script evaluations across Bash or PowerShell profiles. 
Additionally, the tool houses deep system context auditing mechanics, letting users mutate runtime environment variables, apply cross-session structural aliases, locate system binary binaries (`which`), install dependencies using default native package managers (`winget`, `Homebrew`, `apt`), and explicitly supervise system process workflows (listing, identifying resources, or forcing terminate signals via `psutil`).

Methods:-
- run: Runs standard system commands inside an underlying shell environment with precise lifespan timeouts.
- run_interactive: Streams out complex step-by-step console outputs from commands utilizing dedicated platform pipe routines.
- run_script: Generates dynamic temporary automated script assets to assess multi-line program executions.
- run_in_new_terminal: Launches explicit isolated external workspace windows to hold persistent process sessions.
- set_env_var: Registers temporary memory structures or edits cross-session user hardware variables.
- get_env_var: References current system dictionaries to extract active value indicators.
- list_env_vars: Enumerates active variable string landscapes using optional pattern matches.
- source_file: Dynamically parses static property text layouts to seamlessly register environments in the current process memory.
- which: Runs filesystem mapping evaluations to point to exact executable location origins.
- is_installed: Validates whether target framework commands exist and are instantly ready to process tasks.
- install_via_package_manager: Leverages native system managers to configure missing structural binaries.
- create_alias: Appends convenient short command lookup tags to reduce typing or save repetitive syntax sequences.
- list_processes: Queries host kernels to track active runtime resource tables.
- kill_process: Dispatches termination signals to stop specific process loops by name or ID references.
- get_process_info: Extracts deep metrics tracking memory loads, timing signatures, and location profiles of specific processes.

How to use Tool Methods:-

1. run:
   - Purpose: Dispatches commands downstream straight to active underlying shell runtimes.
   - Arguments:
     a) command: str - Raw string parameter outlining the targeted system execution syntax.
     b) cwd: str (default: None) - Working directory workspace target location path.
     c) timeout: int (default: 60) - Threshold window capping allowed execution run times.
     d) env: dict (default: None) - Contextual environment variables injected alongside default environments.
     e) shell: bool (default: True) - Evaluates string syntax utilizing the underlying platform command parser.
     f) capture: bool (default: True) - Determines whether process console outputs are recorded or ignored.
   - Returns: ToolResult holding success evaluation metrics and capturing standard output streams.
   - How to call: TerminalTool.run(command="echo $USER", timeout=30, env={"DEBUG": "true"})

2. run_interactive:
   - Purpose: Captures continuous real-time output line streams from long-running command tasks.
   - Arguments:
     a) command: str - Structural command path strings destined for parsing.
     b) cwd: str (default: None) - Directory destination controlling target execution spaces.
   - Returns: ToolResult containing aggregated output lines collected prior to process finalization.
   - How to call: TerminalTool.run_interactive(command="ping -c 4 google.com")

3. run_script:
   - Purpose: Evaluates multi-line runtime script sequences by wrapping content in automated temp files.
   - Arguments:
     a) script_content: str - Raw code strings representing target automated instructions.
     b) shell: str (default: None) - Target interpreter mapping settings override (e.g., "bash", "powershell").
     c) cwd: str (default: None) - Filesystem reference directory path guiding script runtime environments.
   - Returns: ToolResult summarizing outcome statuses and returning compiled log entries.
   - How to call: TerminalTool.run_script(script_content="echo 'Start Execution'\nls -la\necho 'Done'", shell="bash")

4. run_in_new_terminal:
   - Purpose: Spawns completely separate user workspace terminal windows to run decoupled background sessions.
   - Arguments:
     a) command: str - Target execution statements thrown inside newly opened environment layouts.
   - Returns: ToolResult verifying external workspace shell request initialization metrics.
   - How to call: TerminalTool.run_in_new_terminal(command="python -m http.server 8080")

5. set_env_var:
   - Purpose: Modifies environment state dictionaries in active workspaces or persistent machine profiles.
   - Arguments:
     a) key: str - Tracking identifier variable label name.
     b) value: str - Value payload assigned to the target variable pointer.
     c) persistent: bool (default: False) - Appends variables permanently inside OS initialization profiles (e.g., `.bashrc`, Registry).
     d) scope: str (default: "user") - Delimits profile boundaries for environment integration steps.
   - Returns: ToolResult mapping variable modification state records.
   - How to call: TerminalTool.set_env_var(key="API_KEY", value="secret_token_abc123", persistent=True)

6. get_env_var:
   - Purpose: Retreives specific values stored behind designated environment pointer tags.
   - Arguments:
     a) key: str - Target variable identifier key label name.
   - Returns: ToolResult holding string values matching system lookup parameters.
   - How to call: TerminalTool.get_env_var(key="PATH")

7. list_env_vars:
   - Purpose: Compiles a dictionary mapping out active variables on the host environment.
   - Arguments:
     a) filter: str (default: None) - Substring matching criteria to narrow results down to specific key groups.
   - Returns: ToolResult encapsulating structured dictionaries mapping environment metrics.
   - How to call: TerminalTool.list_env_vars(filter="XDG")

8. source_file:
   - Purpose: Reads static resource documents to inject explicit configuration lists into immediate runtime scopes.
   - Arguments:
     a) path: str - Location route to target environment setting file definitions.
   - Returns: ToolResult capturing loaded parameter entries and validation outcomes.
   - How to call: TerminalTool.source_file(path="./config/.env")

9. which:
   - Purpose: Pinpoints exact directory locations hosting specific target tools.
   - Arguments:
     a) command: str - Binary lookup tag parameter destined for tracking queries.
   - Returns: ToolResult providing path strings mapping location findings.
   - How to call: TerminalTool.which(command="git")

10. is_installed:
    - Purpose: Verifies tool configuration conditions prior to attempting process executions.
    - Arguments:
      a) command: str - Key search criteria referencing the target software package.
    - Returns: ToolResult embedding boolean statuses reflecting binary availability.
    - How to call: TerminalTool.is_installed(command="docker")

11. install_via_package_manager:
    - Purpose: Automatically sets up dependencies using available host management systems.
    - Arguments:
      a) package: str - Name identifier matching requested remote package repository definitions.
    - Returns: ToolResult recording terminal logs outputted during installer transactions.
    - How to call: TerminalTool.install_via_package_manager(package="htop")

12. create_alias:
    - Purpose: Configures macro short-keys to quickly invoke longer command phrases.
    - Arguments:
      a) name: str - Target short token mapped into environment profiles.
      b) command: str - Full command string context bound to the short token alias.
      c) persistent: bool (default: False) - Appends configurations inside shell profiles to keep them active across reboots.
    - Returns: ToolResult tracking registration states.
    - How to call: TerminalTool.create_alias(name="ll", command="ls -la --color=auto", persistent=True)

13. list_processes:
    - Purpose: Captures runtime snapshots detailing system resource usage.
    - Arguments:
      a) filter: str (default: None) - Substring keyword checks to filter items matching target names.
    - Returns: ToolResult framing arrays packed with object stats tracking ID, Name, Status, and RAM usage.
    - How to call: TerminalTool.list_processes(filter="node")

14. kill_process:
    - Purpose: Stops system processes to reclaim hardware resources or kill non-responsive assets.
    - Arguments:
      a) pid_or_name: str - Numeric ID numbers or matching string name signatures of targeted processes.
    - Returns: ToolResult listing array integers mapping terminated elements.
    - How to call: TerminalTool.kill_process(pid_or_name="8392")

15. get_process_info:
    - Purpose: Inspects specific tasks to extract performance details.
    - Arguments:
      a) pid: int - Unique process tracking id number constraint parameter.
    - Returns: ToolResult enclosing data objects mapping paths, status, execution code histories, and CPU loads.
    - How to call: TerminalTool.get_process_info(pid=1024)""")

    @staticmethod
    def run(command: str, cwd: str = None, timeout: int = 60,
            env: dict = None, shell: bool = True, capture: bool = True) -> ToolResult:
        try:
            merged_env = {**os.environ, **(env or {})}
            r = subprocess.run(
                command, cwd=cwd, timeout=timeout,
                env=merged_env, shell=shell,
                capture_output=capture, text=True
            )
            out = ((r.stdout or "") + (r.stderr or "")).strip() if capture else "✓ Done (output not captured)"
            return ToolResult(r.returncode == 0, out or "✓ Done", out)
        except subprocess.TimeoutExpired:
            return ToolResult(False, f"✗ Command timed out after {timeout}s")
        except Exception as e:
            return ToolResult(False, f"✗ run failed: {e}")

    @staticmethod
    def run_interactive(command: str, cwd: str = None) -> ToolResult:
        try:
            import shlex
            proc = subprocess.Popen(
                shlex.split(command) if not isinstance(command, list) else command,
                cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            )
            lines = []
            for line in proc.stdout:
                lines.append(line.rstrip())
            proc.wait()
            out = "\n".join(lines)
            return ToolResult(proc.returncode == 0, out[-2000:] or "✓ Done", out)
        except Exception as e:
            return ToolResult(False, f"✗ run_interactive failed: {e}")

    @staticmethod
    def run_script(script_content: str, shell: str = None, cwd: str = None) -> ToolResult:
        try:
            shell = shell or ("bash" if platform.system() != "Windows" else "powershell")
            suffix = ".sh" if "bash" in shell else (".ps1" if "powershell" in shell else ".sh")
            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False, mode="w") as tf:
                tf.write(script_content)
                tf.flush()
                script_path = tf.name
            if platform.system() != "Windows":
                os.chmod(script_path, 0o755)
            r = subprocess.run([shell, script_path], cwd=cwd, capture_output=True, text=True, timeout=120)
            os.unlink(script_path)
            out = (r.stdout + r.stderr).strip()
            return ToolResult(r.returncode == 0, out[-2000:] or "✓ Script done", out)
        except Exception as e:
            return ToolResult(False, f"✗ run_script failed: {e}")

    @staticmethod
    def run_in_new_terminal(command: str) -> ToolResult:
        try:
            s = platform.system()
            if s == "Windows":
                subprocess.Popen(["start", "cmd", "/k", command], shell=True)
            elif s == "Darwin":
                apple_script = f'tell app "Terminal" to do script "{command}"'
                subprocess.Popen(["osascript", "-e", apple_script])
            else:
                for term in ["gnome-terminal", "xterm", "konsole"]:
                    if shutil.which(term):
                        subprocess.Popen([term, "--", "bash", "-c", command])
                        break
            return ToolResult(True, f"✓ Command launched in new terminal")
        except Exception as e:
            return ToolResult(False, f"✗ run_in_new_terminal failed: {e}")

    @staticmethod
    def set_env_var(key: str, value: str, persistent: bool = False, scope: str = "user") -> ToolResult:
        try:
            os.environ[key] = value
            if persistent:
                s = platform.system()
                if s == "Windows":
                    subprocess.run(["setx", key, value], capture_output=True)
                else:
                    shell_rc = Path.home() / (".bashrc" if "bash" in os.environ.get("SHELL", "") else ".zshrc")
                    if not shell_rc.exists():
                        shell_rc = Path.home() / ".bashrc"
                    content = shell_rc.read_text() if shell_rc.exists() else ""
                    marker = f"export {key}="
                    lines = [l for l in content.splitlines() if not l.startswith(marker)]
                    lines.append(f'export {key}="{value}"')
                    shell_rc.write_text("\n".join(lines) + "\n")
            return ToolResult(True, f"✓ Set {key}={value}" + (" (persistent)" if persistent else ""))
        except Exception as e:
            return ToolResult(False, f"✗ set_env_var failed: {e}")

    @staticmethod
    def get_env_var(key: str) -> ToolResult:
        try:
            val = os.environ.get(key)
            if val is None:
                return ToolResult(False, f"✗ Env var '{key}' not found")
            return ToolResult(True, f"✓ {key}={val}", val)
        except Exception as e:
            return ToolResult(False, f"✗ get_env_var failed: {e}")

    @staticmethod
    def list_env_vars(filter: str = None) -> ToolResult:
        try:
            env = dict(os.environ)
            if filter:
                env = {k: v for k, v in env.items() if filter.lower() in k.lower()}
            return ToolResult(True, f"✓ {len(env)} env vars", env)
        except Exception as e:
            return ToolResult(False, f"✗ list_env_vars failed: {e}")

    @staticmethod
    def source_file(path: str) -> ToolResult:
        try:
            content = Path(path).read_text()
            updated = {}
            for line in content.splitlines():
                line = line.strip()
                if line.startswith("export "):
                    line = line[7:]
                if "=" in line and not line.startswith("#"):
                    k, _, v = line.partition("=")
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    os.environ[k] = v
                    updated[k] = v
            return ToolResult(True, f"✓ Sourced {len(updated)} vars from {path}", updated)
        except Exception as e:
            return ToolResult(False, f"✗ source_file failed: {e}")

    @staticmethod
    def which(command: str) -> ToolResult:
        try:
            path = shutil.which(command)
            if path:
                return ToolResult(True, f"✓ {command} → {path}", path)
            return ToolResult(False, f"✗ '{command}' not found in PATH")
        except Exception as e:
            return ToolResult(False, f"✗ which failed: {e}")

    @staticmethod
    def is_installed(command: str) -> ToolResult:
        try:
            found = shutil.which(command) is not None
            return ToolResult(found, f"✓ '{command}' is installed" if found else f"✗ '{command}' not found", found)
        except Exception as e:
            return ToolResult(False, f"✗ is_installed failed: {e}")

    @staticmethod
    def install_via_package_manager(package: str) -> ToolResult:
        try:
            s = platform.system()
            if s == "Windows":
                r = subprocess.run(["winget", "install", package], capture_output=True, text=True)
            elif s == "Darwin":
                r = subprocess.run(["brew", "install", package], capture_output=True, text=True)
            else:
                # Try apt, then dnf, then pacman
                for pm in [["apt-get", "install", "-y"], ["dnf", "install", "-y"], ["pacman", "-S", "--noconfirm"]]:
                    if shutil.which(pm[0]):
                        r = subprocess.run(["sudo"] + pm + [package], capture_output=True, text=True)
                        break
                else:
                    return ToolResult(False, "✗ No supported package manager found (apt/dnf/pacman)")
            out = (r.stdout + r.stderr).strip()
            return ToolResult(r.returncode == 0, f"✓ Installed '{package}'\n{out[-300:]}" if r.returncode == 0 else f"✗ {out[-300:]}")
        except Exception as e:
            return ToolResult(False, f"✗ install_via_package_manager failed: {e}")

    @staticmethod
    def create_alias(name: str, command: str, persistent: bool = False) -> ToolResult:
        try:
            alias_str = f"alias {name}='{command}'"
            if persistent:
                shell_rc = Path.home() / ".bashrc"
                content = shell_rc.read_text() if shell_rc.exists() else ""
                if alias_str not in content:
                    with open(shell_rc, "a") as f:
                        f.write(f"\n{alias_str}\n")
            return ToolResult(True, f"✓ Alias created: {alias_str}" + (" (persistent)" if persistent else " (session only)"))
        except Exception as e:
            return ToolResult(False, f"✗ create_alias failed: {e}")

    @staticmethod
    def list_processes(filter: str = None) -> ToolResult:
        try:
            import psutil
            procs = []
            for p in psutil.process_iter(["pid", "name", "status", "cpu_percent", "memory_info"]):
                try:
                    info = p.info
                    if filter and filter.lower() not in info["name"].lower():
                        continue
                    procs.append({"pid": info["pid"], "name": info["name"],
                                  "status": info["status"],
                                  "mem_mb": round(info["memory_info"].rss / 1e6, 1) if info["memory_info"] else 0})
                except Exception:
                    continue
            return ToolResult(True, f"✓ {len(procs)} processes", procs)
        except Exception as e:
            return ToolResult(False, f"✗ list_processes failed: {e}")

    @staticmethod
    def kill_process(pid_or_name: str) -> ToolResult:
        try:
            import psutil, signal
            killed = []
            for p in psutil.process_iter(["pid", "name"]):
                try:
                    info = p.info
                    if str(info["pid"]) == str(pid_or_name) or info["name"] == pid_or_name:
                        p.kill()
                        killed.append(info["pid"])
                except Exception:
                    continue
            if killed:
                return ToolResult(True, f"✓ Killed PIDs: {killed}", killed)
            return ToolResult(False, f"✗ No process matching '{pid_or_name}' found")
        except Exception as e:
            return ToolResult(False, f"✗ kill_process failed: {e}")

    @staticmethod
    def get_process_info(pid: int) -> ToolResult:
        try:
            import psutil
            p = psutil.Process(pid)
            info = {
                "pid": p.pid, "name": p.name(), "status": p.status(),
                "cpu_percent": p.cpu_percent(interval=0.5),
                "mem_mb": round(p.memory_info().rss / 1e6, 1),
                "cmdline": " ".join(p.cmdline()),
                "cwd": p.cwd(), "created": p.create_time()
            }
            return ToolResult(True, f"✓ Process info for PID {pid}", info)
        except Exception as e:
            return ToolResult(False, f"✗ get_process_info failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# 8. MakefileTool
# ══════════════════════════════════════════════════════════════════════════════
class MakefileTool:
    name = "makefile"
    description = "Makefile build system: run targets, list targets, create and edit Makefiles"
    use = (
            """Name of Tool:- MakefileTool

Purpose of Tool:- 
The MakefileTool serves as an automated programmatic management system built to interact with the GNU Make build automation infrastructure. 
It facilitates parsing existing build assets, dynamically structuring or appending compilation graphs (including auto-managing `.PHONY` macro headers), identifying actionable instruction pipelines inside source code blocks via Regular Expressions, and securely executing targeted build steps inside isolated subprocess shells with absolute context tracking, runtime timeout constraints, and merged system environments.

Methods:-
- run_target: Executes a specific build ruleset using system `make` wrappers against a target workspace directory.
- list_targets: Parses static Makefile layouts with pattern evaluation to harvest valid execution targets.
- create_makefile: Constructs entirely new, valid build files utilizing dictionary schemas defining rule sets, scripts, and pre-requisites.
- add_target: Modifies existing build configurations by appending fresh instructions and updating global macro namespaces.

How to use Tool Methods:-

1. run_target:
   - Purpose: Directs local shell tasks to run individual recipe chains configured inside an available template configuration file.
   - Arguments:
     a) makefile_path: str - Specific path pointing straight to the core configuration asset.
     b) target: str (default: "all") - Explicit rule label designated for activation.
     c) args: list (default: None) - Additional modifier configuration flags appended into standard executions.
     d) env: dict (default: None) - Runtime property maps merged alongside system setups.
   - Returns: ToolResult holding deployment status evaluations and reporting final output log structures.
   - How to call: MakefileTool.run_target(makefile_path="./src/Makefile", target="build", args=["--silent"])

2. list_targets:
   - Purpose: Scans build asset structural layouts to identify functional pipeline triggers.
   - Arguments:
     a) makefile_path: str - Local filesystem path where the target rule specification document resides.
   - Returns: ToolResult providing an execution boolean confirmation alongside a verified collection of target keys.
   - How to call: MakefileTool.list_targets(makefile_path="./Makefile")

3. create_makefile:
   - Purpose: Generates raw blueprint documentation formatted with appropriate tab spacing delimiters.
   - Arguments:
     a) path: str - Target coordinate where the processed compilation script is created.
     b) targets_dict: dict - Deep nested map structures tracking definitions (e.g., `{"test": {"deps": ["clean"], "commands": ["pytest"]}}`).
   - Returns: ToolResult storing validation success flags and outputting generated plaintext text code matrices.
   - How to call: MakefileTool.create_makefile(path="./Makefile", targets_dict={"clean": {"commands": ["rm -rf build/"]}, "all": {"deps": ["clean"], "commands": ["echo done"]}})

4. add_target:
   - Purpose: Appends customized step blocks straight onto modern existing workflow frameworks.
   - Arguments:
     a) makefile_path: str - Destination tracking coordinates locating files to edit.
     b) name: str - Identifier token mapped to identify the incoming execution recipe rule block.
     b) deps: list (default: None) - Array listing requirements items needed prior to activating targeted recipes.
     c) commands: list (default: None) - Execution tasks to track and process inside targeted configurations.
   - Returns: ToolResult confirming rule changes and output validation states.
   - How to call: MakefileTool.add_target(makefile_path="./Makefile", name="deploy", deps=["build"], commands=["docker push image:latest"])""")
    
    @staticmethod
    def run_target(makefile_path: str, target: str = "all",
                   args: list = None, env: dict = None) -> ToolResult:
        try:
            make_dir = str(Path(makefile_path).parent)
            cmd = ["make", "-f", str(makefile_path), target] + (args or [])
            merged_env = {**os.environ, **(env or {})}
            r = subprocess.run(cmd, cwd=make_dir, capture_output=True, text=True,
                               env=merged_env, timeout=300)
            out = (r.stdout + r.stderr).strip()
            return ToolResult(r.returncode == 0,
                              f"✓ make {target} done\n{out[-800:]}" if r.returncode == 0 else f"✗ make {target} failed\n{out[-800:]}")
        except Exception as e:
            return ToolResult(False, f"✗ run_target failed: {e}")

    @staticmethod
    def list_targets(makefile_path: str) -> ToolResult:
        try:
            content = Path(makefile_path).read_text()
            targets = []
            for line in content.splitlines():
                # Match lines like "target:" or "target: dep1 dep2"
                m = re.match(r'^([a-zA-Z0-9_\-\.]+)\s*:', line)
                if m and not line.startswith("\t") and not line.startswith("#"):
                    target = m.group(1)
                    if target not in (".PHONY", ".DEFAULT", "targets"):
                        targets.append(target)
            return ToolResult(True, f"✓ {len(targets)} targets found", targets)
        except Exception as e:
            return ToolResult(False, f"✗ list_targets failed: {e}")

    @staticmethod
    def create_makefile(path: str, targets_dict: dict) -> ToolResult:
        """targets_dict: {'target_name': {'deps': ['dep1'], 'commands': ['cmd1']}}"""
        try:
            lines = [".PHONY: " + " ".join(targets_dict.keys()), ""]
            for target, info in targets_dict.items():
                deps = " ".join(info.get("deps", []))
                lines.append(f"{target}: {deps}")
                for cmd in info.get("commands", []):
                    lines.append(f"\t{cmd}")
                lines.append("")
            content = "\n".join(lines)
            Path(path).write_text(content)
            return ToolResult(True, f"✓ Makefile created at {path}", content)
        except Exception as e:
            return ToolResult(False, f"✗ create_makefile failed: {e}")

    @staticmethod
    def add_target(makefile_path: str, name: str,
                   deps: list = None, commands: list = None) -> ToolResult:
        try:
            existing = Path(makefile_path).read_text() if Path(makefile_path).exists() else ""
            deps_str = " ".join(deps or [])
            new_block = f"\n{name}: {deps_str}\n"
            for cmd in (commands or []):
                new_block += f"\t{cmd}\n"
            # Update .PHONY if present
            if ".PHONY:" in existing:
                existing = re.sub(r"(\.PHONY:.*)", r"\1 " + name, existing, count=1)
            Path(makefile_path).write_text(existing + new_block)
            return ToolResult(True, f"✓ Target '{name}' added to {makefile_path}")
        except Exception as e:
            return ToolResult(False, f"✗ add_target failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# 9. CMakeTool
# ══════════════════════════════════════════════════════════════════════════════
class CMakeTool:
    name = "cmake"
    description = "CMake build system: configure, build, install, clean, ctest"
    use = (
            """Name of Tool:- CMakeTool

Purpose of Tool:- 
The CMakeTool acts as a standardized programmatic controller for the cross-platform CMake meta-build generation ecosystem. 
It automates project setup loops, multi-threaded workspace builds, cross-compilation configurations, deployment targets, artifact cleanups, and CTest regression check suites. 
Instead of interacting with localized, platform-specific build systems directly, this tool abstracts system generation behaviors inside managed subprocess environments, allowing uniform automation across Windows, macOS, and Linux runtimes with precise timeout parameters.

Methods:-
- configure: Scans project source structures to generate build layouts and project variables inside a chosen output workspace folder.
- build: Translates configured source matrices into native binaries or library targets using downstream system compilers.
- install: Deploys compiled project artifacts out to system layout prefixes or customized location trees.
- clean: Purges compiled intermediate files, object graphs, and caching assets inside target workspaces to force clean builds.
- run_ctest: Orchestrates CTest test suites to parse and evaluate functional code validations across build configurations.

How to use Tool Methods:-

1. configure:
   - Purpose: Initalizes structural build configurations using chosen toolchains and definitions.
   - Arguments:
     a) source_dir: str - File directory location containing the project's root `CMakeLists.txt` file.
     b) build_dir: str - Target workspace folder destination created to store configuration files and binary footprints.
     c) generator: str (default: None) - Directs CMake to structure files targeting specific toolchains (e.g., "Ninja", "Unix Makefiles").
     d) defines: dict (default: None) - Variable mapping parameters passed downstream as compile flags (e.g., `{"CMAKE_BUILD_TYPE": "Release"}`).
   - Returns: ToolResult holding configuration outcome evaluations and presenting structural error or confirmation log streams.
   - How to call: CMakeTool.configure(source_dir="./src", build_dir="./build", generator="Ninja", defines={"BUILD_SHARED_LIBS": "ON"})

2. build:
   - Purpose: Directs local toolchains to process source file translations based on generated configuration plans.
   - Arguments:
     a) build_dir: str - Directory target area holding configured active project blueprints.
     b) target: str (default: None) - Instructs compilers to isolate build focus straight to individual project binaries.
     c) jobs: int (default: None) - Capping limit defining concurrent thread processes allocated for compiling code.
   - Returns: ToolResult storing build compliance indicators and returning compiled log entries.
   - How to call: CMakeTool.build(build_dir="./build", target="my_executable", jobs=4)

3. install:
   - Purpose: Dispatches compiled binaries, runtime libraries, and system header assets directly to localized installation targets.
   - Arguments:
     a) build_dir: str - Root repository workspace directory where assets were built.
     b) prefix: str (default: None) - Targeted system installation path mapping destination directory context names (e.g., `/usr/local`).
   - Returns: ToolResult verifying transaction finalization output traces.
   - How to call: CMakeTool.install(build_dir="./build", prefix="./dist")

4. clean:
   - Purpose: Sweeps intermediate build outputs, temporary caches, and compiled binary layouts out from targets.
   - Arguments:
     a) build_dir: str - Target directory path context housing active operational setups.
   - Returns: ToolResult mapping data purge process evaluations.
   - How to call: CMakeTool.clean(build_dir="./build")

5. run_ctest:
   - Purpose: Drives built-in regression testing tools across configured workspaces.
   - Arguments:
     a) build_dir: str - Directory destination hosting completed code components and evaluation targets.
     b) verbose: bool (default: False) - Demands extensive verbose console readouts tracing sub-component details.
   - Returns: ToolResult mapping testing performance results and full outcome log arrays.
   - How to call: CMakeTool.run_ctest(build_dir="./build", verbose=True)
   """)
        
    @staticmethod
    def configure(source_dir: str, build_dir: str,
                  generator: str = None, defines: dict = None) -> ToolResult:
        try:
            Path(build_dir).mkdir(parents=True, exist_ok=True)
            args = ["cmake", source_dir, "-B", build_dir]
            if generator:
                args += ["-G", generator]
            for k, v in (defines or {}).items():
                args.append(f"-D{k}={v}")
            r = subprocess.run(args, capture_output=True, text=True, cwd=source_dir, timeout=120)
            out = (r.stdout + r.stderr).strip()
            return ToolResult(r.returncode == 0,
                              f"✓ CMake configured\n{out[-600:]}" if r.returncode == 0 else f"✗ CMake configure failed\n{out[-600:]}")
        except Exception as e:
            return ToolResult(False, f"✗ configure failed: {e}")

    @staticmethod
    def build(build_dir: str, target: str = None, jobs: int = None) -> ToolResult:
        try:
            args = ["cmake", "--build", build_dir]
            if target:
                args += ["--target", target]
            if jobs:
                args += ["--", f"-j{jobs}"]
            r = subprocess.run(args, capture_output=True, text=True, timeout=600)
            out = (r.stdout + r.stderr).strip()
            return ToolResult(r.returncode == 0,
                              f"✓ Build done\n{out[-600:]}" if r.returncode == 0 else f"✗ Build failed\n{out[-600:]}")
        except Exception as e:
            return ToolResult(False, f"✗ build failed: {e}")

    @staticmethod
    def install(build_dir: str, prefix: str = None) -> ToolResult:
        try:
            args = ["cmake", "--install", build_dir]
            if prefix:
                args += ["--prefix", prefix]
            r = subprocess.run(args, capture_output=True, text=True, timeout=120)
            out = (r.stdout + r.stderr).strip()
            return ToolResult(r.returncode == 0,
                              f"✓ Installed to {prefix or 'default prefix'}\n{out}" if r.returncode == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ install failed: {e}")

    @staticmethod
    def clean(build_dir: str) -> ToolResult:
        try:
            r = subprocess.run(["cmake", "--build", build_dir, "--target", "clean"],
                               capture_output=True, text=True, timeout=120)
            out = (r.stdout + r.stderr).strip()
            return ToolResult(r.returncode == 0, f"✓ Cleaned {build_dir}\n{out}" if r.returncode == 0 else f"✗ {out}")
        except Exception as e:
            return ToolResult(False, f"✗ clean failed: {e}")

    @staticmethod
    def run_ctest(build_dir: str, verbose: bool = False) -> ToolResult:
        try:
            args = ["ctest", "--test-dir", build_dir] + (["-V"] if verbose else [])
            r = subprocess.run(args, capture_output=True, text=True, timeout=300)
            out = (r.stdout + r.stderr).strip()
            return ToolResult(r.returncode == 0, out[-1500:], out)
        except Exception as e:
            return ToolResult(False, f"✗ run_ctest failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# 10. DebuggerTool
# ══════════════════════════════════════════════════════════════════════════════
class DebuggerTool:
    name = "debugger"
    description = (
        "Debugging utilities: run with pdb, analyze tracebacks, profile scripts, "
        "memory profiling, find deadlocks, strace"
    )
    use = (
            """Name of Tool:- DebuggerTool

Purpose of Tool:- 
The DebuggerTool serves as an automated analysis and inspection suite built to isolate errors, analyze performance bottlenecks, and monitor process states across localized scripts and running operating system applications. 
It supports automated execution step-throughs using Python's Debugger (`pdb`), regular expression parsing of error tracebacks, resource execution profiling (`cProfile`, `pstats`), inline memory consumption audits, low-level Linux kernel syscall telemetry (`strace`), and multi-threaded deadlock telemetry analysis via system resource lookup engines (`psutil`).

Methods:-
- run_python_with_pdb: Dispatches Python targets down through the default interactive debugger to record initial call stacks.
- analyze_traceback: Parses crash traces with structural regex engines to extract exception details and locate the root-cause file frame.
- profile_script: Executes execution timing audits to find performance bottlenecks, ranking the top slow functions by cumulative time.
- memory_profile: Monitors active application memory allocations line-by-line using localized structural profilers.
- find_deadlocks: Scans thread tables and tracking variables to flag stuck parallel process loops.
- strace_process: Traps lower-level system-wide kernel function dispatches on Linux environments for active process diagnostics.

How to use Tool Methods:-

1. run_python_with_pdb:
   - Purpose: Validates execution loops through the `pdb` module to record process output metrics.
   - Arguments:
     a) script: str - Target filesystem location pointing to the script file.
     b) args: list (default: None) - Contextual execution parameter modifiers passed into the running script.
   - Returns: ToolResult holding execution log buffers and structural outcome details.
   - How to call: DebuggerTool.run_python_with_pdb(script="./src/app.py", args=["--verbose"])

2. analyze_traceback:
   - Purpose: Extracts actionable bug insights out of raw, multiline system traceback strings.
   - Arguments:
     a) traceback_text: str - The raw multi-line error log payload copied out from a process crash.
   - Returns: ToolResult presenting a structured dictionary tracking error classifications, full frame arrays, and location coordinates.
   - How to call: DebuggerTool.analyze_traceback(traceback_text="Traceback (most recent call last):\n  File \"main.py\", line 5, in <module>\n    1/0\nZeroDivisionError: division by zero")

3. profile_script:
   - Purpose: pinpoints performance bottlenecks inside applications.
   - Arguments:
     a) script: str - Target codebase script file location path.
     b) output: str (default: None) - An optional filesystem location to save the compiled binary stats file (`.prof`).
   - Returns: ToolResult delivering a clean table breaking down the top 20 functions sorted by cumulative resource runtime.
   - How to call: DebuggerTool.profile_script(script="./src/compute.py", output="./logs/perf.prof")

4. memory_profile:
   - Purpose: Monitors script memory allocations to flag memory leaks or high hardware overheads.
   - Arguments:
     a) script: str - Target python script file destined for structural memory inspection.
   - Returns: ToolResult containing line-by-line RAM growth evaluations.
   - How to call: DebuggerTool.memory_profile(script="./src/data_processor.py")

5. find_deadlocks:
   - Purpose: Evaluates system thread structures to locate processes frozen waiting for resource locks.
   - Arguments:
     a) pid: int - Unique system process tracking identifier reference number.
   - Returns: ToolResult documenting process connection loads and specifying numbers of stuck thread components.
   - How to call: DebuggerTool.find_deadlocks(pid=4512)

6. strace_process:
   - Purpose: Tracks background system calls, file descriptors, and kernel signals handled by an active Linux process.
   - Arguments:
     a) pid: int - Target system operational identifier reference.
     b) output: str (default: None) - Target location destination to write out compiled log arrays.
     c) duration: int (default: 10) - Timeout monitoring interval window quantified in seconds.
   - Returns: ToolResult outlining syscall summaries and returning recorded stream operations.
   - How to call: DebuggerTool.strace_process(pid=1024, duration=5)
   """)

    @staticmethod
    def run_python_with_pdb(script: str, args: list = None) -> ToolResult:
        try:
            cmd = [sys.executable, "-m", "pdb", script] + (args or [])
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=60,
                               input="c\nq\n")  # continue then quit
            out = (r.stdout + r.stderr).strip()
            return ToolResult(True, f"✓ pdb run completed\n{out[-1000:]}", out)
        except Exception as e:
            return ToolResult(False, f"✗ run_python_with_pdb failed: {e}")

    @staticmethod
    def analyze_traceback(traceback_text: str) -> ToolResult:
        try:
            lines = traceback_text.strip().splitlines()
            # Extract the exception type and message
            exc_line = next((l for l in reversed(lines) if ": " in l and not l.startswith(" ")), lines[-1] if lines else "")
            # Extract file references
            file_refs = []
            for line in lines:
                m = re.search(r'File "(.+?)", line (\d+), in (.+)', line)
                if m:
                    file_refs.append({"file": m.group(1), "line": int(m.group(2)), "in": m.group(3)})
            analysis = {
                "exception": exc_line,
                "traceback_frames": file_refs,
                "root_cause_file": file_refs[-1] if file_refs else None,
                "summary": f"Exception at {file_refs[-1]['file']}:{file_refs[-1]['line']} in {file_refs[-1]['in']}" if file_refs else exc_line
            }
            return ToolResult(True, f"✓ Traceback analyzed: {analysis['exception']}", analysis)
        except Exception as e:
            return ToolResult(False, f"✗ analyze_traceback failed: {e}")

    @staticmethod
    def profile_script(script: str, output: str = None) -> ToolResult:
        try:
            out_file = output or str(Path(tempfile.gettempdir()) / "profile_stats.prof")
            r = subprocess.run(
                [sys.executable, "-m", "cProfile", "-o", out_file, script],
                capture_output=True, text=True, timeout=120
            )
            # Read and display top stats
            import pstats, io
            stream = io.StringIO()
            ps = pstats.Stats(out_file, stream=stream)
            ps.sort_stats("cumulative")
            ps.print_stats(20)
            stats_text = stream.getvalue()
            return ToolResult(True, f"✓ Profile saved to {out_file}\n{stats_text[:2000]}", stats_text)
        except Exception as e:
            return ToolResult(False, f"✗ profile_script failed: {e}")

    @staticmethod
    def memory_profile(script: str) -> ToolResult:
        try:
            _ensure("memory-profiler", "memory_profiler")
            r = subprocess.run(
                [sys.executable, "-m", "memory_profiler", script],
                capture_output=True, text=True, timeout=120
            )
            out = (r.stdout + r.stderr).strip()
            return ToolResult(r.returncode == 0, out[-2000:] if out else "✓ No output", out)
        except Exception as e:
            return ToolResult(False, f"✗ memory_profile failed: {e}")

    @staticmethod
    def find_deadlocks(pid: int) -> ToolResult:
        try:
            import psutil
            proc = psutil.Process(pid)
            threads = proc.threads()
            # Check thread states and connections for signs of deadlock
            thread_info = [{"id": t.id, "user_time": t.user_time, "system_time": t.system_time}
                           for t in threads]
            connections = proc.connections()
            # Simple heuristic: threads with identical CPU times may be stuck
            stuck = [t for t in thread_info if t["user_time"] == 0 and t["system_time"] == 0]
            analysis = {
                "pid": pid,
                "total_threads": len(thread_info),
                "potentially_stuck_threads": len(stuck),
                "threads": thread_info,
                "open_connections": len(connections)
            }
            deadlock_suspected = len(stuck) > 1
            msg = f"⚠ Deadlock suspected ({len(stuck)} stuck threads)" if deadlock_suspected else f"✓ No obvious deadlock ({len(thread_info)} threads active)"
            return ToolResult(True, msg, analysis)
        except Exception as e:
            return ToolResult(False, f"✗ find_deadlocks failed: {e}")

    @staticmethod
    def strace_process(pid: int, output: str = None, duration: int = 10) -> ToolResult:
        try:
            if platform.system() != "Linux":
                return ToolResult(False, "✗ strace is Linux-only")
            if not shutil.which("strace"):
                return ToolResult(False, "✗ strace not installed. Run: sudo apt install strace")
            out_file = output or str(Path(tempfile.gettempdir()) / f"strace_{pid}.txt")
            r = subprocess.run(
                ["strace", "-p", str(pid), "-o", out_file, "-c"],
                capture_output=True, text=True, timeout=duration + 5,
                input=None
            )
            if Path(out_file).exists():
                content = Path(out_file).read_text()[:3000]
                return ToolResult(True, f"✓ strace output saved to {out_file}\n{content}", content)
            return ToolResult(False, "✗ strace produced no output")
        except subprocess.TimeoutExpired:
            # This is expected since we let it run for `duration` seconds
            if Path(output or "").exists() or Path(str(Path(tempfile.gettempdir()) / f"strace_{pid}.txt")).exists():
                out_file = output or str(Path(tempfile.gettempdir()) / f"strace_{pid}.txt")
                content = Path(out_file).read_text()[:3000] if Path(out_file).exists() else "No output"
                return ToolResult(True, f"✓ strace captured for {duration}s\n{content}", content)
            return ToolResult(True, f"✓ strace ran for {duration}s (output may be empty if process wasn't active)")
        except Exception as e:
            return ToolResult(False, f"✗ strace_process failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# Tool Registry
# ══════════════════════════════════════════════════════════════════════════════
DEVELOPER_TOOLS = {
    "git":             GitTool,
    "github":          GitHubTool,
    "gitlab":          GitLabTool,
    "docker":          DockerTool,
    "package_manager": PackageManagerTool,
    "vscode":          VSCodeTool,
    "terminal":        TerminalTool,
    "makefile":        MakefileTool,
    "cmake":           CMakeTool,
    "debugger":        DebuggerTool,
}

DEVELOPER_TOOLS_SUMMARY = "\n".join(
    f"- {k}: {v.description}" for k, v in DEVELOPER_TOOLS.items()
)

if __name__ == "__main__":
    print("NPM Agent — Developer CLI Tools loaded successfully.")
    print(f"{len(DEVELOPER_TOOLS)} tool classes available:")
    for name, cls in DEVELOPER_TOOLS.items():
        methods = [m for m in dir(cls) if not m.startswith("_")]
        print(f"  {name:20s} ({len(methods)} methods)")
