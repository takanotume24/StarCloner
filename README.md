# StarCloner

StarCloner clones (and on subsequent runs, pulls) all repositories starred by a specified GitHub user onto your local machine. By default, it creates (or reuses) a subdirectory named after that user in the current directory. If needed, you can provide a GitHub Personal Access Token via an environment variable (`GITHUB_TOKEN`) to help avoid API rate limits or to access private repositories.

## Features

- **Fetch all repositories** starred by a given user.
- **Filter by star counts**:
  - `--min-stars`: Only include repositories with a star count greater than or equal to this value.
  - `--max-stars`: Only include repositories with a star count less than or equal to this value.
- **Dry-run mode** (`--dry-run`): Display which repositories would be processed without actually cloning/pulling them.
- **Skip confirmation** (`--yes`): Automatically proceed without asking for user confirmation.
- **Specify a parent directory** (`--output-dir` or `-o`): By default, StarCloner clones/pulls into a folder named after the GitHub username in your current working directory. Use `--output-dir` to specify a **different parent directory**, within which a subdirectory named after the GitHub username is created.
- **Auto pull if already cloned**: If a repository folder is already present locally, StarCloner will run `git pull` instead of cloning.
- **GitHub token from an environment variable** (`GITHUB_TOKEN`) to help bypass rate limits or to access private repos (if your token has the necessary permissions).

## Requirements

- Python 3.x
- `requests` library  
  Install via:
  ```bash
  pip install requests
  ```

## Installation / Setup

1. Download or copy the `starcloner.py` script to any directory on your machine.
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
   chmod +x starcloner.py
   ```

## Usage

```bash
./starcloner.py [OPTIONS] USERNAME
```
or, if you did not grant execution permission:
```bash
python3 starcloner.py [OPTIONS] USERNAME
```

### Specifying a Token via Environment Variable

To avoid GitHub API rate limits or to allow access to private repositories,  
you can set the `GITHUB_TOKEN` environment variable to a personal access token.  
For example, on Unix-like shells:
```bash
export GITHUB_TOKEN="your_token_here"
```
After setting the variable, run StarCloner as usual.

### Options

- `USERNAME`  
  The GitHub username whose starred repositories you want to clone/pull (e.g., `octocat`).

- `--dry-run, -n`  
  Preview the repositories to be cloned or pulled without actually doing it.

- `--yes, -y`  
  Skip the confirmation prompt and immediately proceed with the clone/pull operation.

- `--min-stars MIN_STARS`  
  Only process repositories with **at least** this many stars.

- `--max-stars MAX_STARS`  
  Only process repositories with **at most** this many stars.

- `--output-dir, -o OUTPUT_DIR`  
  The **parent directory** in which to create or reuse a subdirectory named after `USERNAME`.  
  Defaults to `"."` (the current directory).  
  For example, if `--output-dir /path/to/parent` is used and `USERNAME` is `octocat`,  
  then the repositories are cloned/pulled into `/path/to/parent/octocat/`.

## Examples

1. **Clone all starred repos by `octocat`**:
   ```bash
   python3 starcloner.py octocat
   ```
   - First run: Clones everything into a directory named `octocat/` in the current folder, with each repo in its own subfolder.
   - Subsequent runs: Performs `git pull` for each local repo if it already exists.

2. **Clone all starred repos by `octocat` into a custom parent directory**:
   ```bash
   python3 starcloner.py octocat --output-dir /path/to/parent
   ```
   - First run: Creates (if necessary) `/path/to/parent/octocat/` and clones all repos there.
   - Subsequent runs: Pulls updates in the same directory.

3. **Perform a dry run for repositories starred by `octocat`, limited to at least 50 stars**:
   ```bash
   python3 starcloner.py octocat --min-stars 50 --dry-run
   ```
   This will display which repositories would be cloned or pulled but will not actually clone or pull them.

4. **Clone/pull with an environment variable `GITHUB_TOKEN`**:
   ```bash
   export GITHUB_TOKEN="your_token_here"
   python3 starcloner.py octocat --max-stars 1000
   ```
   Here, only repositories with **at most** 1000 stars will be cloned or pulled. If they already exist locally, StarCloner will attempt a `git pull`.

5. **Skip confirmation**:
   ```bash
   python3 starcloner.py octocat --yes
   ```
   This will clone (or pull) immediately without asking to confirm.

## How It Works

1. **Fetch starred repositories**  
   - StarCloner accesses the GitHub API endpoint `https://api.github.com/users/<USERNAME>/starred`, retrieving all starred repositories (handling pagination as needed).
   - If the `GITHUB_TOKEN` environment variable is set, StarCloner uses that token in the Authorization header, which can help reduce the chances of hitting API rate limits and can allow access to private repositories if the token has the proper scope/permissions.

2. **Filter by star count**  
   - Any repository that does not meet the criteria set by `--min-stars` or `--max-stars` is excluded.

3. **Sort and display**  
   - Repositories are sorted alphabetically by their `full_name` (e.g., `owner/repo`) and displayed to the user.

4. **Confirmation & clone/pull**  
   - StarCloner shows how many repositories match your filters.
   - Unless the `--yes` option is used, StarCloner asks for confirmation before proceeding.
   - For each repository, if a local directory already exists, StarCloner runs `git pull`. Otherwise, it runs `git clone`.

5. **Directory structure (with `--output-dir`)**  
   - By default, StarCloner creates (or reuses) a subdirectory matching `USERNAME` under the current directory.
   - If you specify `--output-dir /path/to/parent` and `USERNAME` is `octocat`,  
     the final structure will be:
     ```
     /path/to/parent/
     └── octocat/
         ├── repo1
         ├── repo2
         ...
     ```

## Notes

- StarCloner is released under the MIT License. You are free to modify and reuse it for your needs.