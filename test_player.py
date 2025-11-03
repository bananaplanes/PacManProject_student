import pytest
import pygame
from player import Player


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
"""
from item import PowerPellet

@pytest.fixture
def pellet():
    return Pellet(100, 100)

@pytest.fixture
def powerPellet():
    return PowerPellet(100, 100)

def test_pellet_initialization(pellet):
    assert pellet.x == 100
    assert pellet.y == 100
    assert pellet.radius == 2
    assert pellet.collected == False

def test_powerPellet_initialization(powerPellet):
    assert powerPellet.x == 100
    assert powerPellet.y == 100
    assert powerPellet.radius == 8
    assert powerPellet.collected == False
"""

"""
from item import PowerPellet

@pytest.fixture
def pellet():
    return Pellet(100, 100)

@pytest.fixture
def powerPellet():
    return PowerPellet(100, 100)

def test_pellet_initialization(pellet):
    assert pellet.x == 100
    assert pellet.y == 100
    assert pellet.radius == 2
    assert pellet.collected == False

def test_powerPellet_initialization(powerPellet):
    assert powerPellet.x == 100
    assert powerPellet.y == 100
    assert powerPellet.radius == 8
    assert powerPellet.collected == False
"""
