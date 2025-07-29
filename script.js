class DotsAndBoxesUI {
    constructor() {
        this.gameState = {
            height: 4,
            width: 4,
            currentPlayer: 'A',
            scoreA: 0,
            scoreB: 0,
            remainingMoves: 0,
            winner: null,
            gameActive: false
        };
        
        this.boardElements = {
            vertical: [],
            horizontal: [],
            squares: []
        };
        
        this.initializeEventListeners();
        this.showSetupOnly();
    }

    async apiCall(endpoint, method = 'GET', data = null) {
        try {
            const url = new URL(endpoint, window.location.origin);
            if (data && method === 'GET') {
                Object.keys(data).forEach(key => url.searchParams.append(key, data[key]));
            }

            const options = {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                }
            };

            if (data && method === 'POST') {
                options.body = JSON.stringify(data);
                console.log('POST request body:', options.body);
            }

            console.log('Making API call:', method, url.toString());
            const response = await fetch(url, options);
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error('HTTP error response:', errorText);
                throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
            }
            
            const result = await response.json();
            console.log('API response:', result);
            return result;
        } catch (error) {
            console.error('API call failed:', error);
            this.showStatus('Error: ' + error.message, 'error');
            throw error;
        }
    }

    async createNewGame() {
        const heightEl = document.getElementById('height');
        const widthEl = document.getElementById('width');
        
        if (!heightEl || !widthEl) {
            this.showStatus('Game setup elements not found', 'error');
            return;
        }
        
        const height = parseInt(heightEl.value);
        const width = parseInt(widthEl.value);
        
        if (height < 2 || width < 2) {
            this.showStatus('Board dimensions must be at least 2x2', 'error');
            return;
        }

        try {
            console.log('Creating game with dimensions:', height, width);
            const result = await this.apiCall('/create', 'POST', { height, width });
            console.log('Create game result:', result);
            
            this.gameState.height = height;
            this.gameState.width = width;
            this.gameState.currentPlayer = 'A';
            this.gameState.scoreA = 0;
            this.gameState.scoreB = 0;
            this.gameState.winner = null;
            this.gameState.gameActive = true;
            
            console.log('Generating board...');
            this.generateBoard();
            console.log('Board generated, updating game state...');
            await this.updateGameState();
            console.log('Game state updated, showing UI...');
            this.showGameUI();
            this.showStatus('New game created!', 'success');
        } catch (error) {
            console.error('Create game error:', error);
            this.showStatus('Failed to create new game: ' + error.message, 'error');
        }
    }

    generateBoard() {
        const gameBoard = document.getElementById('gameBoard');
        if (!gameBoard) return;
        
        gameBoard.innerHTML = '';
        
        const boardContainer = document.createElement('div');
        boardContainer.className = 'board-container';
        
        this.boardElements.vertical = [];
        this.boardElements.horizontal = [];
        this.boardElements.squares = [];
        
        // Generate board rows - alternating pattern
        console.log('Generating board with dimensions:', this.gameState.height, 'x', this.gameState.width);
        
        for (let y = 0; y < this.gameState.height; y++) {
            // Row with dots and horizontal lines
            const dotRow = document.createElement('div');
            dotRow.className = 'board-row dot-row';
            
            for (let x = 0; x < this.gameState.width; x++) {
                // Add dot
                const dot = document.createElement('div');
                dot.className = 'dot';
                dotRow.appendChild(dot);
                
                // Add horizontal line (except for last column)
                if (x < this.gameState.width - 1) {
                    const hLine = document.createElement('div');
                    hLine.className = 'horizontal-line';
                    hLine.dataset.x = x;
                    hLine.dataset.y = y;
                    hLine.addEventListener('click', (e) => {
                        console.log('Horizontal line clicked at:', x, y);
                        e.preventDefault();
                        e.stopPropagation();
                        this.makeMove(x, y, 'H');
                    });
                    dotRow.appendChild(hLine);
                    this.boardElements.horizontal.push(hLine);
                    console.log('Created horizontal line at:', x, y);
                }
            }
            boardContainer.appendChild(dotRow);
            
            // Row with vertical lines and squares (except for last row)
            if (y < this.gameState.height - 1) {
                const lineRow = document.createElement('div');
                lineRow.className = 'board-row line-row';
                
                for (let x = 0; x < this.gameState.width; x++) {
                    // Add vertical line
                    const vLine = document.createElement('div');
                    vLine.className = 'vertical-line';
                    vLine.dataset.x = x;
                    vLine.dataset.y = y;
                    vLine.addEventListener('click', (e) => {
                        console.log('Vertical line clicked at:', x, y);
                        e.preventDefault();
                        e.stopPropagation();
                        this.makeMove(x, y, 'V');
                    });
                    lineRow.appendChild(vLine);
                    this.boardElements.vertical.push(vLine);
                    console.log('Created vertical line at:', x, y);
                    
                    // Add square (except for last column)
                    if (x < this.gameState.width - 1) {
                        const square = document.createElement('div');
                        square.className = 'square empty';
                        square.dataset.x = x;
                        square.dataset.y = y;
                        lineRow.appendChild(square);
                        this.boardElements.squares.push(square);
                    }
                }
                boardContainer.appendChild(lineRow);
            }
        }
        
        gameBoard.appendChild(boardContainer);
    }

    async updateBoardState() {
        try {
            // Get current game state from server
            console.log('Fetching game state...');
            const gameState = await this.apiCall('/game_state');
            console.log('Received game state:', gameState);
            
            // Update game state
            this.gameState.currentPlayer = gameState.current_player;
            this.gameState.scoreA = gameState.score_a;
            this.gameState.scoreB = gameState.score_b;
            this.gameState.remainingMoves = gameState.remaining_moves;
            this.gameState.winner = gameState.winner;
            
            console.log('Server game state:', gameState);
            console.log('Updated local game state:', this.gameState);
            console.log('Winner from server:', gameState.winner);
            console.log('Remaining moves from server:', gameState.remaining_moves);
            
            // Update vertical lines
            for (let y = 0; y < this.gameState.height - 1; y++) {
                for (let x = 0; x < this.gameState.width; x++) {
                    const index = y * this.gameState.width + x;
                    const line = this.boardElements.vertical[index];
                    if (line) {
                        const isFilled = gameState.vertical_lines[y][x] !== '*';
                        line.classList.toggle('filled', isFilled);
                    }
                }
            }
            
            // Update horizontal lines
            for (let y = 0; y < this.gameState.height; y++) {
                for (let x = 0; x < this.gameState.width - 1; x++) {
                    const index = y * (this.gameState.width - 1) + x;
                    const line = this.boardElements.horizontal[index];
                    if (line) {
                        const isFilled = gameState.horizontal_lines[y][x] !== '*';
                        line.classList.toggle('filled', isFilled);
                    }
                }
            }
            
            // Update squares
            this.updateSquares(gameState.inner_squares);
            
        } catch (error) {
            console.error('Failed to update board state:', error);
        }
    }

    updateSquares(innerSquares) {
        this.boardElements.squares.forEach(square => {
            const x = parseInt(square.dataset.x);
            const y = parseInt(square.dataset.y);
            
            const squareValue = innerSquares[y][x];
            
            if (squareValue === '*') {
                square.className = 'square empty';
                square.textContent = '';
            } else if (squareValue === 'A') {
                square.className = 'square captured-a';
                square.textContent = 'A';
            } else if (squareValue === 'B') {
                square.className = 'square captured-b';
                square.textContent = 'B';
            }
        });
    }

    async makeMove(x, y, direction) {
        console.log('makeMove called with:', x, y, direction);
        console.log('Current game state:', this.gameState);
        
        if (this.gameState.winner && this.gameState.winner !== 'Undecided') {
            console.log('Game is over, cannot make move. Winner:', this.gameState.winner);
            return;
        }
        
        try {
            console.log('Making API call for move...');
            const result = await this.apiCall('/make_move', 'POST', { x, y, direction });
            console.log('Move result:', result);
            
            if (result.result) {
                // Update game state
                await this.updateGameState();
                
                this.showStatus(`Player ${this.gameState.currentPlayer} placed a ${direction.toLowerCase()} line at (${x}, ${y})`, 'success');
            } else {
                this.showStatus('Invalid move!', 'error');
            }
        } catch (error) {
            console.error('Move failed:', error);
            this.showStatus('Failed to make move: ' + error.message, 'error');
        }
    }

    async computerMove() {
        if (this.gameState.winner) return;
        
        const depth = parseInt(document.getElementById('depth').value);
        
        try {
            this.setLoading(true);
            this.showStatus('Computer is thinking...', 'info');
            
            const response = await this.apiCall('/get_best_move', 'GET', { depth });
            
            if (response.best_move) {
                const [x, y, direction] = response.best_move;
                await this.makeMove(x, y, direction);
            } else {
                this.showStatus('No valid moves available!', 'error');
            }
        } catch (error) {
            this.showStatus('Computer move failed', 'error');
        } finally {
            this.setLoading(false);
        }
    }

    async undoMove() {
        if (this.gameState.winner) return;
        
        try {
            const result = await this.apiCall('/undo', 'POST');
            
            if (result.result) {
                await this.updateGameState();
                this.showStatus('Move undone!', 'success');
            } else {
                this.showStatus('No moves to undo!', 'error');
            }
        } catch (error) {
            this.showStatus('Failed to undo move', 'error');
        }
    }

    async updateGameState() {
        try {
            // Update board state (which also updates game state)
            await this.updateBoardState();
            
            // Update UI
            this.updateUI();
            
            // Check if game is over
            if (this.gameState.winner !== 'Undecided') {
                this.showStatus(`Game Over! Winner: ${this.gameState.winner}`, 'success');
            }
        } catch (error) {
            console.error('Failed to update game state:', error);
        }
    }

    updateUI() {
        const currentPlayerEl = document.getElementById('currentPlayer');
        const scoreAEl = document.getElementById('scoreA');
        const scoreBEl = document.getElementById('scoreB');
        const remainingMovesEl = document.getElementById('remainingMoves');
        const winnerDiv = document.getElementById('winner');
        const winnerText = document.getElementById('winnerText');
        const undoBtn = document.getElementById('undoBtn');
        const computerMoveBtn = document.getElementById('computerMoveBtn');
        
        if (currentPlayerEl) currentPlayerEl.textContent = this.gameState.currentPlayer;
        if (scoreAEl) scoreAEl.textContent = this.gameState.scoreA;
        if (scoreBEl) scoreBEl.textContent = this.gameState.scoreB;
        if (remainingMovesEl) remainingMovesEl.textContent = this.gameState.remainingMoves;
        
        if (this.gameState.winner && this.gameState.winner !== 'Undecided') {
            if (winnerText) winnerText.textContent = this.gameState.winner;
            if (winnerDiv) winnerDiv.style.display = 'block';
        } else {
            if (winnerDiv) winnerDiv.style.display = 'none';
        }
        
        // Update button states
        const gameOver = this.gameState.winner !== 'Undecided';
        if (undoBtn) undoBtn.disabled = gameOver;
        if (computerMoveBtn) computerMoveBtn.disabled = gameOver;
    }

    showStatus(message, type = 'info') {
        const statusDiv = document.getElementById('moveStatus');
        if (statusDiv) {
            statusDiv.textContent = message;
            statusDiv.className = `status-${type}`;
            
            // Clear status after 3 seconds
            setTimeout(() => {
                if (statusDiv) {
                    statusDiv.textContent = '';
                    statusDiv.className = '';
                }
            }, 3000);
        }
    }

    setLoading(loading) {
        const container = document.querySelector('.container');
        container.classList.toggle('loading', loading);
    }

    showSetupOnly() {
        const setupSection = document.getElementById('setupSection');
        const gameInfo = document.getElementById('gameInfo');
        const gameActions = document.getElementById('gameActions');
        const gameBoard = document.getElementById('gameBoard');
        const moveInfo = document.getElementById('moveInfo');
        
        if (setupSection) setupSection.style.display = 'block';
        if (gameInfo) gameInfo.style.display = 'none';
        if (gameActions) gameActions.style.display = 'none';
        if (gameBoard) gameBoard.style.display = 'none';
        if (moveInfo) moveInfo.style.display = 'none';
    }

    showGameUI() {
        const setupSection = document.getElementById('setupSection');
        const gameInfo = document.getElementById('gameInfo');
        const gameActions = document.getElementById('gameActions');
        const gameBoard = document.getElementById('gameBoard');
        const moveInfo = document.getElementById('moveInfo');
        
        if (setupSection) setupSection.style.display = 'none';
        if (gameInfo) gameInfo.style.display = 'block';
        if (gameActions) gameActions.style.display = 'block';
        if (gameBoard) gameBoard.style.display = 'flex';
        if (moveInfo) moveInfo.style.display = 'block';
    }

    restartGame() {
        this.gameState.gameActive = false;
        this.gameState.winner = null;
        this.showSetupOnly();
        this.showStatus('Game restarted!', 'info');
    }

    quitGame() {
        this.gameState.gameActive = false;
        this.gameState.winner = null;
        this.showSetupOnly();
        this.showStatus('Game quit!', 'info');
    }

    initializeEventListeners() {
        const newGameBtn = document.getElementById('newGameBtn');
        const undoBtn = document.getElementById('undoBtn');
        const computerMoveBtn = document.getElementById('computerMoveBtn');
        const restartBtn = document.getElementById('restartBtn');
        const quitBtn = document.getElementById('quitBtn');
        
        if (newGameBtn) newGameBtn.addEventListener('click', () => this.createNewGame());
        if (undoBtn) undoBtn.addEventListener('click', () => this.undoMove());
        if (computerMoveBtn) computerMoveBtn.addEventListener('click', () => this.computerMove());
        if (restartBtn) restartBtn.addEventListener('click', () => this.restartGame());
        if (quitBtn) quitBtn.addEventListener('click', () => this.quitGame());
    }
}

// Initialize the UI when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new DotsAndBoxesUI();
});
