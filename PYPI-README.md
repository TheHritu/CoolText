# pycooltext-api

A Python wrapper for the [CoolText.com](https://cooltext.com) image generation API.
Build typed payloads, post to CoolText's `/PostChange` endpoint, and get back a
rendered image URL — all in a few lines of code.

## Installation

```bash
pip install pycooltext-api
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

| Field | Type | Default | Description |
|---|---|---|---|
| `LogoID` | `str` | required | ID of the CoolText logo style |
| `Text` | `str` | `"Cool Text"` | Text to render |
| `FontSize` | `str` | `"70"` | Font size |
| `FileFormat` | `str` | `"PNG"` | Output format |
| `BackgroundColor_color` | `str` | `"FFFFFF"` | Background colour (hex) |
| `Color1_color` | `str` | `None` | Primary text colour |
| `Color2_color` | `str` | `None` | Secondary colour |
| `Boolean1`–`Boolean3` | `str` | `None` | Logo-specific toggles |
| `Integer1`–`Integer14_color` | `str` | `None` | Logo-specific numeric options |

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

## Links

- **GitHub:** [https://github.com/TheHritu/CoolText](https://github.com/TheHritu/CoolText)
- **Logo ID List:** [https://thehritu.github.io/CoolText/](https://thehritu.github.io/CoolText/)
- **PyPI:** [https://pypi.org/project/pycooltext-api/](https://pypi.org/project/pycooltext-api/)

## License

MIT © TheHritu