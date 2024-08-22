import pygame
from chess import *
import chess
#board = chess.Board()

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Chess")

# Colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)

# Create a dictionary of piece representations
PIECE_SYMBOLS = {
    'p': '!', 'r': '[]', 'n': '&', 'b': '()', 'q': '#', 'k': '@',
    'P': '!', 'R': '[]', 'N': '&', 'B': '()', 'Q': '#', 'K': '@'
}

# Draw the board
def draw_board(screen):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = WHITE if (row + col) % 2 == 0 else GRAY
            pygame.draw.rect(screen, color, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Draw the pieces
def draw_pieces(screen, board):
    font = pygame.font.SysFont('dejavusansmono', 64)
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            x = chess.square_file(square) * SQ_SIZE
            y = (7 - chess.square_rank(square)) * SQ_SIZE
            piece_symbol = PIECE_SYMBOLS[piece.symbol()]
            text = font.render(piece_symbol, True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + SQ_SIZE // 2, y + SQ_SIZE // 2))
            screen.blit(text, text_rect)

# Highlight squares
def highlight_squares(screen, board, selected_square):
    if selected_square:
        pygame.draw.rect(screen, YELLOW, pygame.Rect(
            chess.square_file(selected_square) * SQ_SIZE, 
            (7 - chess.square_rank(selected_square)) * SQ_SIZE, 
            SQ_SIZE, SQ_SIZE
        ), 3)
        
        moves = board.legal_moves
        for move in moves:
            if move.from_square == selected_square:
                pygame.draw.rect(screen, BLUE, pygame.Rect(
                    chess.square_file(move.to_square) * SQ_SIZE, 
                    (7 - chess.square_rank(move.to_square)) * SQ_SIZE, 
                    SQ_SIZE, SQ_SIZE
                ), 3)

# Main game loop
def main():
    board = Board()
    selected_square = None
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = 7 - (location[1] // SQ_SIZE)
                square = chess.square(col, row)

                if selected_square is None:
                    if board.piece_at(square):
                        selected_square = square
                else:
                    move = chess.Move(selected_square, square)
                    if move in board.legal_moves:
                        board.push(move)
                    selected_square = None

        screen.fill(pygame.Color("white"))
        draw_board(screen)
        highlight_squares(screen, board, selected_square)
        draw_pieces(screen, board)
        pygame.display.flip()
        clock.tick(15)

    pygame.quit()

if __name__ == "__main__":
    main()