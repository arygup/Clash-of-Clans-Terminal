import points as pt
import collections
from graph import moveWithoutBreakingWalls
import time
# from game import King 
barbarians = []
dragons = []
balloons = []
archers = []
inarchers = []
healers = []

troops_spawned = {
    'barbarian': 0,
    'archer': 0,
    'dragon': 0,
    'balloon': 0,
    'inarcher': 0,
    'healer': 0
}


def clearTroops():
    barbarians.clear()
    dragons.clear()
    balloons.clear()
    archers.clear()
    inarchers.clear()
    healers.clear()
    troops_spawned['healers'] = 0
    troops_spawned['barbarian'] = 0
    troops_spawned['dragon'] = 0
    troops_spawned['balloon'] = 0
    troops_spawned['archer'] = 0
    troops_spawned['inarcher'] = 0



class InArcher:
    def __init__(self, position):
        self.speed = 1
        self.health = 100
        self.max_health = 100
        self.attack = 1
        self.attack_radius = 4
        self.position = position
        self.alive = True
        self.target = None
        self.spawntime = time.perf_counter()

    def isInAttackradius(self,pos):
        r = abs(pos[0] - self.position[0])
        c = abs(pos[1] - self.position[1])
        if(r**2 + c**2 <= self.attack_radius**2):
            return True
        return False

    def move(self, pos, V, type, King):
        if(self.alive == False):
            return
        vmap = V.map
        r = abs(pos[0] - self.position[0])
        c = abs(pos[1] - self.position[1])
        if(self.isInAttackradius(pos)):
            info = vmap[pos[0]][pos[1]]
            if(info == pt.TOWNHALL):
                self.break_building(pos[0], pos[1], V)
                return
            x = int(info.split(':')[1])
            y = int(info.split(':')[2])
            self.break_building(x, y, V)
            return
        elif type == 1:
            flag = 0
            for i in range(self.speed):
                coords = findPathWithoutWall(V.map, self.position, pos)
                if(coords == None):
                    flag = 1
                    break
                self.position = coords
            if(flag == 0):
                return
        if(r == 0):
            if(pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V, King)
                        return
                    self.position[1] += 1
                    if(self.isInAttackradius(pos)):
                        break
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V, King)
                        return
                    self.position[1] -= 1
                    if(self.isInAttackradius(pos)):
                        break
        elif(r > 1):
            if(pos[0] > self.position[0]):
                for i in range(self.speed):
                    r = self.position[0] + 1
                    c = self.position[1]
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V, King)
                        return
                    self.position[0] += 1
                    if(self.position[0] == pos[0] or self.isInAttackradius(pos)):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0] - 1
                    c = self.position[1]
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V, King)
                        return
                    self.position[0] -= 1
                    if(self.position[0] == pos[0] or self.isInAttackradius(pos)):
                        return
        elif(c > 1):
            if(pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V, King)
                        return
                    self.position[1] += 1
                    if(self.position[1] == pos[1] or self.isInAttackradius(pos)):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V, King)
                        return
                    self.position[1] -= 1
                    if(self.position[1] == pos[1] or self.isInAttackradius(pos)):
                        return
        elif(r+c == 2):
            if(pos[0] > self.position[0]):
                for i in range(self.speed):
                    r = self.position[0] + 1
                    c = self.position[1]
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V, King)
                        return
                    self.position[0] += 1
                    if(self.isInAttackradius(pos)):
                        break
            else:
                for i in range(self.speed):
                    r = self.position[0] - 1
                    c = self.position[1]
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V, King)
                        return
                    self.position[0] -= 1
                    if(self.isInAttackradius(pos)):
                        break

    def check_for_walls(self, x, y, vmap):
        if(vmap[x][y] == pt.WALL):
            return True
        return False

    def break_wall(self, x, y, V, King):
        target = V.wall_objs[(x, y)]
        self.attack_target(target, King)

    def break_building(self, x, y, V):
        target = None
        if(V.map[x][y] == pt.TOWNHALL):
            target = V.town_hall_obj
        else:
            all_buildings = collections.ChainMap(
                V.hut_objs, V.cannon_objs, V.wizard_tower_objs)
            target = all_buildings[(x, y)]
        self.attack_target(target, None)

    def attack_target(self, target, King):
        if(self.alive == False):
            return
        target.health -= self.attack
        if target.health <= 0:
            target.health = 0
            target.destroy(King)

    def kill(self):
        self.alive = False
        inarchers.remove(self)

    def deal_damage(self, hit):
        if(self.alive == False):
            return
        self.health -= hit
        if self.health <= 0:
            self.health = 0
            self.kill()

    def rage_effect(self):
        self.speed = self.speed*2
        self.attack = self.attack*2

    def heal_effect(self):
        self.health = self.health*1.5
        if self.health > self.max_health:
            self.health = self.max_health




