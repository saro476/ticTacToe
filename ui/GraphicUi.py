import tkinter as tk

from ai.TNode import TNode
from game.GameEnums import BoardCell
from game.TicTacToe import TicTacToe
from ai.BoardNode import BoardNode
from game.GameEnums import GameState
from game.GameEnums import Player
from minmax.minmax import MinMaxTree, PlayerType
from enum import Enum

debug = False

def log( text ):
    print( text )

# Enumerations
class GameMode( Enum ):
    SINGLE_PLAYER = 0
    TWO_PLAYER = 1


# Graphic UI class
class GraphicUi(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs, className="Tic-Tac-Toe")

        self.__debug = True

        # Setup menu frame
        self.__menu_frame = MenuFrame( self, game_command=self.__setup_game )

        # Setup game frame
        self.__game_frame = GameFrame( self, menu_command=self.__setup_menu )

        # Start GUI
        self.__setup_menu()
        self.geometry("600x600")
        self.mainloop()

    def __setup_menu( self ):
        # Adds the menu frame to the window
        self.__game_frame.pack_forget()

        self.__menu_frame.pack( anchor=tk.CENTER, fill=tk.BOTH, expand=True)

    def __setup_game( self, game_mode=GameMode.SINGLE_PLAYER ):
        # Adds the game frame to the window and sets the game mode
        # This will reset the game
        self.__menu_frame.pack_forget()

        self.__game_frame.setgamemode( game_mode )
        self.__game_frame.reset()
        self.__game_frame.pack( anchor=tk.CENTER, fill=tk.BOTH, expand=True)


# Menu frame class
class MenuFrame(tk.Frame):

    def __init__( self, *args, game_command=None, **kwargs ):
        tk.Frame.__init__(self, *args, **kwargs)

        self.__game_command = game_command

        # Setup grid
        self.columnconfigure( 0, weight = 1 )
        self.columnconfigure( 1, weight = 1 )
        self.columnconfigure( 2, weight = 1 )
        self.columnconfigure( 3, weight = 1 )
        self.columnconfigure( 4, weight = 1 )

        self.rowconfigure( 0, weight = 1 )
        self.rowconfigure( 1, weight = 1 )
        self.rowconfigure( 2, weight = 1 )

        # Set game title
        self.__title_label = tk.Label(self, text = 'Tic-Tac-Toe', font = 48)

        # Set game mode buttons
        self.__single_player_button = tk.Button( self, text = "Single Player", font = 24, command=self.__singleplayer_callback )
        self.__two_player_button = tk.Button( self, text = "Two Player", font = 24, command=self.__twoplayer_callback )

        # Add widgets to frame
        self.__title_label.grid( row = 0, column = 0, columnspan = 5, rowspan = 2, sticky='nsew')
        self.__single_player_button.grid( row = 2, column = 1 )
        self.__two_player_button.grid( row = 2, column = 3 )

    def __singleplayer_callback( self ):
        # Callback for the single-player button
        self.__game_command( GameMode.SINGLE_PLAYER )

    def __twoplayer_callback( self ):
        # Callback for the two-player button
        self.__game_command( GameMode.TWO_PLAYER )


