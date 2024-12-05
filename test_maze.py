import unittest
from maze import Maze
from board import Board  # Assuming Board is another class that is part of your code

class TestMazeGeneration(unittest.TestCase):

    def setUp(self):
        # Setup a simple 10x10 board for testing
        self.board = Board(10, 10)
        self.maze = Maze(self.board)

    def test_get_frontiers_edge_cases(self):
        self.board.start = (0, 0)
        self.board.target = (9, 9)
        self.maze.initialize()
        frontiers = self.maze.get_frontiers(self.board.start)
        self.assertEqual(frontiers, {(0, 2), (2, 0)})

    def test_initialize_without_start_target(self):
        with self.assertRaises(ValueError):
            self.maze.initialize()

    def test_no_passages_created(self):
        self.board.start = (0, 0)
        self.board.target = (0, 0)
        self.maze.initialize()
        self.maze.generate()
        self.assertEqual(len(self.maze.passages), 0)

    def test_large_maze_generation(self):
        self.board = Board(100, 100)  # Large grid
        self.board.start = (0, 0)
        self.board.target = (99, 99)
        self.maze.initialize()
        self.maze.generate()
        self.assertGreater(len(self.maze.passages), 0)

    def test_frontiers_updated_after_generation(self):
        initial_frontiers = len(self.maze.board.frontiers)
        self.maze.generate()
        self.assertLess(len(self.maze.board.frontiers), initial_frontiers)

    def test_wall_and_passages_are_separated(self):
        self.assertTrue(self.maze.board.wall.isdisjoint(self.maze.passages))

    def test_generate_randomized(self):
        maze_1 = self.maze.generate()
        maze_2 = self.maze.generate()
        self.assertNotEqual(maze_1.passages, maze_2.passages)

    def test_multiple_passages_in_maze(self):
        self.assertGreater(len(self.maze.passages), 10)

    def test_start_target_opposite_corners(self):
        self.board.start = (0, 0)
        self.board.target = (9, 9)
        self.maze.initialize()
        self.maze.generate()
        self.assertGreater(len(self.maze.passages), 0)

if _name_ == "_main_":
    unittest.main()