class Barbarian:
    def __init__(self, position):
        self.speed = 1
        self.health = 100
        self.max_health = 100
        self.attack = 1
        self.position = position
        self.alive = True
        self.target = None

    def move(self, pos, V, type, King):
        if(self.alive == False):
            return
        vmap = V.map
        r = abs(pos[0] - self.position[0])
        c = abs(pos[1] - self.position[1])
        if(r + c == 1):
            info = vmap[pos[0]][pos[1]]
            if(info == pt.TOWNHALL):
                self.break_building(pos[0], pos[1], V)
                return
            x = int(info.split(':')[1])
            y = int(info.split(':')[2])
            self.break_building(x, y, V)
            return
        elif type == 1:
            flag = 0
            for i in range(self.speed):
                coords = findPathWithoutWall(V.map, self.position, pos)
                if(coords == None):
                    flag = 1
                    break
                info = vmap[pos[0]][pos[1]]
                x = 0
                y = 0
                if(info != pt.TOWNHALL):
                    x = int(info.split(':')[1])
                    y = int(info.split(':')[2])
                else:
                    x = pos[0]
                    y = pos[1]
                if(x == coords[0] and y == coords[1]):
                    flag = 1
                    break
                self.position = coords
            if(flag == 0):
                return
        if(r == 0):
            if(pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V, King)
                        return
                    self.position[1] += 1
                    if(abs(pos[1] - self.position[1]) == 1):
                        break
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V, King)
                        return
                    self.position[1] -= 1
                    if(abs(pos[1] - self.position[1]) == 1):
                        break
        elif(r > 1):
            if(pos[0] > self.position[0]):
                for i in range(self.speed):
                    r = self.position[0] + 1
                    c = self.position[1]
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V, King)
                        return
                    self.position[0] += 1
                    if(self.position[0] == pos[0]):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0] - 1
                    c = self.position[1]
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V, King)
                        return
                    self.position[0] -= 1
                    if(self.position[0] == pos[0]):
                        return
        elif(c > 1):
            if(pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V, King)
                        return
                    self.position[1] += 1
                    if(self.position[1] == pos[1]):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V, King)
                        return
                    self.position[1] -= 1
                    if(self.position[1] == pos[1]):
                        return
        elif(r+c == 2):
            if(pos[0] > self.position[0]):
                for i in range(self.speed):
                    r = self.position[0] + 1
                    c = self.position[1]
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V, King)
                        return
                    self.position[0] += 1
            else:
                for i in range(self.speed):
                    r = self.position[0] - 1
                    c = self.position[1]
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V, King)
                        return
                    self.position[0] -= 1

    def check_for_walls(self, x, y, vmap):
        if(vmap[x][y] == pt.WALL):
            return True
        return False

    def break_wall(self, x, y, V, King):
        target = V.wall_objs[(x, y)]
        self.attack_target(target, King)

    def break_building(self, x, y, V):
        target = None
        if(V.map[x][y] == pt.TOWNHALL):
            target = V.town_hall_obj
        else:
            all_buildings = collections.ChainMap(
                V.hut_objs, V.cannon_objs, V.wizard_tower_objs)
            target = all_buildings[(x, y)]
        self.attack_target(target, None)

    def attack_target(self, target, King):
        if(self.alive == False):
            return
        target.health -= self.attack
        if target.health <= 0:
            target.health = 0
            target.destroy(King)

    def kill(self):
        self.alive = False
        barbarians.remove(self)

    def deal_damage(self, hit):
        if(self.alive == False):
            return
        self.health -= hit
        if self.health <= 0:
            self.health = 0
            self.kill()

    def rage_effect(self):
        self.speed = self.speed*2
        self.attack = self.attack*2

    def heal_effect(self):
        self.health = self.health*1.5
        if self.health > self.max_health:
            self.health = self.max_health


