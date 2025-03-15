# Fetch SRE python exercise

## Setup

### Requirements

Python 3.13
[uv](https://docs.astral.sh/uv/getting-started/installation/)

```powershell
# Install latest UV release
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Use UV to install Python 3.13
uv python install 3.13
```

### Windows

Activate the virtual environment

```powershell
uv venv
.\.venv\Scripts\activate.ps1
```

Install packages

```powershell
uv pip install -r .\requirements.txt
```

## Running the application

```powershell
uv run main.py <PATH_TO_YAML>
```

## Changes

Created `requirements.txt`, `pyproject.toml`, `.python-version`, and `uv.lock` to easily manage and install required packages.

`yaml` and `requests` packages are missing because they don't exist in the standard library. They needed to be installed and added to `requirements.txt`.

Since `method` is an optional paramter, it needs to be set to GET as default if not present.

Added another split on the endpoint url to remove any port numbers.

Added latency check to the `check_health` function. Any response over 500ms fails.

Implented early returns for unsatisfactory responses.

As you add more endpoints, the requests can add up and could potentially take more than 15 seconds. To resolve this, I modified the request to be done asynchronously.
