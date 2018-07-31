#!/usr/bin/env python3


"""
Run some tests.
"""
import unittest
import gameLogic as Gl

"""
Grid tests.
"""


class TestGridWinningConditions(unittest.TestCase):

    def setUp(self):
        self.smallGrid = Gl.Grid(dimension=3)
        self.bigGrid = Gl.Grid(dimension=10)

        x_positions_small_grid = [(0, 0), (0, 1), (1, 0), (2, 1), (0, 2)]
        x_positions_big_grid = [(2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]

        o_positions_small_grid = [(1, 1), (1, 2), (2, 0), (2, 2)]

        for x in x_positions_small_grid:
            self.smallGrid.place_mark(x, "X")
        for o in o_positions_small_grid:
            self.smallGrid.place_mark(o, "O")
        for x in x_positions_big_grid:
            self.bigGrid.place_mark(x, "X")

    """
    XX-
    XOO
    OXO
    """
    def test_small_grid(self):
        self.assertTrue(self.smallGrid.test_coordinate_for_win((0, 2), "X", 3),
                        "Checking X win by move (0,2) in small grid fails! Game state:" +
                        "\n" + self.smallGrid.grid_to_string())
        self.assertFalse(self.smallGrid.test_coordinate_for_win((0, 2), "O", 3),
                         "Checking O cannot win by move (0,2) in small grid fails! Game state:" +
                         "\n" + self.smallGrid.grid_to_string())

    def test_big_grid(self):
        self.assertTrue(self.bigGrid.test_coordinate_for_win((2, 2), "X", 5),
                        "Checking X win by move (2,2) in big grid fails! Game state:" +
                        "\n" + self.bigGrid.grid_to_string())
        self.assertTrue(self.bigGrid.test_coordinate_for_win((7, 7), "X", 5),
                        "Checking X win by move (7,7) in big grid fails!" +
                        "\n" + self.bigGrid.grid_to_string())


def grid_suite():
    suite = unittest.TestSuite()
    suite.addTest(TestGridWinningConditions('test_small_grid'))
    suite.addTest(TestGridWinningConditions('test_big_grid'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(grid_suite())

