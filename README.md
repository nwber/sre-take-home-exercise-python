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
uv run .\main.py <PATH_TO_YAML>

# Example
uv run .\main.py .\sample.yaml

# View application logs 
cat .\endpoint_health.log
```

## Changes

Created `requirements.txt`, `pyproject.toml`, `.python-version`, and `uv.lock` to easily manage and install required packages.

`yaml` and `requests` packages are missing because they don't exist in the standard library. They needed to be installed and added to `requirements.txt`.

Since `method` is an optional paramter, it needs to be set to GET as default if not present.

Added another split on the endpoint url to remove any port numbers.

Added latency check to the `check_health` function. Any response over 500ms fails.

Implented early returns for unsatisfactory response codes.

Set the timeout on the requests to 0.5s.

Adding logging to make this more "Production Ready".

Added examples of potential failure modes to the `sample.yaml` for testing.

Accounted for runtime when sleeping. While this is more accurate, it still does not account for cases where running all the requests takes longer than 15s. In this case, running the requests asynchronously would be a better solution. I tried to do this, but I haven't done anything with async Python before.
