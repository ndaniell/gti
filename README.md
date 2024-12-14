# Conway's Game of Life - Enhanced Edition

An enhanced implementation of Conway's Game of Life with visual features including color gradients, cell aging, and glow effects.

## Features

- Color gradients based on cell age
- Glow effects for live cells
- Grid wrapping
- Interactive controls
- Visual UI elements

## Requirements

- Python 3.x
- pygame
- numpy
- pytest (for testing)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/conways-game-of-life.git
   cd conways-game-of-life
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the game:
```bash
python conways_game_of_life.py
```

### Controls

- Space: Pause/Resume simulation
- R: Randomize grid
- Click: Toggle cell state
- ESC: Quit
- H: Toggle UI visibility

## Testing

Run tests using pytest:
```bash
pytest test_conways_game_of_life.py -v
```

## License

MIT License