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
