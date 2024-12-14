"""
Unit tests for Conway's Game of Life implementation.
Tests core game logic and helper functions.
"""

import pytest
import numpy as np
from conways_game_of_life import count_neighbors, generate_color_palette

def test_count_neighbors_empty():
    """Test neighbor counting with empty grid."""
    grid = np.zeros((3, 3))
    assert count_neighbors(grid, 1, 1) == 0

def test_count_neighbors_full():
    """Test neighbor counting with full grid."""
    grid = np.ones((3, 3))
    assert count_neighbors(grid, 1, 1) == 8

def test_count_neighbors_mixed():
    """Test neighbor counting with mixed pattern."""
    grid = np.array([
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1]
    ])
    assert count_neighbors(grid, 1, 1) == 4

def test_count_neighbors_edge():
    """Test neighbor counting at grid edge (wrapping)."""
    grid = np.array([
        [1, 0, 1],
        [0, 0, 0],
        [1, 0, 1]
    ])
    assert count_neighbors(grid, 0, 0) == 3

def test_generate_color_palette():
    """Test color palette generation."""
    n_colors = 10
    palette = generate_color_palette(n_colors)
    
    assert len(palette) == n_colors
    # Check if each color is valid RGB
    for color in palette:
        assert len(color) == 3
        assert all(0 <= c <= 255 for c in color)

def test_color_palette_uniqueness():
    """Test that generated colors are not all the same."""
    n_colors = 10
    palette = generate_color_palette(n_colors)
    unique_colors = set(tuple(color) for color in palette)
    assert len(unique_colors) > 1

@pytest.fixture
def sample_grid():
    """Fixture providing a sample grid for testing."""
    return np.array([
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0]
    ])

def test_blinker_pattern(sample_grid):
    """Test the classic blinker pattern oscillation."""
    # Initial state is vertical line
    assert np.array_equal(sample_grid[:, 1], [1, 1, 1])
    
    # After one update, should become horizontal line
    next_grid = sample_grid.copy()
    for i in range(3):
        for j in range(3):
            neighbors = count_neighbors(sample_grid, i, j)
            if sample_grid[i, j] == 1:
                next_grid[i, j] = 1 if 2 <= neighbors <= 3 else 0
            else:
                next_grid[i, j] = 1 if neighbors == 3 else 0
    
    assert np.array_equal(next_grid[1, :], [1, 1, 1])

def test_underpopulation():
    """Test that cells die from underpopulation."""
    grid = np.array([
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ])
    neighbors = count_neighbors(grid, 1, 1)
    assert neighbors < 2  # Should die in next generation

def test_overpopulation():
    """Test that cells die from overpopulation."""
    grid = np.array([
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ])
    neighbors = count_neighbors(grid, 1, 1)
    assert neighbors > 3  # Should die in next generation

def test_reproduction():
    """Test cell reproduction rule."""
    grid = np.array([
        [1, 1, 0],
        [1, 0, 0],
        [0, 0, 0]
    ])
    neighbors = count_neighbors(grid, 1, 1)
    assert neighbors == 3  # Should become alive in next generation

def test_survival():
    """Test cell survival rules."""
    grid = np.array([
        [1, 1, 0],
        [0, 1, 0],
        [0, 0, 0]
    ])
    neighbors = count_neighbors(grid, 1, 1)
    assert 2 <= neighbors <= 3  # Should survive to next generation

if __name__ == '__main__':
    pytest.main([__file__]) 