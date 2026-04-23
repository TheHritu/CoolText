from cooltext import CoolText, PostChangeConfigOptions, CoolTextSearch

config = PostChangeConfigOptions(LogoID="2975689126", Text="Hello World")
result = CoolText(config).create()
# The result object becomes the result url if used as a string.
url = str(result)
print(f"Image URL: {url}")

# And result object also supports download
downloaded_file = result.download("downloaded_sample.png")
if downloaded_file:
    print(f"Downloaded to: {downloaded_file}")

# Search example
search_results = CoolTextSearch().search(
    "gold"
)  # bool(search_results) is False if the query is empty or no results are found, otherwise a list of CoolTextSearchResult objects is returned (see README for details of CoolTextSearchResult).
# Print search results
for results in search_results:
    # Print title, link, and dictionary representation of each search result
    print(results.title)
    print(results.link)
    print(results.to_dict())

print(
    bool(search_results)
)  # True if search results are found, False if the query is empty or no results are found.
