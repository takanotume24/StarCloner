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
