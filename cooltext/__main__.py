from .logo_id import scrape_logos
from .modules import CoolText, PostChangeConfigOptions, CoolTextSearch
import argparse
import json

def generate(filename="logo_id.json"):
    data = scrape_logos()
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def main():
    parser = argparse.ArgumentParser(
        prog="cooltext"
        # TODO: add description
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--generate", action="store_true")
    group.add_argument("--cli", action="store_true") # TODO: rename --cli i think, and add help

    subparsers = parser.add_subparsers(dest="command")

    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("--logo_id", default="2975689126")
    create_parser.add_argument("--text", default="Hello World")
    create_parser.add_argument("--output")

    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("query")

    args = parser.parse_args()

    # genetaror
    if args.generate:
        generate()
        return

    # cli
    if args.cli:
        if args.command == "create":
            # create
            config = PostChangeConfigOptions(LogoID=args.logo_id, Text=args.text)
            result = CoolText(config).create()

            url = str(result)
            print(f"Image URL: {url}")

            if args.output:
                downloaded_file = result.download(args.output)
                if downloaded_file:
                    print(f"Downloaded to: {downloaded_file}")

        elif args.command == "search":
            # search
            search_results = CoolTextSearch().search(args.query)

            if search_results:
                for result in search_results:
                    print(f"Title: {result.title}")
                    print(f"Link: {result.link}")
                    print(f"Data: {result.to_dict()}")
                    print("-" * 20)

            print(f"Results found: {bool(search_results)}")
        else:
            parser.print_help()

if __name__ == "__main__":
    main()