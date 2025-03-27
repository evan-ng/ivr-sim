import networkx as nx
import matplotlib.pyplot as plt


class Menu:
    """
    This class represents a single menu, containing options to other menus
    """

    def __init__(self, start: bool, end: bool, label: str, next: list[int]):
        """
        :param start: boolean, starting point of the menu (should only be one)
        :param label: string, text describing the menu
        :param next:  array of idx, the menus that can be directly reached from the menu

        """
        self.start = start
        self.end = end
        self.label = label
        self.next = next.copy()


class MenuList:
    def __init__(self, menus: list[Menu]):
        """
        Create a list of IVR menus.

        :param list: an array of Menus
        """
        self.menus = menus
        self.start = list(m.start == True for m in menus).index(True)
        self.G = nx.DiGraph()

        self.G.add_nodes_from(range(len(menus)))
        for i, m in enumerate(menus):
            self.G.add_edges_from([(i, n) for n in m.next])

    def draw_menu_network(self, frustration: list[float] = [], show_menu_label=False):
        pos = hierarchy_pos_no_recur(
            self.G, self.start, yoffset=(0.04 if show_menu_label else 0.0)
        )
        for i, m in enumerate(self.menus):
            node_color = "white"
            if m.start:
                node_color = "blue"
            if m.end:
                node_color = "green"
            nx.draw_networkx_nodes(
                self.G,
                pos,
                nodelist=[i],
                node_color=node_color,
                edgecolors="black",
                node_size=(300 if show_menu_label else 600),
            )

        nx.draw_networkx_edges(self.G, pos, arrows=True, edge_color="black")
        labels = (
            dict([(i, m.label) for i, m in enumerate(self.menus)])
            if show_menu_label
            else dict(
                [(i, "{:0.1f}%".format(f * 100)) for i, f in enumerate(frustration)]
            )
        )
        nx.draw_networkx_labels(
            self.G,
            pos,
            labels=labels,
            font_color=("#000c" if show_menu_label else "black"),
            font_size=(6 if show_menu_label else 8),
        )

        # Set margins for the axes so that nodes aren't clipped
        plt.axis("off")
        plt.margins(0.2)
        plt.show()


def hierarchy_pos_no_recur(
    G, root, width=2.5, vert_gap=0.3, vert_loc=0, xcenter=0.5, yoffset=0.0
):
    """
    From https://stackoverflow.com/a/31685423
    If there is a cycle that is reachable from root, then result will not be a hierarchy.

    G: the graph
    root: the root node of current branch
    width: horizontal space allocated for this branch - avoids overlap with other branches
    vert_gap: gap between levels of hierarchy
    vert_loc: vertical location of root
    xcenter: horizontal location of root
    """

    def h_recur(
        G,
        root,
        width=width,
        vert_gap=vert_gap,
        vert_loc=vert_loc,
        xcenter=xcenter,
        yoffset=yoffset,
        pos=None,
        parent=None,
        parsed=[],
    ):
        if root not in parsed:
            parsed.append(root)
            if pos == None:
                pos = {root: (xcenter, vert_loc)}
            else:
                pos[root] = (xcenter, vert_loc)
            neighbors = list(G.neighbors(root))

            if parent != None and parent in neighbors:
                neighbors.remove(parent)
            if len(neighbors) > 0:
                dx = width / len(neighbors)
                nextx = xcenter - width / 2 - dx / 2
                for i, neighbor in enumerate(neighbors):
                    nextx += dx
                    pos = h_recur(
                        G,
                        neighbor,
                        width=dx,
                        vert_gap=vert_gap,
                        vert_loc=vert_loc - vert_gap - (i * yoffset),
                        xcenter=nextx,
                        yoffset=yoffset,
                        pos=pos,
                        parent=root,
                        parsed=parsed,
                    )
        return pos

    return h_recur(
        G,
        root,
        width=width,
        vert_gap=vert_gap,
        vert_loc=vert_loc,
        xcenter=xcenter,
        yoffset=yoffset,
    )
