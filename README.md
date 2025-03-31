# ACM 

## Installation

### 1. Install `uv` (high-speed Python package manager)
Run this command to install `uv`:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Install dependencies
```bash
uv sync
```
## Run the application
```bash
uv run acm -- ~/testfile.txt 
```