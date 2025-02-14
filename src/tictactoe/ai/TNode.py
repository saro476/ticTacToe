from tictactoe.game.GameEnums import BoardCell, Player, GameState
from minmax.minmax import Node, Transition
from tictactoe.game.Board import Board


class TNode(Node):

    def __init__(self, min_max_tree, state):
        self.__state = state

        board = Board( self.__state )
        self.__terminal = board.getgamestate() != GameState.IN_PROGRESS
        self.__game_state = board.getgamestate()

        Node.__init__(self, min_max_tree)

    def init_id( self ):
        self.id = self.__state

    def expand( self, depth=0 ):
        # Usage
        # expand()              - Expand one layer
        # expand( depth )       - Expand by depth layers
        # expand( -1 )          - Expand all layers

        # Skip expansion if already expanded
        if not self._expanded and not self.terminal:

            # Expand nodes based on available moves
            board = Board( self.__state )
            turn = board.getturn()
            for cell in BoardCell.__members__.values():
                if board.getcell(cell) == Player.NO_PLAYER:
                    board.setcell(turn, cell)
                    state = board.getstate()
                    try:
                        node = self._tree.get_node(state)
                    except KeyError:
                        node = TNode(self._tree, state)
                    self.add_transition( Transition( self, node, turn, board.getturn(), cell ) )
                    board.setcell(Player.NO_PLAYER, cell)

            self._expanded = True
        else:
            pass

        # Expand children if requested
        if depth != 0:
            depth = depth - 1
            for transition in self.transitions:
                transition.end_node.expand( depth )

        # Update internal counts
        self.update()

    @property
    def terminal( self ):
        if self.__terminal is None:
            board = Board( self.__state )
            self.__terminal = board.getgamestate() != GameState.IN_PROGRESS
        return self.__terminal

    def update_values( self ):
        if self.__game_state == GameState.WINNER_X:
            self._values[Player.PLAYER_O] = -1
            self._values[Player.PLAYER_X] = 1
        elif self.__game_state == GameState.WINNER_O:
            self._values[Player.PLAYER_O] = 1
            self._values[Player.PLAYER_X] = -1
        else:
            self._values[Player.PLAYER_O] = 0
            self._values[Player.PLAYER_X] = 0

    def __str__( self, level=0, layers=-1 ):

        # Set indention string
        indent_str = ""
        for i in range( level ):
            indent_str += "|  "
        indent_str += "|->"

        # Set board string
        board = Board( self.__state )
        board_str = "[ "
        for cell in BoardCell.__members__.values():
            board_str += str( board.getcell(cell) ) + " "
        board_str += "]"

        # Set Win/Loss/Tie string
        wlt_str = " X: " + str( self._values[Player.PLAYER_X] )
        wlt_str += ", O: " + str( self._values[Player.PLAYER_O] )

        # Set turn string
        turn_str = ", Turn: " + str(board.getturn())

        # Combine strings
        ret_str = indent_str + board_str + wlt_str + turn_str + "\n"

        # Get child strings
        if layers != 0:
            for transition in self.transitions:
                ret_str += transition.end_node.__str__( level + 1, layers - 1)

        return ret_str