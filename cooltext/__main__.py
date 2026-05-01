from __future__ import annotations

import sys
import argparse
from typing import Optional

try:
    from rich.rule import Rule
    from rich.panel import Panel
    from rich.table import Table
    from rich.console import Console
    from rich.prompt import Prompt, Confirm
except ImportError:
    print("error: 'rich' is required — run: pip install rich", file=sys.stderr)
    sys.exit(1)

# // KEEPING ALL TEXTS AND VRIABLES IN SINGLE FILE COZ I DONT WANT TO DEAL WITH IMPORTS IN A CLI TOOL, ESPECIALLY WITH THE INTERACTIVE FLOW. ALSO THIS FILE IS NOT TOO BIG ANYWAY.

from .modules import CoolText, PostChangeConfigOptions, CoolTextSearch

console = Console()
DEFAULT_LOGO_ID = "2975689126"


def create_image(text: str, logo_id: str, output: Optional[str], plain: bool) -> None:
    if not plain:
        with console.status("Generating...", spinner="dots"):
            result = CoolText(
                PostChangeConfigOptions(LogoID=logo_id, Text=text)
            ).create()
    else:
        result = CoolText(PostChangeConfigOptions(LogoID=logo_id, Text=text)).create()

    if result is None:
        msg = "Failed to generate image. Double-check the logo ID."
        if plain:
            print(f"error: {msg}", file=sys.stderr)
        else:
            console.print(f"[red]✗[/red] {msg}")
        sys.exit(1)

    url = str(result)

    if output:
        if not plain:
            with console.status(f"Downloading to {output}...", spinner="dots"):
                saved = result.download(output)
        else:
            saved = result.download(output)

        if not saved and not plain:
            console.print("[yellow]⚠ Download failed — URL is still valid.[/yellow]")

    if plain:
        # just print the URL, nothing else
        print(url)
        if output and saved:
            print(saved)
    else:
        body = f"[bold cyan]{url}[/bold cyan]"
        if output and saved:
            body += f"\n\n[green]Saved →[/green] {saved}"
        console.print(Panel(body, title="[green]✓ Done[/green]", expand=False))


def search_logos(query: str, limit: int, plain: bool) -> None:
    if not plain:
        with console.status(f"Searching for '{query}'...", spinner="dots"):
            results = CoolTextSearch().search(query)
    else:
        results = CoolTextSearch().search(query)

    if not results:
        msg = f"No results for '{query}'."
        print(msg) if plain else console.print(f"[yellow]{msg}[/yellow]")
        return

    shown = results[:limit] if limit else results

    if plain:
        for r in shown:
            print(f"{r.title}  {r.link}")
        return

    table = Table(title=f"Results for '{query}'", show_lines=True)
    table.add_column("#", style="dim", width=4)
    table.add_column("Title", style="bold white")
    table.add_column("Link", style="cyan")

    for i, r in enumerate(shown, 1):
        table.add_row(str(i), r.title, r.link)

    console.print(table)

    if limit and len(results) > limit:
        console.print(
            f"[dim]{len(results) - limit} more — increase --limit to see them.[/dim]"
        )


def search_and_pick_logo() -> str:
    # used inside the interactive flow to let the user find a logo by keyword
    query = Prompt.ask("   Search keyword (e.g. fire, neon, glitter)")

    with console.status("   Searching...", spinner="dots"):
        results = CoolTextSearch().search(query)

    if not results:
        console.print("   [yellow]No results — keeping default logo.[/yellow]")
        return DEFAULT_LOGO_ID

    table = Table(show_lines=True)
    table.add_column("#", style="dim", width=4)
    table.add_column("Title", style="bold white")
    table.add_column("Logo ID", style="cyan")

    for i, r in enumerate(results[:10], 1):
        d = r.to_dict()
        lid = str(d.get("logo_id", d.get("id", "?")))
        table.add_row(str(i), r.title, lid)

    console.print(table)

    choice = Prompt.ask("   Pick a number (or Enter to skip)", default="")
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < min(10, len(results)):
            d = results[idx].to_dict()
            lid = str(d.get("logo_id", d.get("id", DEFAULT_LOGO_ID)))
            if lid != "?":
                return lid

    console.print("   [dim]Keeping default logo.[/dim]")
    return DEFAULT_LOGO_ID


