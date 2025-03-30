# Clone Starred GitHub Repositories

This script clones (optionally filtered by star counts) all repositories starred by a specified GitHub user onto your local machine. If needed, you can provide a GitHub Personal Access Token via an environment variable (`GITHUB_TOKEN`) to help avoid API rate limits or access private repositories.

## Features

- **Fetch all repositories** starred by a given user.
- **Filter by star counts**:
  - `--min-stars`: Only include repositories with a star count greater than or equal to this value.
  - `--max-stars`: Only include repositories with a star count less than or equal to this value.
- **Dry-run mode** (`--dry-run`): Display which repositories would be cloned without actually cloning them.
- **GitHub token from an environment variable** (`GITHUB_TOKEN`) to help bypass rate limits or to access private repos (if your token has the necessary permissions).

## Requirements

- Python 3.x
- `requests` library  
  Install via:
  ```bash
  pip install requests
  ```

## Installation / Setup

1. Download or copy this script to any directory on your machine.
2. (Optional) Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install required libraries:
   ```bash
   pip install requests
   ```
4. (Optional) Grant execution permission to the script (on Unix-like systems):
   ```bash
   chmod +x clone_starred_repos.py
   ```

## Usage

```bash
./clone_starred_repos.py [OPTIONS] USERNAME
```
or, if you did not grant execution permission:
```bash
python3 clone_starred_repos.py [OPTIONS] USERNAME
```

### Specifying a Token via Environment Variable

To avoid GitHub API rate limits or to allow access to private repositories,  
you can set the `GITHUB_TOKEN` environment variable to a personal access token.  
For example, on Unix-like shells:
```bash
export GITHUB_TOKEN="your_token_here"
```
After setting the variable, run the script as usual.

### Options

- `USERNAME`  
  The GitHub username whose starred repositories you want to clone (e.g., `octocat`).

- `--dry-run, -n`  
  Preview the repositories to be cloned without actually cloning them.

- `--min-stars MIN_STARS`  
  Only process repositories with **at least** this many stars.

- `--max-stars MAX_STARS`  
  Only process repositories with **at most** this many stars.

## Examples

1. Clone all repositories starred by `octocat`:
   ```bash
   python3 clone_starred_repos.py octocat
   ```
2. Perform a dry run for repositories starred by `octocat`, but only those with at least 50 stars:
   ```bash
   python3 clone_starred_repos.py octocat --min-stars 50 --dry-run
   ```
   This will simply display the repositories without actually cloning them.
3. Use an environment variable `GITHUB_TOKEN` to clone:
   ```bash
   export GITHUB_TOKEN="your_token_here"
   python3 clone_starred_repos.py octocat --max-stars 1000
   ```
   Here, only repositories with **at most** 1000 stars will be cloned.

## How It Works

1. **Fetch starred repositories**  
   - The script accesses the GitHub API endpoint `https://api.github.com/users/<USERNAME>/starred`, retrieving all starred repositories (handling pagination as needed).
   - If the `GITHUB_TOKEN` environment variable is set, it uses that token in the Authorization header, which can help reduce the chances of hitting API rate limits. It can also give access to private repositories if the token has the proper scope/permissions.

2. **Filter by star count**  
   - Any repository that does not meet the criteria set by `--min-stars` or `--max-stars` is excluded.

3. **Sort and display**  
   - Repositories are sorted alphabetically by their `full_name` (e.g., `owner/repo`) and displayed to the user.

4. **Confirmation & cloning**  
   - The script shows the number of repositories to be processed and asks for confirmation.
   - If confirmed, each repository is cloned into a local directory named after the GitHub username (e.g., `octocat`).  
   - If `--dry-run` is specified, it only displays which repositories would be cloned and does not perform the actual cloning.

## Notes

- The script is released under the MIT License. You are free to modify and reuse it for your needs.
