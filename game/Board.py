from game.GameEnums import Player
from game.GameEnums import getboardcell
from game.GameEnums import GameState


class Board:

    def __init__( self, init_state=0 ):
        self.__board = []

        for i in range( 9 ):
            player = Player( init_state % 3 )
            self.__board.append( player )
            init_state -= player.value
            init_state /= 3

        self.__turn = Player.NO_PLAYER
        self.__turn_calculated = False

    def getwinner( self ):
        for i in range( 3 ):
            # Row check
            if Player.NO_PLAYER != self.getcell( i, 0 ) == self.getcell( i, 1 ) == self.getcell( i, 2 ):
                return self.getcell( i, 0 )

            # Col check
            if Player.NO_PLAYER != self.getcell( 0, i ) == self.getcell( 1, i ) == self.getcell( 2, i ):
                return self.getcell( 0, i )

        # Diagonal check
        if Player.NO_PLAYER != self.getcell( 0, 0 ) == self.getcell( 1, 1 ) == self.getcell( 2, 2 ):
            return self.getcell( 1, 1 )

        elif Player.NO_PLAYER != self.getcell( 0, 2 ) == self.getcell( 1, 1 ) == self.getcell( 2, 0 ):
            return self.getcell( 0, 2 )

        return Player.NO_PLAYER

    def isvalidmove( self, *args ):
        # Usage
        # isvalidmove( board, board_cell )
        # isvalidmove( board, cell_index )
        # isvalidmove( board, row, column )

        return self.getcell( *args ) is Player.NO_PLAYER and self.getwinner() == Player.NO_PLAYER

    def getcell( self, *args ):
        # Usage
        # getcell( board_cell )
        # getcell( cell_index )
        # getcell( row, column )

        return self.__board[getboardcell(*args).value]

    def setcell( self, val, *args ):
        # Usage
        # setcell( val, board_cell )
        # setcell( val, cell_index )
        # setcell( val, row, column )
        self[getboardcell(*args).value] = val

    def getstate( self ):
        state = 0
        for i in range( 9 ):
            state += pow( 3, i ) * self.__board[i].value
        return state

    def getgamestate( self ):
        winner = self.getwinner()
        if winner == Player.NO_PLAYER:

            complete = True

            for idx in range(9):
                if self.__board[idx] == Player.NO_PLAYER:
                    complete = False
                    break

            if complete:
                return GameState.TIE
            else:
                return GameState.IN_PROGRESS
        elif winner == Player.PLAYER_O:
            return GameState.WINNER_O

        elif winner == Player.PLAYER_X:
            return GameState.WINNER_X

        else:
            return GameState.IN_PROGRESS

    def __calcturn( self ):
        player_count = 0
        for cell in self.__board:
            if cell == Player.PLAYER_O:
                player_count -= 1
            elif cell == Player.PLAYER_X:
                player_count += 1

        if player_count == 0:
            self.__turn = Player.PLAYER_X
        else:
            self.__turn = Player.PLAYER_O

        self.__turn_calculated = True

    def getturn( self ):
        if not self.__turn_calculated:
            self.__calcturn()
        return self.__turn

    def __getitem__( self, idx ):
        return self.__board[idx]

    def __setitem__( self, idx, value ):
        self.__board[idx] = value
        self.__turn_calculated = False

    def __str__( self ):
        str_val = " | 1 2 3 |\n"
        str_val += "-|-------"

        for row in range( 3 ):
            str_val += "|\n"+str(row+1)+"| "
            for col in range( 3 ):
                str_val += str( self.getcell( row, col ) ) + " "

        str_val += "|\n-|-------|"

        return str_val
