from tictactoe.game.Board import Board
from tictactoe.game.GameEnums import Player


class TicTacToe:

    def __init__(self):
        self.__board = Board()
        self.__turn = Player.PLAYER_X

    def makemove(self, *args):
        # Usage
        # success = makemove( board_cell )
        # success = makemove( cell_index )
        # success = makemove( row, column )

        if self.__board.isvalidmove( *args ):

            self.__board.setcell( self.__turn, *args )
            self.__advanceturn()

            return True

        else:
            return False

    def reset(self):
        self.__board = Board()
        self.__turn = Player.PLAYER_X

    def getboard(self):
        return self.__board

    def getgamestate(self):
        return self.__board.getgamestate()

    def getplayerturn( self ):
        return self.__turn

    def getwinner( self ):
        return self.__board.getwinner()

    def __advanceturn( self ):

        if self.__board.getwinner() != Player.NO_PLAYER:
            self.__turn == Player.NO_PLAYER
        elif self.__turn == Player.PLAYER_X:
            self.__turn = Player.PLAYER_O
        elif self.__turn == Player.PLAYER_O:
            self.__turn = Player.PLAYER_X

