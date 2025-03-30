# StarCloner

StarCloner lets you clone (and on subsequent runs, pull) GitHub repositories in three ways:

1. **Starred repositories** (`star` subcommand)  
   Clone/pull all repositories starred by a specified GitHub user.
2. **User-owned repositories** (`repo` subcommand)  
   Clone/pull all repositories owned by a specified GitHub user.
3. **Organization-owned repositories** (`org` subcommand)  
   Clone/pull all repositories owned by a specified GitHub organization.

By default, repositories are cloned (or pulled) into the current directory. If needed, you can provide a GitHub Personal Access Token (via `GITHUB_TOKEN`) to help avoid API rate limits or to access private repositories.

## Features

- **Clone starred repositories** (`star` subcommand)  
  - Filter by **minimum/maximum star count**.  
  - Filter by **owner** (only repos owned by a specific user).

- **Clone user-owned repositories** (`repo` subcommand)  
  - (Optional) Include **forked** repositories (`--include-forks`).  
  - (Optional) Include **archived** repositories (`--include-archived`).

- **Clone organization-owned repositories** (`org` subcommand)  
  - (Optional) Include **forked** repositories (`--include-forks`).  
  - (Optional) Include **archived** repositories (`--include-archived`).

- **Dry-run mode** (`--dry-run` or `-n`): Display which repositories would be processed without actually cloning/pulling them.

- **Skip confirmation** (`--yes` or `-y`): Automatically proceed without asking for user confirmation.

- **Specify a target directory** (`--output-dir` or `-o`): By default, StarCloner clones/pulls into the current directory.

- **Auto-pull if already cloned**: If a repository folder is already present locally, StarCloner will run `git pull` instead of cloning.

- **GitHub token from an environment variable** (`GITHUB_TOKEN`) to help bypass rate limits or to access private repos (if your token has the necessary permissions).

## Requirements

- Python 3.x
- `requests` library

## Installation / Setup

### Recommended: Using pipx

1. **Install pipx** (if not already installed):

   ```bash
   python3 -m pip install --user pipx
   python3 -m pipx ensurepath
   ```

2. **Install StarCloner using pipx**:

   ```bash
   pipx install /path/to/starcloner
   ```

   Replace `/path/to/starcloner` with the actual path to the `starcloner` directory.

### Alternative: Manual Setup

1. **Download or copy** the `starcloner.py` script to any directory on your machine.
2. (Optional) **Create and activate** a Python virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install required libraries**:

   ```bash
   pip install requests
   ```

4. (Optional) **Grant execution permission** to the script (on Unix-like systems):

   ```bash
   chmod +x starcloner.py
   ```

## Running Tests

To run the tests for StarCloner, you can use the `pytest` framework. Ensure you have `pytest` installed in your environment. If not, you can install it using pip:

```bash
pip install pytest
```

Once `pytest` is installed, you can run the tests by executing the following command in the root directory of the project:

```bash
pytest
```

This will automatically discover and run all the test files in the `tests` directory.


StarCloner has three subcommands:

- `star` — Clone/pull repositories starred by a GitHub user  
- `repo` — Clone/pull repositories owned by a GitHub user  
- `org` — Clone/pull repositories owned by a GitHub organization  

General syntax:

```bash
./starcloner.py <subcommand> [OPTIONS] ARG
```

or

```bash
python3 starcloner.py <subcommand> [OPTIONS] ARG
```

where `<subcommand>` is one of `star`, `repo`, or `org`, and `ARG` is either the username (for `star`/`repo`) or the organization name (for `org`).

---

### Subcommand: `star`
Clones (or pulls) repositories **starred** by a given user.  

**Command format**:
```bash
python3 starcloner.py star USERNAME [OPTIONS]
```

**Options**:

- **`USERNAME`** (required)  
  The GitHub username whose starred repositories you want to clone/pull (e.g., `octocat`).

- **`--min-stars MIN_STARS`**  
  Only process repositories with **at least** this many stars.

- **`--max-stars MAX_STARS`**  
  Only process repositories with **at most** this many stars.

- **`--owner-filter OWNER_FILTER`**  
  Only include repositories whose **owner name** matches this string (case-insensitive).

- **`--dry-run, -n`**  
  Preview the repositories to be cloned or pulled without actually doing it.

- **`--yes, -y`**  
  Skip the confirmation prompt and immediately proceed.

- **`--output-dir, -o OUTPUT_DIR`**  
  The directory where repositories will be cloned. Defaults to the current directory (`"."`).

---

### Subcommand: `repo`
Clones (or pulls) repositories **owned** by a given user.  

**Command format**:
```bash
python3 starcloner.py repo USERNAME [OPTIONS]
```

**Options**:

- **`USERNAME`** (required)  
  The GitHub username whose **owned** repositories you want to clone/pull.