class GameFrame(tk.Frame):

    def __init__( self, *args, menu_command=None, gamemode = GameMode.SINGLE_PLAYER, **kwargs ):
        tk.Frame.__init__( self, *args, **kwargs )

        # Setup game
        self.__game = TicTacToe()
        self.__menu_command = menu_command
        self.__gamemode = gamemode
        self.setgamemode( gamemode )
        # BoardNode.initializenodes()
        self.__players = {Player.PLAYER_X: PlayerType.USER, Player.PLAYER_O: PlayerType.AI }
        self.__tree = MinMaxTree( self.__players )
        node = TNode( self.__tree, self.__game.getboard().getstate() )
        node.expand( -1 )
        node.update()

        # Setup grid
        self.columnconfigure( 0, weight = 1 )
        self.columnconfigure( 1, weight = 1 )
        self.columnconfigure( 2, weight = 1 )

        self.rowconfigure( 0, weight = 0 ) # Title
        self.rowconfigure( 1, weight = 1 ) # Grid row 1
        self.rowconfigure( 2, weight = 1 ) # Grid row 2
        self.rowconfigure( 3, weight = 1 ) # Grid row 3
        self.rowconfigure( 4, weight = 0 ) # Turn label
        self.rowconfigure( 5, weight = 0 ) # Control buttons

        # Set game title
        self.__title_label = tk.Label( self, text = 'Tic-Tac-Toe', font = 24 )
        self.__title_label.grid( row = 0, column = 0, columnspan=3, sticky = 'nsew')

        # Set game board
        self.__grid_buttons = []
        for i in range( 9 ):
            grid_button = tk.Button( self, text = '-', height=5, width=15, font = 24, command = lambda m=i: self.__grid_callback(m) )
            self.__grid_buttons.append( grid_button )
            (row,col) = BoardCell( i ).coord()
            grid_button.grid( row = row + 1, column = col, sticky='nsew' )

        # Setup turn label
        self.__turn_label = tk.Label( self, text='' )
        self.__turn_label.grid( row = 4, column = 0, columnspan = 3, sticky='nsew' )

        # Set control buttons
        self.__menu_button = tk.Button( self, text = 'Menu', command = self.__menu_callback )
        self.__menu_button.grid( row = 5, column = 0, sticky = 'nsew' )
        self.__reset_button = tk.Button( self, text = 'Reset', command = self.__reset_callback )
        self.__reset_button.grid( row = 5, column = 2, sticky = 'nsew' )

        # Start game
        self.reset()

    def setgamemode( self, gamemode ):
        # Sets the gamemode and establishes player types
        self.__gamemode = gamemode
        if gamemode == GameMode.SINGLE_PLAYER:
            self.__players = {Player.PLAYER_X: PlayerType.USER, Player.PLAYER_O: PlayerType.AI }
        else:
            self.__players = {Player.PLAYER_X: PlayerType.USER, Player.PLAYER_O: PlayerType.AI }

    def reset( self ):
        # Resets the game to the initial state and prepares for the next input
        log( "Resetting game" )

        # Reset game
        self.__game.reset()

        # Reset grid buttons
        for button in self.__grid_buttons:
            button['text'] = ''
            button['bg'] = 'white'
            button['state'] = "normal"
        self.__reset_button['text'] = 'Reset'

        # Setup next move
        self.__setupnextmove()

    def swapplayers( self ):
        # Swap players between games. This allows the user to alternate first and second
        log( "Swapping players" )

        temp = self.__players[Player.PLAYER_X]
        self.__players[Player.PLAYER_X] = self.__players[Player.PLAYER_O]
        self.__players[Player.PLAYER_O] = temp

    def __playmove( self, move ):
        # Play a move for the current player and advance the game state
        log( "Playing move" )

        if not self.__checkendcondition():
            index = move.value
            button = self.__grid_buttons[index]
            button['state'] = "disabled"
            button['text'] = str(self.__game.getplayerturn())

            self.__game.makemove( move )

        is_ended = self.__checkendcondition()

        if is_ended:
            self.__endgame()
        else:
            self.__setupnextmove()

    def __setupnextmove( self ):
        # Setup graphics for the next turn
        log( "Setup for next move" )

        user_type = None
        turn = self.__game.getplayerturn()
        if turn == Player.PLAYER_X:
            user_type = self.__players[Player.PLAYER_X]
        elif turn == Player.PLAYER_O:
            user_type = self.__players[Player.PLAYER_O]

        if user_type == PlayerType.AI:
            self.__turn_label['text'] = "It's the computer's turn"
        else:
            if self.__gamemode == GameMode.SINGLE_PLAYER:
                self.__turn_label['text'] = "It's your turn"
            else:
                self.__turn_label['text'] = "It's player " + str( turn ) + "'s turn"

        self.__getnextmove()

    def __getnextmove( self ):
        # Request the next move. If the next player is an AI, return the best move.
        # If not, wait for user input
        log( "Requesting next move" )

        if self.__game.getplayerturn() == Player.PLAYER_X:
            user_type = self.__players[Player.PLAYER_X]
        elif self.__game.getplayerturn() == Player.PLAYER_O:
            user_type = self.__players[Player.PLAYER_O]
        else:
            return None

        if user_type == PlayerType.AI:
            # ai_move = BoardNode.getbestmove( self.__game.getboard() )
            state = self.__game.getboard().getstate()
            node = self.__tree.get_node( state )
            turn = self.__game.getplayerturn()
            ai_move = node.best_move( turn )
            self.__playmove( ai_move )
        # If it is a player's turn, just wait for a button press

    def __checkendcondition( self ):
        # Return T/F if the game has ended
        game_state = self.__game.getgamestate()
        return game_state != GameState.IN_PROGRESS

    def __endgame( self ):
        # Set graphics and values for when the game has ended.
        log( "Ending game" )

        # Switch players
        self.swapplayers()

        # Reset buttons
        for button in self.__grid_buttons:
            button['bg'] = 'grey'
            button['state'] = tk.DISABLED

        # Display winner
        game_state = self.__game.getgamestate()
        if game_state == GameState.WINNER_X:
            text =  "Player X wins"
        elif game_state == GameState.WINNER_O:
            text =  "Player O wins"
        else:
            text =  "The game ended in a draw."

        self.__turn_label['text'] = text

        self.__reset_button['text'] = 'New Game'

    def __grid_callback( self, index ):
        # Callback function for grid buttons
        log( "Grid button event" )

        grid_cell = BoardCell( index )

        if self.__game.getplayerturn() == Player.PLAYER_X:
            user_type = self.__players[Player.PLAYER_X]
        elif self.__game.getplayerturn() == Player.PLAYER_O:
            user_type = self.__players[Player.PLAYER_O]
        else:
            return None

        if user_type == PlayerType.USER:
            self.__playmove( grid_cell )

    def __menu_callback( self ):
        # Callback function for return to menu button
        # Takes appropriate action to return to the menu
        log( "Menu button event" )
        self.__menu_command()

    def __reset_callback( self ):
        # Callback function for reset button.
        # Takes appropriate action to reset the game
        log( "Reset button event" )
        self.reset()




if __name__ == '__main__':
    gui = GraphicUi()
