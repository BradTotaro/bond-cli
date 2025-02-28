from .base_command import BaseCommand
import bond.database
from bond.cli.table import Table


class ListCommand(BaseCommand):
    subcmd = "list"
    help = "List Bonds in local database."

    def run(self, args):
        table = Table(["bondid", "ip", "token"])
        bonds = bond.database.get_bonds()
        for bondid in bonds.keys():
            b = bonds[bondid]
            table.add_row(
                {
                    "bondid": bondid,
                    "ip": b["ip"] if "ip" in b else None,
                    "token": b["token"] if "token" in b else None,
                }
            )


def register():
    ListCommand()