- **`--include-forks`**  
  Include forked repositories (otherwise, forks are excluded by default).

- **`--include-archived`**  
  Include archived repositories (otherwise, archived repos are excluded by default).

- **`--dry-run, -n`**  
  Preview the repositories to be cloned or pulled without actually doing it.

- **`--yes, -y`**  
  Skip the confirmation prompt and immediately proceed.

- **`--output-dir, -o OUTPUT_DIR`**  
  The directory where repositories will be cloned. Defaults to the current directory.

---

### Subcommand: `org`
Clones (or pulls) repositories **owned** by a given organization.  

**Command format**:
```bash
python3 starcloner.py org ORGNAME [OPTIONS]
```

**Options**:

- **`ORGNAME`** (required)  
  The GitHub organization whose repositories you want to clone/pull.

- **`--include-forks`**  
  Include forked repositories (otherwise, forks are excluded by default).

- **`--include-archived`**  
  Include archived repositories (otherwise, archived repos are excluded by default).

- **`--dry-run, -n`**  
  Preview the repositories to be cloned or pulled without actually doing it.

- **`--yes, -y`**  
  Skip the confirmation prompt and immediately proceed.

- **`--output-dir, -o OUTPUT_DIR`**  
  The directory where repositories will be cloned. Defaults to the current directory.

---

### Specifying a Token via Environment Variable

To avoid GitHub API rate limits or to allow access to private repositories,  
you can set the `GITHUB_TOKEN` environment variable to a personal access token (PAT).

For example, on Unix-like shells:

```bash
export GITHUB_TOKEN="your_token_here"
```

After setting the variable, run StarCloner as usual. Make sure your token has the necessary scopes/permissions for private repositories if you intend to clone/pull them.

---

## Examples

### 1. Clone all repositories starred by `octocat`

```bash
python3 starcloner.py star octocat
```

### 2. Clone all repositories starred by `octocat` into a custom directory

```bash
python3 starcloner.py star octocat --output-dir /path/to/dir
```

### 3. Perform a dry run for repositories starred by `octocat`, limited to at least 50 stars

```bash
python3 starcloner.py star octocat --min-stars 50 --dry-run
```

### 4. Filter only repos owned by `torvalds` that `octocat` has starred

```bash
python3 starcloner.py star octocat --owner-filter torvalds
```

### 5. Clone all **user-owned** repos (default excludes forks & archived) by `octocat`

```bash
python3 starcloner.py repo octocat
```

### 6. Clone all user-owned repos by `octocat`, **including forks** and **archived** repos

```bash
python3 starcloner.py repo octocat --include-forks --include-archived
```

### 7. Clone all **organization-owned** repos for `github` (default excludes forks & archived)

```bash
python3 starcloner.py org github
```

### 8. Clone all organization-owned repos for `github`, **including forks** and **archived**

```bash
python3 starcloner.py org github --include-forks --include-archived
```

### 9. Combine multiple filters for starred repos

For example, repos with at least 100 stars **AND** owned by `microsoft`:

```bash
python3 starcloner.py star octocat --min-stars 100 --owner-filter microsoft
```

### 10. Clone/pull starred repos with an environment variable `GITHUB_TOKEN`

```bash
export GITHUB_TOKEN="your_token_here"
python3 starcloner.py star octocat --max-stars 1000
```

### 11. Skip confirmation

```bash
python3 starcloner.py star octocat --yes
```
*(Works similarly with the `repo` and `org` subcommands.)*

---

## How It Works

1. **Fetch repositories**  
   - For `star` subcommand, StarCloner uses the endpoint:  
     `https://api.github.com/users/<USERNAME>/starred`  
   - For `repo` subcommand, StarCloner uses:  
     `https://api.github.com/users/<USERNAME>/repos`  
   - For `org` subcommand, StarCloner uses:  
     `https://api.github.com/orgs/<ORGNAME>/repos`  
   - StarCloner handles pagination automatically (e.g., multiple pages of results).  
   - If `GITHUB_TOKEN` is set, StarCloner uses it in the `Authorization` header to help reduce the chance of hitting rate limits and to allow private repo access (if your token has the proper scopes).

2. **Filter & sort**  
   - For `star`, you can filter by `--min-stars`, `--max-stars`, and `--owner-filter`.  
   - For `repo` and `org`, you can exclude forks/archived repos by default, or include them via `--include-forks` / `--include-archived`.  
   - The final list is sorted alphabetically (`owner/repo`) and displayed to the user.

3. **Confirmation & clone/pull**  
   - StarCloner prints how many repositories will be processed and asks for confirmation unless you specify `--yes`.  
   - If a local directory already exists, StarCloner runs `git pull`; otherwise, it runs `git clone`.

4. **Directory structure**  
   - By default, repositories are cloned/pulled into the **current** directory.  
   - If `--output-dir /path/to/dir` is specified, they are cloned/pulled into that directory.
