import numpy as np
import math

from menu_list import *


class MonteCarlo:
    def __init__(
        self, menu_list: MenuList, dropout_rate: float = None, num_iters: int = None
    ):
        """
        :param num_iters: int, number of simulated users
        :param label: string, text describing the menu
        :param next:  array of idx, the menus that can be directly reached from the menu
        """
        self.menu_list = menu_list
        self.num_iters = 100000 if num_iters == None else num_iters
        self.dropout_rate = 0.04 if dropout_rate == None else dropout_rate

    def run(self, breadth=True):
        num_end = 0
        num_frustrated = 0
        frustrated_menus = [0 for _ in self.menu_list.menus]

        for i in range(self.num_iters):
            curr_menu = self.menu_list.start
            # loop through the menus
            while True:
                # user made it to the end
                if self.menu_list.menus[curr_menu].end:
                    num_end += 1
                    break
                # no more menus to go to, but not end
                if len(self.menu_list.menus[curr_menu].next) == 0:
                    num_frustrated += 1
                    frustrated_menus[curr_menu] += 1
                    break

                # check how many menu options user has gone through
                next_menu_idx = np.random.choice(
                    range(len(self.menu_list.menus[curr_menu].next)), 1
                )[0]
                # adjust dropout rate with number of menu options
                dropout_rate = (
                    self.dropout_rate
                    if not breadth
                    else (
                        1.5 * self.dropout_rate * math.log(next_menu_idx + 1)
                        + 0.25 * self.dropout_rate
                    )
                )

                # run a dropout check
                is_frustrated = np.random.choice(
                    [False, True], 1, p=[1 - dropout_rate, dropout_rate]
                )[0]
                if is_frustrated:
                    num_frustrated += 1
                    frustrated_menus[curr_menu] += 1
                    break

                # randomly select next menu
                curr_menu = self.menu_list.menus[curr_menu].next[next_menu_idx]

        average_frustration = num_frustrated / self.num_iters

        return average_frustration, [f / self.num_iters for f in frustrated_menus]
