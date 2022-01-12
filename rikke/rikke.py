from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.status import Spinner
from rich.tree import Tree
from time import sleep
from importlib import import_module

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description='Rikke')
    parser.add_argument('usernames', metavar='usernames', type=str, nargs='+',
                        help='Usernames to look up')

    args = parser.parse_args()

    toSearch = ["search.github", "search.dummy"]

    console = Console()

    libs = [import_module(search) for search in toSearch]

    current = 0

    def gentree(init):
        generated = Tree(init)
        index = 0
        for librar in libs:
            generated.add(('[green]' if index == current else '') + librar.name)
            index += 1
        return generated

    for user in args.usernames:
        info = {}
        spin = Spinner('point', style="green")
        with Live(refresh_per_second=20, transient=True) as live:
            table = Table.grid(padding=1)
            table.add_row(spin, "Searching for [red]" + user)
            for lib in libs:
                ret = None
                gen = lib.run(user)
                live.update(gentree(table))
                try:
                    while True:
                        next(gen)
                        live.update(gentree(table))
                except StopIteration as e:
                    ret = e.value
                
                info = {
                    **info,
                    **ret
                }
                current += 1

        t = Table("Data", "Value")

        for k, v in info.items():
            t.add_row(k, v)

        console.print(t)