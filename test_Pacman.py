import pytest
import pygame
from Pacman import Pacman
from game_board import GameBoard
from ghost import Ghost

import main


@pytest.fixture
def board():
    return GameBoard()


@pytest.fixture
def Pacman():
    return Pacman(100, 100)

@pytest.fixture
def walls():
    return [
        pygame.Rect(0, 0, 20, 600),  # Left wall
        pygame.Rect(200, 200, 20, 20),  # Small obstacle
        pygame.Rect(780, 0, 20, 600),  # Right wall
    ]


@pytest.fixture
def ghost():
    return Ghost(100, 100, (255, 0, 0))


# PLAYER TESTS


def test_Pacman_movement_with_obstacles(Pacman, walls):
    # Step 1: Move Pacman towards an obstacle (left wall)
    Pacman.x = 25
    Pacman.y = 100
    Pacman.move("left", walls)
    assert Pacman.x == 25 # Should not move through the left wall

    # Step 2: Move Pacman towards an obstacle (small obstacle at (200, 200))
    Pacman.x = 190
    Pacman.y = 210
    Pacman.move("right", walls)
    assert Pacman.x == 190 # Should not move through the small obstacle

    # Step 3: Move Pacman towards the right wall (new right wall at x=780)
    Pacman.x = 780
    Pacman.y = 100
    Pacman.move("right", walls)
    # Assert that the Pacman's position hasn't changed, as they can't move past the wall
    assert Pacman.x ==  780 # Should not move beyond the right wall


# PACMAN TESTS
def test_Pacman_initialization(Pacman):
    assert Pacman.x == 100
    assert Pacman.y == 100
    assert Pacman.direction == "right"
    assert Pacman.speed == 2
    assert Pacman.radius == 10


def test_Pacman_movement_no_walls(Pacman):
    initial_x = Pacman.x
    initial_y = Pacman.y

    Pacman.move("right", [])
    assert Pacman.x == initial_x + Pacman.speed
    assert Pacman.y == initial_y
    assert Pacman.direction == "right"

    Pacman.move("left", [])
    assert Pacman.x == initial_x
    assert Pacman.y == initial_y
    assert Pacman.direction == "left"


def test_Pacman_wall_collision(Pacman, walls):
    # Move towards left wall
    Pacman.x = 25
    Pacman.y = 100
    Pacman.move("left", walls)
    assert Pacman.x == 25  # Should not move through wall

    # Move towards obstacle
    Pacman.x = 190
    Pacman.y = 210
    Pacman.move("right", walls)
    assert Pacman.x == 190  # Should not move through obstacle


# GAME BOARD TESTS


def test_board_initialization(board):
    assert board.width == 800
    assert board.height == 600


def test_board_outer_walls(board):
    assert len(board.walls) > 0
    outer_walls = board.walls[0:4]

    assert outer_walls[0].topleft == (0, 0)
    assert outer_walls[0].size == (board.width, 20)

    assert outer_walls[1].topleft == (0, 0)
    assert outer_walls[1].size == (20, board.height)

    assert outer_walls[2].topleft == (0, board.height - 20)
    assert outer_walls[2].size == (board.width, 20)

    assert outer_walls[3].topleft == (board.width - 20, 0)
    assert outer_walls[3].size == (20, board.height)


def test_board_inner_walls(board):
    assert len(board.walls) > 0
    inner_walls = board.walls[4:8]

    assert inner_walls[0].topleft == (100, 100)
    assert inner_walls[0].size == (20, 200)

    assert inner_walls[1].topleft == (300, 100)
    assert inner_walls[1].size == (200, 20)

    assert inner_walls[2].topleft == (600, 100)
    assert inner_walls[2].size == (20, 400)

    assert inner_walls[3].topleft == (300, 350)
    assert inner_walls[3].size == (200, 20)


def test_pellets_collide(board):
    assert len(board.pellets) > 0
    assert len(board.pellets) <= ((board.width - 80) / 40) * ((board.height - 80) / 40)

    for pellet in board.pellets:
        for wall in board.walls:
            assert wall.collidepoint(pellet.x, pellet.y) is False


def test_power_pellet_positions(board):
    assert len(board.power_pellets) == 4

    power_pellet_positions = [
        (50, 50),
        (board.width - 50, 50),
        (50, board.height - 50),
        (board.width - 50, board.height - 50),
    ]

    for pellet, position in zip(board.power_pellets, power_pellet_positions):
        assert pellet.x == position[0]
        assert pellet.y == position[1]

        for wall in board.walls:
            assert wall.collidepoint(pellet.x, pellet.y) is False


# GHOST TESTS


def test_ghost_init(ghost):
    assert ghost.x == 100
    assert ghost.y == 100
    assert ghost.speed == 1
    assert ghost.radius == 10
    assert ghost.scared is False


def test_ghost_collision_left_wall(ghost, player, walls):
    ghost.scared = True  # get rid of random value
    ghost.scared_timer = 10
    ghost.x = 25  # Close to left wall
    ghost.y = 100
    ghost.direction = "left"
    initial_x = ghost.x

    ghost.move(walls, player)

    # Should not move through left wall
    assert ghost.x in {initial_x or initial_x + ghost.speed}


def test_ghost_collision_with_top_wall(ghost, player, walls):
    ghost.scared = True  # get rid of random value
    ghost.scared_timer = 10
    ghost.x = 100
    ghost.y = 15
    ghost.direction = "up"
    initial_y = ghost.y - 1

    ghost.move(walls, player)

    # Should not move through top wall
    assert ghost.y == initial_y


def test_ghost_movement_no_walls(ghost, player):
    ghost.direction = "right"
    initial_x = ghost.x
    initial_y = ghost.y
    ghost.move([], player)
    assert ghost.x in {initial_x + ghost.speed, initial_x - ghost.speed, initial_x}
    assert ghost.y in {initial_y + ghost.speed, initial_y - ghost.speed, initial_y}
