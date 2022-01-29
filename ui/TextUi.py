from game.TicTacToe import TicTacToe
from game.GameEnums import GameState
from game.GameEnums import Player
from game.GameEnums import coord2cell
from ai.BoardNode import BoardNode
from enum import Enum


class PlayerType( Enum ):
    USER = 0
    AI = 1


class TextUi:

    def __init__(self):
        self.__game = TicTacToe()
        self.__playerX = PlayerType.USER
        self.__playerO = PlayerType.USER

    def run( self ):

        # Reset game
        self.__game.reset()

        # Request mode selection
        self.__selectmode()

        # Main game loop
        while self.__game.getgamestate() == GameState.IN_PROGRESS:

            # Print board
            self.printboard()

            # Request move
            move = self.__requestnextmove()

            # Update board with new move
            valid = self.__game.makemove( move )

            if not valid:
                print( "Invalid move requested. Please try again.")

        # Print board and display winner
        self.printboard()
        self.printwinner()

    def __selectmode( self ):

        mode = None

        while mode is None:
            print( "=====Modes=====")
            print( "1) Single player")
            print( "2) Two player")
            mode = input( "Select the game mode:" )

            if int(mode) == 1:
                self.__playerX = PlayerType.AI
            elif int(mode) == 2:
                self.__playerX = PlayerType.USER
            else:
                mode = None
                print( "Invalid response. Please try again.")


    def __requestnextmove( self ):
        if self.__game.getplayerturn() == Player.PLAYER_X:
            user_type = self.__playerX
        elif self.__game.getplayerturn() == Player.PLAYER_O:
            user_type = self.__playerO
        else:
            return None

        if user_type == PlayerType.USER:
            return self.__requestusermove()
        else:
            return self.__requestaimove()

    def __requestusermove( self ):

        valid_move = False

        while not valid_move:

            if self.__game.getplayerturn() == Player.PLAYER_X:
                txt_move = input( "\nPlayer X make your move (row,col):" )
            else:
                txt_move = input( "\nPlayer O make your move (row,col):" )

            txt_move = txt_move.split(",")

            if len( txt_move ) == 2:
                row = int( txt_move[0] ) - 1
                col = int( txt_move[1] ) - 1

                if 0 <= row <= 2 and 0 <= col <= 2:
                    valid_move = self.__game.getboard().isvalidmove( row, col )

            if not valid_move:
                print( "Invalid move. Please try again using the format row,column where row and column are numbers" )
                print( "between 1 and 3" )

        return coord2cell( row, col )

    def __requestaimove( self ):
        return BoardNode.getbestmove( self.__game.getboard(), self.__game.getplayerturn() )

    def printboard( self ):
        print( "\n\n==========\n")
        print(self.__game.getboard())

    def printwinner( self ):

        state = self.__game.getgamestate()

        print( "\n")

        if state == GameState.WINNER_X:
            print( "Player X wins" )
        elif state == GameState.WINNER_O:
            print( "Player O wins" )
        else:
            print( "The game ended in a draw." )

        print( "Good Game!" )


