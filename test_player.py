import pytest
import pygame
from player import Player
from game_board import GameBoard

@pytest.fixture
def board():
    return GameBoard()

@pytest.fixture
def player():
    return Player(100, 100)

@pytest.fixture
def walls():
    return [
        pygame.Rect(0, 0, 20, 600),  # Left wall
        pygame.Rect(200, 200, 20, 20),  # Small obstacle
        pygame.Rect(780, 0, 20, 600),  # Right wall
    ]

"""
UNCOMMENT and FILL THIS IN

def test_player_movement_with_obstacles(player, walls):
    # Step 1: Move player towards an obstacle (left wall)
    player.x = 25
    player.y = 100
    player.move("left", walls)
    assert player.x ==  # Should not move through the left wall

    # Step 2: Move player towards an obstacle (small obstacle at (200, 200))
    player.x = 190
    player.y = 210
    player.move("right", walls)
    assert player.x ==  # Should not move through the small obstacle

    # Step 3: Move player towards the right wall (new right wall at x=780)
    player.x = 780
    player.y = 100
    player.move("right", walls)
    # Assert that the player's position hasn't changed, as they can't move past the wall
    assert player.x ==   # Should not move beyond the right wall
"""

# PLAYER TESTS
def test_player_initialization(player):
    assert player.x == 100
    assert player.y == 100
    assert player.direction == "right"
    assert player.speed == 2
    assert player.radius == 10


def test_player_movement_no_walls(player):
    initial_x = player.x
    initial_y = player.y

    player.move("right", [])
    assert player.x == initial_x + player.speed
    assert player.y == initial_y
    assert player.direction == "right"

    player.move("left", [])
    assert player.x == initial_x
    assert player.y == initial_y
    assert player.direction == "left"


def test_player_wall_collision(player, walls):
    # Move towards left wall
    player.x = 25
    player.y = 100
    player.move("left", walls)
    assert player.x == 25  # Should not move through wall

    # Move towards obstacle
    player.x = 190
    player.y = 210
    player.move("right", walls)
    assert player.x == 190  # Should not move through obstacle


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
            assert wall.collidepoint(pellet.x, pellet.y) == False

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
            assert wall.collidepoint(pellet.x, pellet.y) == False