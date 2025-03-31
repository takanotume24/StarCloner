## Usage

StarCloner has five subcommands:

- `star` — Clone/pull repositories starred by a GitHub user  
- `repo` — Clone/pull repositories owned by a GitHub user  
- `org` — Clone/pull repositories owned by a GitHub organization  
- `maintenance` — Perform maintenance tasks  
- `list-cloned` — List all cloned repositories in a specified directory  

General syntax for the main subcommands:

```bash
./starcloner.py <subcommand> [OPTIONS] ARG
```

or

```bash
python3 starcloner.py <subcommand> [OPTIONS] ARG
```

where `<subcommand>` is one of `star`, `repo`, or `org`, and `ARG` is either the username (for `star`/`repo`) or the organization name (for `org`).

### Examples

1. Clone all repositories starred by `octocat`

   ```bash
   python3 starcloner.py star octocat
   ```

2. Clone all repositories starred by `octocat` into a custom directory

   ```bash
   python3 starcloner.py star octocat --output-dir /path/to/dir
   ```

3. Perform a dry run for repositories starred by `octocat`, limited to at least 50 stars

   ```bash
   python3 starcloner.py star octocat --min-stars 50 --dry-run
   ```

4. Filter only repos owned by `torvalds` that `octocat` has starred

   ```bash
   python3 starcloner.py star octocat --owner-filter torvalds
   ```

5. Clone all **user-owned** repos (default excludes forks & archived) by `octocat`

   ```bash
   python3 starcloner.py repo octocat
   ```

6. Clone all user-owned repos by `octocat`, **including forks** and **archived** repos

   ```bash
   python3 starcloner.py repo octocat --include-forks --include-archived
   ```

7. Clone all **organization-owned** repos for `github` (default excludes forks & archived)

   ```bash
   python3 starcloner.py org github
   ```

8. Clone all organization-owned repos for `github`, **including forks** and **archived**

   ```bash
   python3 starcloner.py org github --include-forks --include-archived
   ```

9. Combine multiple filters for starred repos

   For example, repos with at least 100 stars **AND** owned by `microsoft`:

   ```bash
   python3 starcloner.py star octocat --min-stars 100 --owner-filter microsoft
   ```

10. Clone/pull starred repos with an environment variable `GITHUB_TOKEN`

    ```bash
    export GITHUB_TOKEN="your_token_here"
    python3 starcloner.py star octocat --max-stars 1000
    ```

11. Skip confirmation

    ```bash
    python3 starcloner.py star octocat --yes
    ```
    *(Works similarly with the `repo` and `org` subcommands.)*
