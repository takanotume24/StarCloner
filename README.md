# StarCloner

# StarCloner

StarCloner is a tool that allows you to clone (and on subsequent runs, pull) GitHub repositories in various ways, including starred repositories, user-owned repositories, and organization-owned repositories.

## Documentation

The documentation for StarCloner is divided into several sections:

- [Installation and Setup](docs/installation.md)
- [Usage](docs/usage.md)
- [Features](docs/features.md)
- [Subcommands](docs/subcommands.md)

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
