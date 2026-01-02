from modules import CoolText, PostChangeConfigOptions

config = PostChangeConfigOptions(LogoID="2975689126", Text="Hello World")
result = CoolText(config).create()
# The result object becomes the result url if used as a string.
url = str(result)
print(f"Image URL: {url}")

# And result object also supports download
downloaded_file = result.download("downloaded_sample.png")
if downloaded_file:
    print(f"Downloaded to: {downloaded_file}")
