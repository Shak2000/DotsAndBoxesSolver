# Dots and Boxes Solver

A complete implementation of the classic Dots and Boxes game with both a web interface and command-line version, featuring an AI opponent powered by the minimax algorithm with alpha-beta pruning.

## 🎮 Game Overview

Dots and Boxes is a paper-and-pencil game where players take turns drawing lines between dots to form boxes. When a player completes a box (all four sides), they score a point and get another turn. The player with the most boxes wins!

## ✨ Features

- **Web Interface**: Modern, responsive UI with smooth animations
- **Command Line Interface**: Terminal-based gameplay for classic experience
- **AI Opponent**: Intelligent computer player using minimax algorithm
- **Configurable Board Size**: Play on boards from 2x2 to 8x8
- **Move History**: Undo moves to explore different strategies
- **Real-time Updates**: Live score tracking and game state visualization
- **Multiple Difficulty Levels**: Adjustable AI search depth (1-6 levels)

## 🚀 Quick Start

### Web Interface

1. **Install Dependencies**
   ```bash
   pip install fastapi uvicorn
   ```

2. **Start the Server**
   ```bash
   uvicorn app:app --reload
   ```

3. **Open Your Browser**
   Navigate to `http://localhost:8000`

### Command Line Interface

```bash
python main.py
```

## 📁 Project Structure

```
dots-and-boxes-solver/
├── app.py              # FastAPI web server
├── main.py             # Core game logic and CLI interface
├── index.html          # Web interface HTML
├── styles.css          # Web interface styling
├── script.js           # Web interface JavaScript
└── README.md           # This file
```

## 🎯 How to Play

### Web Interface

1. **Setup**: Choose board dimensions (height and width)
2. **Start**: Click "New Game" to begin
3. **Make Moves**: Click on the gray lines to place them
4. **Score**: Complete boxes by drawing the fourth side
5. **Win**: Player with the most boxes when all lines are drawn wins

### Game Controls

- **New Game**: Start with custom board dimensions
- **Computer Move**: Let the AI make a move (adjustable difficulty)
- **Undo Move**: Take back the last move
- **Restart Game**: Reset with same board size
- **Quit Game**: Return to setup screen

### Command Line Interface

Follow the menu prompts to:
- Create new games with custom dimensions
- Make manual moves by specifying coordinates
- Request computer moves with custom search depth
- Undo moves and restart games

## 🤖 AI Features

The AI opponent uses a sophisticated minimax algorithm with:

- **Alpha-Beta Pruning**: Optimized search for better performance
- **Position Evaluation**: Smart scoring based on:
  - Completed squares (±10 points)
  - Squares ready to capture (±5 points penalty/bonus)
- **Configurable Depth**: Choose AI thinking depth (1-6 levels)
- **Strategic Play**: Considers both offensive and defensive moves

### Difficulty Levels

- **Depth 1-2**: Beginner (fast, basic strategy)
- **Depth 3-4**: Intermediate (balanced play)
- **Depth 5-6**: Expert (deep analysis, slower but stronger)

## 🛠️ Technical Details

### Backend (Python)

- **FastAPI**: Modern web framework for the API
- **Game Logic**: Complete dots and boxes implementation
- **AI Algorithm**: Minimax with alpha-beta pruning
- **Move Validation**: Comprehensive rule checking
- **State Management**: Full game state tracking and history

### Frontend (JavaScript/HTML/CSS)

- **Responsive Design**: Works on desktop and mobile
- **Real-time Updates**: Live game state synchronization
- **Interactive Board**: Click-to-play interface
- **Visual Feedback**: Smooth animations and hover effects
- **Modern Styling**: Clean, professional appearance

### API Endpoints

- `POST /create` - Create new game
- `POST /make_move` - Make a move
- `POST /switch` - Switch players
- `GET /game_state` - Get current state
- `GET /get_best_move` - Get AI move
- `POST /undo` - Undo last move

## 🎨 Customization

### Board Sizes

- Minimum: 2x2 (simple games)
- Maximum: 8x8 (complex games)
- Recommended: 3x3 to 5x5 for best experience

### AI Difficulty

Adjust the search depth in the web interface or when prompted in CLI:
- Higher depth = stronger play but slower response
- Lower depth = faster response but simpler strategy

## 🔧 Development

### Requirements

- Python 3.7+
- FastAPI
- Uvicorn (for web server)

### Running in Development

```bash
# Install dependencies
pip install fastapi uvicorn

# Start development server with auto-reload
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Or run CLI version
python main.py
```

### Code Structure

- **Game Class**: Core game logic in `main.py`
- **FastAPI Routes**: Web API in `app.py`
- **Frontend**: HTML/CSS/JS for web interface
- **Minimax AI**: Advanced algorithm for computer moves

## 🎲 Game Rules

1. Players alternate drawing lines between adjacent dots
2. When a player completes a box (all 4 sides), they:
   - Score 1 point
   - Get another turn
3. Game ends when all possible lines are drawn
4. Player with the most boxes wins
5. Ties are possible when players have equal boxes

## 🚨 Troubleshooting

### Common Issues

1. **Server won't start**: Check if port 8000 is available
2. **Moves not registering**: Ensure you're clicking on gray lines, not filled ones
3. **AI taking too long**: Reduce search depth for faster moves
4. **Board not displaying**: Check browser console for JavaScript errors

### Browser Compatibility

- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge

## 📈 Future Enhancements

Potential improvements:
- Online multiplayer support
- Tournament mode
- Move analysis and hints
- Game replay system
- Advanced AI personalities
- Sound effects and animations

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

---

Enjoy playing Dots and Boxes! 🎯