class Archer:
    def __init__(self, position):
        self.speed = 1
        self.health = 100
        self.max_health = 100
        self.attack = 1
        self.attack_radius = 4
        self.position = position
        self.alive = True
        self.target = None

    def isInAttackradius(self,pos):
        r = abs(pos[0] - self.position[0])
        c = abs(pos[1] - self.position[1])
        if(r**2 + c**2 <= self.attack_radius**2):
            return True
        return False

    def move(self, pos, V, type, King):
        if(self.alive == False):
            return
        vmap = V.map
        r = abs(pos[0] - self.position[0])
        c = abs(pos[1] - self.position[1])
        if(self.isInAttackradius(pos)):
            info = vmap[pos[0]][pos[1]]
            if(info == pt.TOWNHALL):
                self.break_building(pos[0], pos[1], V)
                return
            x = int(info.split(':')[1])
            y = int(info.split(':')[2])
            self.break_building(x, y, V)
            return
        elif type == 1:
            flag = 0
            for i in range(self.speed):
                coords = findPathWithoutWall(V.map, self.position, pos)
                if(coords == None):
                    flag = 1
                    break
                self.position = coords
            if(flag == 0):
                return
        if(r == 0):
            if(pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V, King)
                        return
                    self.position[1] += 1
                    if(self.isInAttackradius(pos)):
                        break
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V, King)
                        return
                    self.position[1] -= 1
                    if(self.isInAttackradius(pos)):
                        break
        elif(r > 1):
            if(pos[0] > self.position[0]):
                for i in range(self.speed):
                    r = self.position[0] + 1
                    c = self.position[1]
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V, King)
                        return
                    self.position[0] += 1
                    if(self.position[0] == pos[0] or self.isInAttackradius(pos)):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0] - 1
                    c = self.position[1]
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V, King)
                        return
                    self.position[0] -= 1
                    if(self.position[0] == pos[0] or self.isInAttackradius(pos)):
                        return
        elif(c > 1):
            if(pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V, King)
                        return
                    self.position[1] += 1
                    if(self.position[1] == pos[1] or self.isInAttackradius(pos)):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V, King)
                        return
                    self.position[1] -= 1
                    if(self.position[1] == pos[1] or self.isInAttackradius(pos)):
                        return
        elif(r+c == 2):
            if(pos[0] > self.position[0]):
                for i in range(self.speed):
                    r = self.position[0] + 1
                    c = self.position[1]
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V, King)
                        return
                    self.position[0] += 1
                    if(self.isInAttackradius(pos)):
                        break
            else:
                for i in range(self.speed):
                    r = self.position[0] - 1
                    c = self.position[1]
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V, King)
                        return
                    self.position[0] -= 1
                    if(self.isInAttackradius(pos)):
                        break

    def check_for_walls(self, x, y, vmap):
        if(vmap[x][y] == pt.WALL):
            return True
        return False

    def break_wall(self, x, y, V, King):
        target = V.wall_objs[(x, y)]
        self.attack_target(target, King)

    def break_building(self, x, y, V):
        target = None
        if(V.map[x][y] == pt.TOWNHALL):
            target = V.town_hall_obj
        else:
            all_buildings = collections.ChainMap(
                V.hut_objs, V.cannon_objs, V.wizard_tower_objs)
            target = all_buildings[(x, y)]
        self.attack_target(target, None)

    def attack_target(self, target, King):
        if(self.alive == False):
            return
        target.health -= self.attack
        if target.health <= 0:
            target.health = 0
            target.destroy(King)

    def kill(self):
        self.alive = False
        archers.remove(self)

    def deal_damage(self, hit):
        if(self.alive == False):
            return
        self.health -= hit
        if self.health <= 0:
            self.health = 0
            self.kill()

    def rage_effect(self):
        self.speed = self.speed*2
        self.attack = self.attack*2

    def heal_effect(self):
        self.health = self.health*1.5
        if self.health > self.max_health:
            self.health = self.max_health


