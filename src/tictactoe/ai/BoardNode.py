from tictactoe.game.Board import Board
from tictactoe.game.GameEnums import *


class BoardNode:

    node_dict = {}

    def __init__(self, state=0):
        if isinstance( state, Board ):
            self.__state = state.getstate()
        elif isinstance( state, BoardNode ):
            self.__state = state.__state
        else:
            self.__state = state

        # Default initialization
        self.__turn = Player.NO_PLAYER
        self.__num_x_wins = 0
        self.__num_o_wins = 0
        self.__num_ties = 0

        self.__children = []
        self.__transitions = {}

        self.__best_child = None

        self.__expanded = False

        # Initialize board from state
        board = Board( self.__state )
        self.__gamestate = board.getgamestate()
        state = self.__gamestate

        # Get next player's turn
        player_count = 0
        for cell in BoardCell.__members__.values():
            player = board.getcell( cell )
            if player == Player.PLAYER_O:
                player_count -= 1
            elif player == Player.PLAYER_X:
                player_count += 1

        if player_count == 0:
            self.__turn = Player.PLAYER_X
        else:
            self.__turn = Player.PLAYER_O

        self.update()

    def getstate( self ):
        return self.__state

    def getboard( self ):
        return Board( self.__state )

    def getchildren( self ):
        return self.__children

    def gettransitions( self ):
        return self.__transitions

    def getwins( self, player ):
        if player == Player.PLAYER_X:
            return self.__num_x_wins
        elif player == Player.PLAYER_O:
            return self.__num_o_wins
        else:
            return None

    def getlosses( self, player ):
        if player == Player.PLAYER_X:
            return self.__num_o_wins
        elif player == Player.PLAYER_O:
            return self.__num_x_wins
        else:
            return None

    def getties( self ):
        return self.__num_ties

    def expand( self, depth=0 ):
        # Usage
        # expand()              - Expand one layer
        # expand( depth )       - Expand by depth layers
        # expand( -1 )          - Expand all layers

        # Skip expansion if already expanded
        if not self.__expanded:

            # Expand nodes based on available moves
            if self.__gamestate == GameState.IN_PROGRESS:
                board = Board( self.__state )
                for cell in BoardCell.__members__.values():
                    if board.getcell(cell) == Player.NO_PLAYER:
                        board.setcell(self.__turn, cell)
                        state = board.getstate()
                        node = BoardNode.getnode(state)
                        self.__children.append(node)
                        self.__transitions[node.__state] = cell
                        board.setcell(Player.NO_PLAYER, cell)

            self.__expanded = True

        # Expand children if requested
        if depth != 0:
            depth = depth - 1
            for child in self.__children:
                child.expand( depth )

        # Update internal counts
        self.update()

    def update( self ):

        if self.__gamestate == GameState.WINNER_X:
            self.__num_x_wins = 1
        elif self.__gamestate == GameState.WINNER_O:
            self.__num_o_wins = 1
        elif self.__gamestate == GameState.TIE:
            self.__num_ties = 1
        else:
            self.__best_child = None
            for child in self.__children:
                if self.__best_child is None:
                    self.__best_child = child
                elif BoardNode.comparenodesforplayer( self.__best_child, child, self.__turn ) < 0:
                    self.__best_child = child

            if self.__best_child is not None:
                self.__num_x_wins = self.__best_child.__num_x_wins
                self.__num_o_wins = self.__best_child.__num_o_wins
                self.__num_ties = self.__best_child.__num_ties

    def __eq__( self, other ):
        if other is BoardNode:
            return self.__num_o_wins == other.__num_o_wins and self.__num_x_wins == other.__num_x_wins and self.__num_ties == other.__num_ties
        else:
            return super().__le__(self, other)

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
        wlt_str = " X: " + str( self.__num_x_wins )
        wlt_str += ", O: " + str( self.__num_o_wins )
        wlt_str += ", T: " + str( self.__num_ties )

        # Set turn string
        turn_str = ", Turn: " + str(self.__turn)

        # Combine strings
        ret_str = indent_str + board_str + wlt_str + turn_str + "\n"

        # Get child strings
        if layers != 0:
            for child in self.__children:
                ret_str += child.__str__( level + 1, layers - 1)

        return ret_str

    @staticmethod
    def getnode(state):
        if state in BoardNode.node_dict.keys():
            return BoardNode.node_dict[state]
        else:
            node = BoardNode( state )
            BoardNode.node_dict[state] = node
            return node

    def __getbestmove( self ):
        # Return transition
        transition = self.__transitions[ self.__best_child.__state ]
        return transition

    @staticmethod
    def getbestmove( state ):
        if isinstance( state, Board ):
            node = BoardNode.getnode( state.getstate() )
        elif isinstance( state, BoardNode ):
            node = state
        else:
            node = BoardNode.getnode( state )

        node.expand( -1 )
        return node.__getbestmove()

    @staticmethod
    def comparenodesforplayer( node1, node2, player ):
        return node1.getwins(player) - node2.getwins(player) - node1.getlosses(player) + node2.getlosses(player)

    @staticmethod
    def initializenodes():
        node = BoardNode.getnode( 0 )
        node.expand( -1 )
