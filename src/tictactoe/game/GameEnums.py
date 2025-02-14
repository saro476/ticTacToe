import math
from enum import Enum


class Player( Enum ):
    NO_PLAYER = 0
    PLAYER_X = 1
    PLAYER_O = 2

    def __str__( self ):
        if self == Player.PLAYER_X:
            return "X"
        elif self == Player.PLAYER_O:
            return "O"
        else:
            return "-"


class BoardCell( Enum ):
    UPPER_LEFT = 0
    UPPER_CENTER = 1
    UPPER_RIGHT = 2
    CENTER_LEFT = 3
    CENTER = 4
    CENTER_RIGHT = 5
    BOTTOM_LEFT = 6
    BOTTOM_CENTER = 7
    BOTTOM_RIGHT = 8

    def coord( self ):
        return [math.floor( self.value / 3 ), self.value % 3]


def getboardcell( *args ):
    # Usage
    # getboardcell( board_cell )
    # getboardcell( cell_index )
    # getboardcell( row, column )
    if len( args ) == 1:
        if isinstance( args[0], BoardCell ):
            return args[0]
        else:
            return BoardCell( args[0] )
    else:
        return BoardCell( args[0] * 3 + args[1] )


def coord2cell( row, col ):
    return BoardCell( row * 3 + col )


class GameState( Enum ):
    IN_PROGRESS = 0
    WINNER_X = 1
    WINNER_O = 2
    TIE = 3


def iswinner( state, player ):
    if state == GameState.WINNER_X and player == Player.PLAYER_X:
        return True
    elif state == GameState.WINNER_O and player == Player.PLAYER_O:
        return True
    else:
        return False


def isloser( state, player ):
    if state == GameState.WINNER_O and player == Player.PLAYER_X:
        return True
    elif state == GameState.WINNER_X and player == Player.PLAYER_O:
        return True
    else:
        return False