class Dragon:
    def __init__(self, position):
        self.speed = 1
        self.health = 100
        self.max_health = 100
        self.attack = 5
        self.position = position
        self.alive = True
        

    def move(self, pos, V, King):
        if(self.alive == False):
            return
        vmap = V.map
        r = abs(pos[0] - self.position[0])
        c = abs(pos[1] - self.position[1])
        if(r + c == 1):
            info = vmap[pos[0]][pos[1]]
            if(info == pt.TOWNHALL):
                self.break_building(pos[0], pos[1], V)
                return
            x = int(info.split(':')[1])
            y = int(info.split(':')[2])
            self.break_building(x, y, V)
            return
        elif(r == 0):
            if(pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    self.position[1] += 1
                    if(abs(pos[1] - self.position[1]) == 1):
                        break
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    self.position[1] -= 1
                    if(abs(pos[1] - self.position[1]) == 1):
                        break
        elif(r > 1):
            if(pos[0] > self.position[0]):
                for i in range(self.speed):
                    r = self.position[0] + 1
                    c = self.position[1]
                    self.position[0] += 1
                    if(self.position[0] == pos[0]):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0] - 1
                    c = self.position[1]
                    self.position[0] -= 1
                    if(self.position[0] == pos[0]):
                        return
        elif(c > 1):
            if(pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    self.position[1] += 1
                    if(self.position[1] == pos[1]):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    self.position[1] -= 1
                    if(self.position[1] == pos[1]):
                        return
        elif(r+c == 2):
            if(pos[0] > self.position[0]):
                for i in range(self.speed):
                    r = self.position[0] + 1
                    c = self.position[1]
                    self.position[0] += 1
            else:
                for i in range(self.speed):
                    r = self.position[0] - 1
                    c = self.position[1]
                    self.position[0] -= 1

    def break_building(self, x, y, V):
        target = None
        if(V.map[x][y] == pt.TOWNHALL):
            target = V.town_hall_obj
        else:
            all_buildings = collections.ChainMap(
                V.hut_objs, V.cannon_objs, V.wizard_tower_objs)
            target = all_buildings[(x, y)]
        self.attack_target(target)

    def attack_target(self, target):
        if(self.alive == False):
            return
        target.health -= self.attack
        if target.health <= 0:
            target.health = 0
            target.destroy(None)

    def kill(self):
        self.alive = False
        dragons.remove(self)

    def deal_damage(self, hit):
        if(self.alive == False):
            return
        self.health -= hit
        if self.health <= 0:
            self.health = 0
            self.kill()

    def rage_effect(self):
        self.speed = self.speed*2
        self.attack = self.attack*2

    def heal_effect(self):
        self.health = self.health*1.5
        if self.health > self.max_health:
            self.health = self.max_health


class Balloon:
    def __init__(self, position):
        self.speed = 2
        self.health = 100
        self.max_health = 100
        self.attack = 2
        self.position = position
        self.alive = True
        

    def move(self, pos, V, King):
        if(self.alive == False):
            return
        vmap = V.map
        r = abs(pos[0] - self.position[0])
        c = abs(pos[1] - self.position[1])
        if(r + c == 1):
            info = vmap[pos[0]][pos[1]]
            if(info == pt.TOWNHALL):
                self.break_building(pos[0], pos[1], V)
                return
            x = int(info.split(':')[1])
            y = int(info.split(':')[2])
            self.break_building(x, y, V)
            return
        elif(r == 0):
            if(pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    self.position[1] += 1
                    if(abs(pos[1] - self.position[1]) == 1):
                        break
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    self.position[1] -= 1
                    if(abs(pos[1] - self.position[1]) == 1):
                        break
        elif(r > 1):
            if(pos[0] > self.position[0]):
                for i in range(self.speed):
                    r = self.position[0] + 1
                    c = self.position[1]
                    self.position[0] += 1
                    if(self.position[0] == pos[0]):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0] - 1
                    c = self.position[1]
                    self.position[0] -= 1
                    if(self.position[0] == pos[0]):
                        return
        elif(c > 1):
            if(pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    self.position[1] += 1
                    if(self.position[1] == pos[1]):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    self.position[1] -= 1
                    if(self.position[1] == pos[1]):
                        return
        elif(r+c == 2):
            if(pos[0] > self.position[0]):
                    self.position[0] += 1
            else:
                    self.position[0] -= 1

    def break_building(self, x, y, V):
        target = None
        if(V.map[x][y] == pt.TOWNHALL):
            target = V.town_hall_obj
        else:
            all_buildings = collections.ChainMap(
                V.hut_objs, V.cannon_objs, V.wizard_tower_objs)
            target = all_buildings[(x, y)]
        self.attack_target(target)

    def attack_target(self, target):
        if(self.alive == False):
            return
        target.health -= self.attack
        if target.health <= 0:
            target.health = 0
            target.destroy(None)

    def kill(self):
        self.alive = False
        balloons.remove(self)

    def deal_damage(self, hit):
        if(self.alive == False):
            return
        self.health -= hit
        if self.health <= 0:
            self.health = 0
            self.kill()

    def rage_effect(self):
        self.speed = self.speed*2
        self.attack = self.attack*2

    def heal_effect(self):
        self.health = self.health*1.5
        if self.health > self.max_health:
            self.health = self.max_health



class Healer:
    def __init__(self, position):
        self.speed = 2
        self.health = 250
        self.max_health = 250
        self.attack = 20
        self.position = position
        self.alive = True
        self.heal_radius = 1

    def move(self, tar, V, King):
        troops = barbarians+ archers + dragons + balloons + inarchers #+ healers
        for troop in troops:
            if (troop.position[0] - self.position[0])**2 + (troop.position[1] - self.position[1])**2 <= self.heal_radius**2:
                self.attack_target(troop)
    
        if King.alive == True:
            if(King.position[0] - self.position[0])**2 + (King.position[1] - self.position[1])**2 <= self.heal_radius**2:
                self.attack_target(King)

        if tar is None:
           return
            
        pos = tar.position 
        if(self.alive == False):
            return
        vmap = V.map
        r = abs(pos[0] - self.position[0])
        c = abs(pos[1] - self.position[1])
        if(r + c == 1):
            info = vmap[pos[0]][pos[1]]
            # if(info == pt.TOWNHALL):
            #     self.break_building(pos[0], pos[1], V)
            #     return
            # x = int(info.split(':')[1])
            # y = int(info.split(':')[2])
            self.attack_target(tar)
            return
        elif(r == 0):
            if(pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    self.position[1] += 1
                    if(abs(pos[1] - self.position[1]) == 1):
                        break
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    self.position[1] -= 1
                    if(abs(pos[1] - self.position[1]) == 1):
                        break
        elif(r > 1):
            if(pos[0] > self.position[0]):
                for i in range(self.speed):
                    r = self.position[0] + 1
                    c = self.position[1]
                    self.position[0] += 1
                    if(self.position[0] == pos[0]):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0] - 1
                    c = self.position[1]
                    self.position[0] -= 1
                    if(self.position[0] == pos[0]):
                        return
        elif(c > 1):
            if(pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    self.position[1] += 1
                    if(self.position[1] == pos[1]):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    self.position[1] -= 1
                    if(self.position[1] == pos[1]):
                        return
        elif(r+c == 2):
            if(pos[0] > self.position[0]):
                    self.position[0] += 1
            else:
                    self.position[0] -= 1

    def attack_target(self, target):
        if(self.alive == False):
            return
        if(id(target) == id(self)):
            return
        if target.health >= target.max_health:
            return
        if target.health + self.attack > target.max_health:
            target.health += target.max_health-target.health
        target.health += self.attack

    def kill(self):
        self.alive = False
        healers.remove(self)

    def deal_damage(self, hit):
        if(self.alive == False):
            return
        self.health -= hit
        if self.health <= 0:
            self.health = 0
            self.kill()

    def rage_effect(self):
        self.speed = self.speed*2
        self.attack = self.attack*2

    def heal_effect(self):
        self.health = self.health*1.5
        if self.health > self.max_health:
            self.health = self.max_health




def spawnBarbarian(pos):
    if(pt.troop_limit['barbarian'] <= troops_spawned['barbarian']):
        return

    # convert tuple to list
    pos = list(pos)
    barb = Barbarian(pos)
    troops_spawned['barbarian'] += 1
    barbarians.append(barb)

def spawnArcher(pos):
    if(pt.troop_limit['archer'] <= troops_spawned['archer']):
        return

    # convert tuple to list
    pos = list(pos)
    archer = Archer(pos)
    troops_spawned['archer'] += 1
    archers.append(archer)

def spawnInArcher(pos):
    if(pt.troop_limit['inarcher'] <= troops_spawned['inarcher']):
        return

    # convert tuple to list
    pos = list(pos)
    inarcher = InArcher(pos)
    troops_spawned['inarcher'] += 1
    inarchers.append(inarcher)

def spawnDragon(pos):
    if(pt.troop_limit['dragon'] <= troops_spawned['dragon']):
        return

    # convert tuple to list
    pos = list(pos)
    dr = Dragon(pos)
    troops_spawned['dragon'] += 1
    dragons.append(dr)

def spawnBalloon(pos):
    if(pt.troop_limit['balloon'] <= troops_spawned['balloon']):
        return

    # convert tuple to list
    pos = list(pos)
    bal = Balloon(pos)
    troops_spawned['balloon'] += 1
    balloons.append(bal)

def spawnHealer(pos):
    if(pt.troop_limit['healer'] <= troops_spawned['healer']):
        return

    # convert tuple to list
    pos = list(pos)
    bal = Healer(pos)
    troops_spawned['healer'] += 1
    healers.append(bal)

def move_barbarians(V,type, King):
    if(type == 1):
        for barb in barbarians:
            if(barb.alive == False):
                continue
            if barb.target != None:    
                if(V.map[barb.target[0]][barb.target[1]] == pt.BLANK):
                    barb.target = None

            if(barb.target == None):
                barb.target = search_for_closest_building(barb.position, V.map, 0)
            if(barb.target == None):
                continue
            barb.move(barb.target, V, type, King)
    elif(type == 2):
        for barb in barbarians:
            if(barb.alive == False):
                continue
            closest_building = search_for_closest_building(barb.position, V.map, 0)
            if(closest_building == None):
                continue
            barb.move(closest_building, V, type, King)

def move_archers(V,type, King):
    if(type == 1):
        for archer in archers:
            if(archer.alive == False):
                continue
            if archer.target != None:
                if(V.map[archer.target[0]][archer.target[1]] == pt.BLANK):
                    archer.target = None
            if(archer.target == None):
                archer.target = search_for_closest_building(archer.position, V.map, 0)
            if(archer.target == None):
                continue
            archer.move(archer.target, V,type, King)
    elif(type == 2):
        for archer in archers:
            if(archer.alive == False):
                continue
            closest_building = search_for_closest_building(archer.position, V.map, 0)
            if(closest_building == None):
                continue
            archer.move(closest_building, V, type, King)

def move_inarchers(V,type, King):
    if(type == 1):
        for inarcher in inarchers:
            if(inarcher.alive == False):
                continue
            if inarcher.target != None:
                if(V.map[inarcher.target[0]][inarcher.target[1]] == pt.BLANK):
                    inarcher.target = None
            if(inarcher.target == None):
                inarcher.target = search_for_closest_building(inarcher.position, V.map, 0)
            if(inarcher.target == None):
                continue
            inarcher.move(inarcher.target, V,type, King)
    elif(type == 2):
        for inarcher in inarchers:
            if(inarcher.alive == False):
                continue
            closest_building = search_for_closest_building(inarcher.position, V.map, 0)
            if(closest_building == None):
                continue
            inarcher.move(closest_building, V, type, King)

def move_dragons(V, King):
    for dr in dragons:
        if(dr.alive == False):
            continue
        closest_building = search_for_closest_building(dr.position, V.map, 0)
        if(closest_building == None):
            continue
        dr.move(closest_building, V, King)

def move_balloons(V, King):
    for bal in balloons:
        if(bal.alive == False):
            continue
        closest_building = search_for_closest_building(bal.position, V.map, 1)
        if(closest_building == None):
            continue
        bal.move(closest_building, V, King)


####################
def move_healers(V, King):
    for bal in healers:
        if(bal.alive == False):
            continue
        closest_building = search_for_closest_troop(bal.position, V.map, 1, King)
        # if(closest_building == None):
        #     if King.alive == True:
        #         closest_building = King
                
        bal.move(closest_building, V, King)
####################




def search_for_closest_building(pos, vmap, prioritized):
    closest_building = None
    closest_dist = 10000
    flag = 0
    for i in range(len(vmap)):
        for j in range(len(vmap[i])):
            item = vmap[i][j].split(':')[0]
            if(prioritized == 0):
                if (item == pt.HUT or item == pt.CANNON or item == pt.TOWNHALL or item == pt.WIZARD_TOWER):
                    dist = abs(i - pos[0]) + abs(j - pos[1])
                    if(dist < closest_dist):
                        flag = 1
                        closest_dist = dist
                        closest_building = (i, j)
            else:
                if (item == pt.CANNON or item == pt.WIZARD_TOWER):
                    dist = abs(i - pos[0]) + abs(j - pos[1])
                    if(dist < closest_dist):
                        flag = 1
                        closest_dist = dist
                        closest_building = (i, j)
    if(flag == 0 and prioritized == 0):
        return None
    elif(flag == 0 and prioritized == 1):
        return search_for_closest_building(pos, vmap, 0)
    else:
        return closest_building
    

def search_for_closest_troop(pos, vmap, prioritized, King):
    troops = barbarians+ archers + dragons + balloons + inarchers
    closest_building = None
    closest_dist = 10000
    if King.alive == True:
            closest_dist = abs(King.position[0] - pos[0]) + abs(King.position[1] - pos[1])
            closest_building = King
    for troop in troops:
        dist = abs(troop.position[0] - pos[0]) + abs(troop.position[1] - pos[1])
        if(dist < closest_dist):
                        closest_dist = dist
                        closest_building = troop
    return closest_building


def findPathWithoutWall(grid,start,end):
    graph = []
    for row in grid:
        row2 = []
        for col in row:
            if(col == pt.BLANK):
                row2.append(0) # 0 means walkable
            else:
                row2.append(1) # 1 means not walkable
        graph.append(row2)
    graph[start[0]] [start[1]] = 2 # mark start as 2
    graph[end[0]] [end[1]] = 3 # mark end as 3

    coords = moveWithoutBreakingWalls(graph,start)
    if coords == None:
        return None
    else:
        return list(coords)
   