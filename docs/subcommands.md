## Subcommands

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

### Subcommand: `maintenance`
Perform maintenance tasks such as moving temporary files.

**Command format**:
```bash
python3 starcloner.py maintenance <maintenance_command> [OPTIONS]
```

**Maintenance Commands**:

- **`move-temp-files`**  
  Move temporary files to a designated directory.

**Options**:

- **`--dry-run, -n`**  
  Preview the files to be moved without actually doing it.

---

### Subcommand: `list-cloned`
List all cloned repositories in the specified directory.

**Command format**:
```bash
python3 starcloner.py list-cloned [OPTIONS]
```

**Options**:

- **`--output-dir, -o OUTPUT_DIR`**  
  The directory where repositories are cloned. Defaults to the current directory.
