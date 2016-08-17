# -*- encoding: utf-8 -*-
import board
import os
import time

UNICODE_PIECES = {
  'r': u'♜', 'n': u'♞', 'b': u'♝', 'q': u'♛',
  'k': u'♚', 'p': u'♟', 'R': u'♖', 'N': u'♘',
  'B': u'♗', 'Q': u'♕', 'K': u'♔', 'P': u'♙',
  None: ' '
}

class BoardGuiConsole(object):
    '''
        Print a text-mode chessboard using the unicode chess pieces
    '''
    error = ''

    def __init__(self, chessboard):
        self.board = chessboard

    def prompt(self):
        self.error = ''
        print ('State a move in chess notation (e.g. A2A3).\n'
            "State a piece's coordinates to see it's valid moves (e.g. A2).\n"
            'Type \"exit\" to leave:')
        print '>>>',
        coord = raw_input()
        if coord == "exit":
            print "Bye."
            exit(0)
        if len(coord) == 2:
            try:
                if coord in (self.board.occupied("white") + self.board.occupied("black")):
                    self.error = "Possible move for {} is {}".format(self.board[coord].abbriviation ,self.board[coord].possible_moves(coord))
                else:
                    self.error = "No Piece is located at {}".format(coord)
            except board.ChessError as error:
                self.error = "Error: %s" % error.__class__.__name__
        elif len(coord) == 4:
            try:
                if len(coord) != 4: raise board.InvalidCoord
                self.board.move(coord[0:2], coord[2:4])
                os.system("clear")
            except board.ChessError as error:
                self.error = "Error: %s" % error.__class__.__name__
        else:
            self.error = "Invalid Input: {}".format(coord)

    def move(self):
        os.system("clear")
        self.unicode_representation()
        print ('------------------------\n'
            '{}'
            '\n------------------------').format(self.error)
        self.prompt()
        self.move()

    def unicode_representation(self):
        print "\n", ("%s's turn\n" % self.board.player_turn.capitalize()).center(28)
        for number in self.board.axis_x[::-1]:
            print " " + str(number) + " ",
            for letter in self.board.axis_y:
                piece = self.board[letter+str(number)]
                if piece is not None:
                    print UNICODE_PIECES[piece.abbriviation] + ' ',
                else: print '  ',
            print "\n"
        print "    " + "  ".join(self.board.axis_y)


def display(board):
    try:
        gui = BoardGuiConsole(board)
        gui.move()
    except (KeyboardInterrupt, EOFError):
        os.system("clear")
        exit(0)
