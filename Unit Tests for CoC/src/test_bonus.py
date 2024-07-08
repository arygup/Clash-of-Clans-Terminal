import unittest
import village
from king import  *
import points as pt


class SimpleTest(unittest.TestCase):
    def test_alive(self):
        #init king
        V = village.createVillage(1)
        K = spawnKing([17, 28])  # since archer tower at 17,27
        K.facing = "left"
        t = V.get_target(17,27)
        x = t.health
        K.kill()
        # should not be able to attack after death therefore health remains the same
        K.attack_target(t, K.attack)
        self.assertEqual(t.health, x)
    
    def test_healthisdec(self):
        V = village.createVillage(1)
        K = spawnKing([17, 28])  # since archer tower at 17,27
        K.facing = "left"
        t = V.get_target(17,27)
        x = t.health
        # post attack the health must decrease to min(Health - Attack, 0)
        K.attack_target(t, K.attack)
        if(x <= K.attack):
            self.assertEqual(t.health, 0)
        self.assertEqual(t.health, x-K.attack)

    def test_negativehealth(self):
        # to check if the health gets set to 0 and not a negative value, we update the attack value and attack the object making sure the health gets sub zero and then reset to 0
        V = village.createVillage(1)
        K = spawnKing([17, 28])  # since archer tower at 17,27
        K.facing = "left"
        t = V.get_target(17,27)
        x = t.health
        K.attack_target(t, x+5)
        self.assertEqual(t.health, 0)
        # self.assertFalse(t.destroyed)

with open("output_bonus.txt", "w") as File:
    if unittest.TextTestRunner().run(unittest.makeSuite(SimpleTest)).wasSuccessful():
        File.write("True")
    else:
        File.write("False")