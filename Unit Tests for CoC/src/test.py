import unittest
import village
from king import  *
import points as pt

class SimpleTest(unittest.TestCase):
    def test_alive(self):
        # king moves 1 move towards R & then dies, therefore its position should not be updated from 0,1
        V = village.createVillage(1)
        K = spawnKing([0, 0])
        K.move('right', V)
        K.kill()
        K.move('left', V)
        K.move('up', V)
        K.move('up', V)
        K.move('up', V)
        K.move('down', V)
        K.move('right', V)
        K.move('right', V)
        self.assertEqual(K.position, [0, 1])

    # movement in a 17X35 grid. We go to each point in the grid and then try the 4 available options W,A,S,D. 
    # if something is at the position we plan to go at, the move function should do nothing
    # else it should update the position of the king 
    def test_mov(self):
        # init king & village 
        V = village.createVillage(1)
        K = spawnKing([0, 0])
        vmap = V.map
        # loop to access each point in grid
        for i in range(1,17):
            for j in range(1,35):
                K.position[0] = i
                K.position[1] = j
                K.move('left', V)
                # check for object on left of king
                if(vmap[i][j-1] != pt.BLANK):
                    # if object, position doesnt change
                    self.assertEqual(K.position, [i, j])
                else :
                    # else changes 
                    self.assertEqual(K.position, [i, j-1])
                # right    
                K.position[0] = i
                K.position[1] = j
                K.move('right', V)
                if(vmap[i][j+1] != pt.BLANK):
                    self.assertEqual(K.position, [i, j])
                else :
                    self.assertEqual(K.position, [i, j+1])
                # up
                K.position[0] = i
                K.position[1] = j
                K.move('up', V)
                if(vmap[i-1][j] != pt.BLANK):
                    self.assertEqual(K.position, [i, j])
                else :
                    self.assertEqual(K.position, [i-1, j])
                # down
                K.position[0] = i
                K.position[1] = j
                K.move('down', V)
                if(vmap[i+1][j] != pt.BLANK):
                    self.assertEqual(K.position, [i, j])
                else :
                    self.assertEqual(K.position, [i+1, j])

    def test_edges_and_spwan(self):
        
        # 0,0 17,0 0,35 form the 3 spawn points where the map value is not BLANK but points are accessible while moving
        # we check if all of these points are accessible 
        # we check if the code allows us to go out of boundaries of the map

        V = village.createVillage(1)
        K = spawnKing([1, 0]) 
        K.move('up', V)
        self.assertEqual(K.position, [0, 0])
        K.move('left', V)
        K.move('up', V)
        self.assertEqual(K.position, [0, 0])


        K.position[0] = 17
        K.position[1] = 1
        K.move('left', V)
        K.move('up', V)
        K.move('down', V)
        self.assertEqual(K.position, [17, 0])
        K.move('down', V)
        K.move('left', V)
        self.assertEqual(K.position, [17, 0])

        K.position[0] = 0
        K.position[1] = 34
        K.move('right', V)
        K.move('down', V)
        K.move('up', V)
        self.assertEqual(K.position, [0, 35])
        K.move('up', V)
        K.move('right', V)
        self.assertEqual(K.position, [0, 35])
        
        K.position[0] = 17
        K.position[1] = 35
        K.move('right', V)
        K.move('down', V)
        self.assertEqual(K.position, [17, 35])



with open("output.txt", "w") as File:
    if unittest.TextTestRunner().run(unittest.makeSuite(SimpleTest)).wasSuccessful():
        File.write("True")
    else:
        File.write("False")
