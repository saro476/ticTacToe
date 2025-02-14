from tictactoe.ai.TNode import TNode
from tictactoe.game.Board import Board
from tictactoe.game.GameEnums import Player
from minmax.minmax import PlayerType, MinMaxTree
from tictactoe.ui.GraphicUi import GraphicUi
from tictactoe.ai.BoardNode import BoardNode


def test5():
    print( "\n=====TEST 5====" )

    node = BoardNode( state = 0 )

    board = node.getboard()

    print( "Single Node:" )
    print(node)

    node.expand( depth = -1 )

    f = open( "C:\\Users\\aalow\Desktop\\test5.txt", "w" )
    f.write( str(node) )
    f.close

def test1():
    print( "\n=====TEST 1====" )

    players = {Player.PLAYER_X: PlayerType.USER, Player.PLAYER_O: PlayerType.AI}
    tree = MinMaxTree( players )
    node = TNode( tree, state = 0 )

    board = Board( node.id )

    print( "Single Node:" )
    print(node)

    node.expand( depth = -1 )

    f = open( "C:\\Users\\aalow\Desktop\\test1.txt", "w" )
    f.write( str(node) )
    f.close

def test2():
    gui = GraphicUi()

if __name__ == '__main__':
    test2()

    # ui = TextUi()
    # ui.run()

    # gui = GraphicUi()