def run_interactive() -> None:
    # runs when the user calls `cooltext` with no arguments
    console.print()
    console.print(
        Panel(
            "[bold cyan]CoolText[/bold cyan] — styled text images\n"
            "[dim]Answer a few questions and we'll generate your image.[/dim]",
            expand=False,
        )
    )
    console.print()

    text = Prompt.ask("[bold]1.[/bold] Your text", default="Hello World")

    console.print()
    logo_id = DEFAULT_LOGO_ID
    logo_choice = Prompt.ask(
        "[bold]2.[/bold] Logo style",
        choices=["search", "enter id", "default"],
        default="default",
    )

    if logo_choice == "search":
        logo_id = search_and_pick_logo()
    elif logo_choice == "enter id":
        logo_id = (
            Prompt.ask(
                f"   Logo ID (default: {DEFAULT_LOGO_ID})", default=DEFAULT_LOGO_ID
            ).strip()
            or DEFAULT_LOGO_ID
        )

    console.print()
    want_save = Confirm.ask("[bold]3.[/bold] Download to a file?", default=False)
    output_path = None
    if want_save:
        output_path = Prompt.ask("   Save as", default="cooltext_output.gif")

    console.print()
    console.print(Rule("[dim]Generating[/dim]"))
    create_image(text, logo_id, output_path, plain=False)


# separate parsers per command to avoid argparse mixing positionals with subcommands
def make_create_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="cooltext", description="Generate a styled text image."
    )
    p.add_argument("text", metavar="TEXT")
    p.add_argument("--logo", dest="logo_id", default=DEFAULT_LOGO_ID, metavar="ID")
    p.add_argument("--save", dest="output", metavar="FILE")
    p.add_argument(
        "--as-text", action="store_true", help="print plain URL, no formatting"
    )
    return p


def make_search_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="cooltext search")
    p.add_argument("query", metavar="QUERY")
    p.add_argument("--limit", type=int, default=0, metavar="N")
    p.add_argument(
        "--as-text", action="store_true", help="print plain results, no formatting"
    )
    return p


def print_help() -> None:
    console.print(
        Panel(
            "[bold]cooltext[/bold] — styled text images via CoolText.com\n\n"
            "  [cyan]cooltext[/cyan]                        interactive mode\n"
            '  [cyan]cooltext[/cyan] [green]"Hello World"[/green]           create with default logo\n'
            '  [cyan]cooltext[/cyan] [green]"Hi"[/green] [yellow]--logo[/yellow] [magenta]732453157[/magenta]     specific logo\n'
            '  [cyan]cooltext[/cyan] [green]"Hi"[/green] [yellow]--save[/yellow] [magenta]logo.gif[/magenta]      save to file\n'
            '  [cyan]cooltext[/cyan] [green]"Hi"[/green] [yellow]--as-text[/yellow]             plain URL output\n'
            "  [cyan]cooltext[/cyan] [green]search[/green] [magenta]fire[/magenta]              find logos by keyword\n",
            title="Usage",
            expand=False,
        )
    )


def main() -> None:
    argv = sys.argv[1:]

    if not argv:
        run_interactive()
        return

    if argv[0] in ("-h", "--help"):
        print_help()
        return

    if argv[0] == "search":
        args = make_search_parser().parse_args(argv[1:])
        search_logos(args.query, limit=args.limit, plain=args.as_text)
        return

    # default: treat everything as a create command
    args = make_create_parser().parse_args(argv)
    create_image(args.text, args.logo_id, args.output, plain=args.as_text)


if __name__ == "__main__":
    main()
