# pycooltext-api

A Python wrapper for the [CoolText.com](https://cooltext.com) image generation API.
Build typed payloads, post to CoolText's `/PostChange` endpoint, and get back a
rendered image URL — all in a few lines of code.

## Installation

```bash
pip install pycooltext-api -U
```

## Quick Start

```python
from cooltext import CoolText, PostChangeConfigOptions

config = PostChangeConfigOptions(LogoID="732440996", Text="Hello World")
result = CoolText(config).create()

print(result)           # prints the image URL
result.download()       # saves the image locally
```

## Browse Available Logos

Visit **[https://thehritu.github.io/CoolText/](https://thehritu.github.io/CoolText/)** to browse
all available logo styles and their IDs.

## Configuration

`PostChangeConfigOptions` accepts these fields:

| Field                        | Type  | Default       | Description                   |
| ---------------------------- | ----- | ------------- | ----------------------------- |
| `LogoID`                     | `str` | required      | ID of the CoolText logo style |
| `Text`                       | `str` | `"Cool Text"` | Text to render                |
| `FontSize`                   | `str` | `"70"`        | Font size                     |
| `FileFormat`                 | `str` | `"PNG"`       | Output format                 |
| `BackgroundColor_color`      | `str` | `"FFFFFF"`    | Background colour (hex)       |
| `Color1_color`               | `str` | `None`        | Primary text colour           |
| `Color2_color`               | `str` | `None`        | Secondary colour              |
| `Boolean1`–`Boolean3`        | `str` | `None`        | Logo-specific toggles         |
| `Integer1`–`Integer14_color` | `str` | `None`        | Logo-specific numeric options |

### FileFormat options:

`FileFormat` accepts these values:

| Value | Format                                                             |
| ----- | ------------------------------------------------------------------ |
| `1`   | GIF with background color (if `BackgroundColor_color` is provided) |
| `2`   | GIF (Transparent)                                                  |
| `3`   | GIF (Transparent With No Dither)                                   |
| `4`   | JPG with background color (if `BackgroundColor_color` is provided) |
| `5`   | PNG with background color (if `BackgroundColor_color` is provided) |
| `6`   | PNG (Transparent)                                                  |

### Get default configuration values for a logo:

Returns a dictionary of all default values for the given logo id

```python
from cooltext import CoolText, PostChangeConfigOptions

config = PostChangeConfigOptions(LogoID="2975689126")
defaults = CoolText(config).get_defaults()
print(defaults)
```

## `CoolTextResult`

`CoolText.create()` returns a `CoolTextResult` object:

```python
result = CoolText(config).create()

str(result)                               # the image URL as a string
bool(result)                              # False if the request failed
result.download()                         # save to current directory
result.download("out.png")                # save to a specific path
result.download("out.png", stream=False)  # disable streaming
```

## Finding a Logo ID

Go to **[https://thehritu.github.io/CoolText/](https://thehritu.github.io/CoolText/)** — every
logo is listed with its ID and default configuration values.

## Search for logos by keyword:

Search for logos on cooltext.com by keyword:

```python
from cooltext import CoolTextSearch
results = CoolTextSearch().search("gold") # list of CoolTextSearchResult
for result in results:
    print(result.title, " - ", result.link)
    print(result.to_dict())  # get title and link as a dictionary
```

## `CoolTextSearchResult`

`CoolTextSearch.search()` returns a list of `CoolTextSearchResult` objects.

`CoolTextSearchResult` has these attributes:

- `title`: The logo's title (e.g. "Gold Text")
- `link`: The URL to the logo's page on CoolText.com

`CoolTextSearchResult` has these methods:

- `to_dict()`: Returns a dictionary with the title and link

```python
from cooltext.modules import CoolTextSearchResult

result = CoolTextSearchResult("Gold Text", "https://cooltext.com/Logo-ID/1234567890")
print(result.title)  # "Gold Text"
print(result.link)   # "https://cooltext.com/Logo-ID/1234567890"
print(result.to_dict())  # {"title": "Gold Text", "link": "https://cooltext.com/Logo-ID/1234567890"}
```

---

# CLI

First, install the extra dependency:

```bash
pip install rich
```

---

## Usage

**No arguments** — launches an interactive prompt:

```bash
cooltext
```

**Quick create** — just pass your text directly:

```bash
cooltext "Hello World"
```

**Pick a specific logo:**

```bash
cooltext "Hello World" --logo 732453157
```

**Save the image to a file:**

```bash
cooltext "Hello World" --save output.png
```

**Plain output** (just the URL, no colors — useful for scripting):

```bash
cooltext "Hello World" --as-text
```

---

## Search

Find logo styles by keyword:

```bash
cooltext search fire
cooltext search "neon" --limit 1
```

> **Add `--as-text` to get plain line-by-line output instead of a table.**

## On Some OS

On some operating systems, the CLI may not be available as `cooltext` immediately after installation. If you encounter a "command not found" error, try running it with Python:

```bash
python -m cooltext "Hello World"
```

---

## Links

- **GitHub:** [https://github.com/TheHritu/CoolText](https://github.com/TheHritu/CoolText)
- **Logo ID List:** [https://thehritu.github.io/CoolText/](https://thehritu.github.io/CoolText/)
- **PyPI:** [https://pypi.org/project/pycooltext-api/](https://pypi.org/project/pycooltext-api/)

## License

MIT © TheHritu
