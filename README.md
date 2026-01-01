# CoolText

A small Python helper for generating images using CoolText's PostChange API. This repository wraps CoolText form options in a simple data model, posts the configuration to CoolText, and returns the rendered image URL.

# Example

- Result with logo id - ```4618063429```:

<img src='./results/sample.png' style="width:30%"></img>

- Result with logo id - ```8```:

<img src='./results/sample2.png' style="width:30%"></img>

- Result with logo id - ```2975689126```:

<img src='./results/sample3.png' style="width:30%"></img>

- Result with logo id - ```829964308```:

<img src='./results/sample4.png' style="width:30%"></img>

### <b>...And Many More Are Here...</b>

**Features**
- Build payloads using a typed `pydantic` model.
- Merge user-provided options with a logo's defaults from `logo-id.json`.
- Manage HTTP requests and return the final render URL.

## Requirements

- Python 3.10+
- See `requirements.txt` for exact package versions.

## Installation

Install dependencies with pip:

```bash
python -m pip install -r requirements.txt
```

If you prefer a virtual environment:

```bash
python -m venv .venv
.
\venv\Scripts\activate   # Windows
python -m pip install -r requirements.txt
```

## Quick Start

1. Ensure `logo-id.json` is present in the repository root. This file maps `LogoID` values to their CoolText page links and default form values. The repository includes a generated `logo-id.json` (see `logo-id.py` for the scraper used to produce it).
2. Edit `main.py` or create your own script using the library.

Example minimal usage (same logic as in `main.py`):

```python
from modules import CoolText, PostChangeConfigOptions

config = PostChangeConfigOptions(LogoID="732440996", Text="Hello World")
print(CoolText(config).create())
```

Running the example:

```bash
python main.py
```

The script will print a URL where the rendered image can be downloaded.

## Configuration and API details

- `PostChangeConfigOptions` (defined in `modules.py`) exposes the familiar CoolText form fields: `LogoID`, `Text`, `FontSize`, `FileFormat`, `BackgroundColor_color`, and many optional color/boolean/integer fields. The model uses sensible defaults from `constants.DefaultValues` when values are not provided.
- `CoolText.create()` workflow:
  - Loads the logo metadata and defaults from `logo-id.json`.
  - Fetches the CoolText logo page (to satisfy referer/session expectations).
  - Posts the combined payload to CoolText's `/PostChange` endpoint.
  - Parses and returns the render URL from the JSON response.

If the request fails or a response cannot be parsed, `create()` returns `None` and logs a message via the `logging` module.

## How to find a LogoID

Just hop on to https://cool-text-thehritu.vercel.app for list of logos and their ids and other configs.

## Development

- Run the example locally (`python main.py`).
- Add or modify `PostChangeConfigOptions` in `modules.py` if you need to support additional CoolText parameters.
- Logging is used for error and debug messages; enable or configure the `logging` module in your own scripts as needed.

## Files
- [main.py](main.py)
- [modules.py](modules.py)
- [constants.py](constants.py)
- [logo-id.json](logo-id.json)
- [logo-id.py](logo-id.py)
- [requirements.txt](requirements.txt)

## Contributing

Contributions are welcome. Open an issue or submit a pull request with a clear description of the change.

## License

This project does not include an explicit license file. Add a `LICENSE` if you wish to define reuse terms.
