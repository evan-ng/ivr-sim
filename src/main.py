import json
import argparse

from menu_list import *
from monte_carlo import *


def read_from_file(filename):
    """
    Create and return a list of menus
    """
    inputfile = open(filename, "r")
    data = json.load(inputfile)

    id_idx_map = dict()

    for i, m in enumerate(data["menus"]):
        id_idx_map[m["id"]] = i

    menus = []
    for m in data["menus"]:
        menus.append(
            Menu(
                m["start"] if "start" in m else False,
                m["end"] if "end" in m else False,
                m["label"],
                [id_idx_map[n] for n in m["next"]],
            )
        )

    menu_list = MenuList(menus)

    return menu_list


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input json file that contains the menus.",
    )
    parser.add_argument(
        "--breadth",
        type=bool,
        required=False,
        help="Account for breadth",
    )
    parser.add_argument(
        "--labels",
        type=bool,
        required=False,
        help="Show menu labels",
    )
    parser.add_argument(
        "--iter",
        type=int,
        required=False,
        help="Number of simulated users",
    )
    parser.add_argument(
        "--dropout",
        type=float,
        required=False,
        help="Dropout rate",
    )

    args = parser.parse_args()

    menu_file = args.inputfile
    menu_list = read_from_file(menu_file)

    sim = MonteCarlo(
        menu_list,
        dropout_rate=args.dropout,
        num_iters=args.iter,
    )
    if not args.labels:
        avg_frustration, menu_frustration = sim.run(breadth=args.breadth)
        print("Average Frustration: {:0.2f}%".format(avg_frustration * 100))

    menu_list.draw_menu_network(
        [] if args.labels else menu_frustration, show_menu_label=args.labels
    )
