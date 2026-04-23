# CoolText

###### I hope a STAR ⭐ from you 😊.

A Python wrapper for the [CoolText.com](https://cooltext.com) image generation API.
Build typed payloads, post to CoolText's `/PostChange` endpoint, and get back a
rendered image URL — all in a few lines of code.

[![Version](https://img.shields.io/badge/Version-0.1.3-red)](https://pypi.org/project/pycooltext-api/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

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

## Logo Previews

Browse all logos at **[https://thehritu.github.io/CoolText/](https://thehritu.github.io/CoolText/)**.
Here are a few examples:

| Logo ID | Preview |
|---|---|
| `4618063429` | ![](./results/sample.png) |
| `8` | ![](./results/sample2.png) |
| `2975689126` | ![](./results/sample3.png) |
| `829964308` | ![](./results/sample4.png) |
| `732453157` | ![](./results/sample5.png) |
| `1779834160` | ![](./results/sample6.png) |

...and many more on the [logo id list](https://thehritu.github.io/CoolText/).

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

If anything fails, `create()` returns a falsy `CoolTextResult` and logs the error.

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

## Coffee is love, coffee is life.

<a href="https://www.buymeacoffee.com/hritu" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-yellow.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;" ></a>

## Contributing

Contributions are welcome — open an issue or submit a pull request.

## License

MIT © TheHritu
