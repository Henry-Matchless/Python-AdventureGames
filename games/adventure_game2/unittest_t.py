import unittest
from Room import Room
from Thing import Thing
from Game import Game
from Package import PackageGUI

class MyTestCase(unittest.TestCase):
    
    def setUp(self):
        self.game = Game()

    def test_updateRoom(self):
        try:
            self.game.updateRoom()
            assert(True)
            self.game.currentRoom = self.game.lobby
            self.game.updateRoom()
            assert(True)
        except Exception as e:
            print('error'+str(e))
            assert(False)

    def test_addMsg(self):
        try:
            self.game.addMsg('sksksk')
            assert(True)
        except Exception as e:
            print('error:'+str(e))
            assert(False)

    def test_start(self):
        try:
            self.game.start()
            assert(True)
        except Exception as e:
            print('error:'+str(e))
            assert(False)

    def test_startPage(self):
        try:
            self.game.startPage()
            assert(True)
        except Exception as e:
            print('error:'+str(e))
            assert(False)

    def test_move(self):
        try:
            self.game.move([11,233], ('aaa', None))
            assert(True)
        except Exception as e:
            print('error:'+str(e))
            assert(False)

    def test_moving(self):
        try:
            self.game.moving()
            assert(True)
        except Exception as e:
            print('error:'+str(e))
            assert(False)

    def test_doAttackCommand(self):
        try:
            self.game.doAttackCommand([111,22])
            assert(True)
        except Exception as e:
            print('error:'+str(e))
            assert(False)

    def test_doPackageCommand(self):
        try:
            self.game.doPackageCommand()
            assert(True)
        except Exception as e:
            print('error:'+str(e))
            assert(False)

    def test_saveGame(self):
        try:
            self.game.saveGame()
            assert(True)
        except Exception as e:
            print('error:'+str(e))
            assert(False)

if __name__ == '__main__':
    unittest.main()
