#Canali Federico
#SPACE INVADERS V.2

import pygame, time, random

class Actor():
    def move(self):
        raise NotImplementedError('Abstract method')

    def collide(self, other: 'Actor'):
        raise NotImplementedError('Abstract method')

    def position(self) -> (int, int, int, int):
        raise NotImplementedError('Abstract method')

    def symbol(self) -> (int, int, int, int):
        raise NotImplementedError('Abstract method')
    
class Effetto():

    def anima(self):
        raise NotImplementedError('Abstract method')

    def position(self) -> (int, int, int, int):
        raise NotImplementedError('Abstract method')

    def symbol(self) -> (int, int, int, int):
        raise NotImplementedError('Abstract method')

class Arena():
    def __init__(self, width: int, height: int):
        self._w, self._h = width, height
        self._actors = []
        self._effetti = []
        self._punteggio = 0
        self._ninv = 50

    def add(self, a: Actor):
        if a not in self._actors:
            self._actors.append(a)

    def add_effetto(self, a: Effetto):
        if a not in self._effetti:
            self._effetti.append(a)

    def remove(self, a: Actor):
        if a in self._actors:
            self._actors.remove(a)

    def remove_effetto(self,a: Effetto):
        if a in self._effetti:
            self._effetti.remove(a)

    def move_all(self):
        actors = list(reversed(self._actors))
        for a in actors:
            previous_pos = a.position()
            a.move()
            if a.position() != previous_pos:
                for other in actors:
                    if other is not a and self.check_collision(a, other):
                            a.collide(other)
                            other.collide(a)

        for a in self._effetti:
            a.anima()

        if self._ninv <= 0:
            Hai_Vinto(self._punteggio)

    def check_collision(self, a1: Actor, a2: Actor) -> bool:
        x1, y1, w1, h1 = a1.position()
        x2, y2, w2, h2 = a2.position()
        return (y2 < y1 + h1 and y1 < y2 + h2
            and x2 < x1 + w1 and x1 < x2 + w2
            and a1 in self._actors and a2 in self._actors)

    def actors(self) -> list:
        return list(self._actors)

    def size(self) -> (int, int):
        return (self._w, self._h)

    def draw_all(self):
        for el in self._actors:
            disegno = sprites.subsurface(el.symbol())
            screen.blit(disegno, el.position())

        if (round(time.time()*15)) %2 == 0:
            for el in self._effetti:
                disegno = sprites.subsurface(el.symbol())
                screen.blit(disegno, el.position())

    def get_punteggio(self):
        return self._punteggio

    def add_punti(self,punti):
        self._punteggio += punti

    def set_ninv(self):
        self._ninv -= 1

class Invader(Actor):
    def __init__(self, arena, x, y, spazio_inv, bordo,tipo):
        self._x = x
        self._y = y
        self._dx = 1
        self._dy = 2.5
        self._larg = 22
        self._alt = 16
        self._tipo = tipo
        self._prob = 600
        self._danno = 300
        self._vita = 25 * (tipo+1)
        self._punti = 100 * (tipo+1)
        self._spazio_inv = spazio_inv
        self._bordo = bordo
        self._arena = arena
        arena.add(self)

    def position(self):
        return self._x, self._y, self._larg, self._alt

    def move(self):
        aw, ah = self._arena.size()
        if self._x + self._larg > self._spazio_inv * (self._x // self._spazio_inv) + self._bordo or self._x < self._spazio_inv * ((self._x // self._spazio_inv) - 1) + self._bordo:
            self._dx = -self._dx
            self._y += self._dy
        self._x += self._dx
        if self._y + self._alt > ah:
            Game_Over(self._arena.get_punteggio())

        self.spara()

    def symbol(self) -> (int, int, int, int):

        if self._tipo == 0:
            if (round(time.time()*1.5)) %2 == 0:
                return 148,224,self._larg +2,self._alt
            else:
                return 180,224,self._larg+2,self._alt


        elif self._tipo == 1:
            if (round(time.time()*1.5)) %2 == 0:
                return 75,223,self._larg,self._alt
            else:
                return 108,223,self._larg,self._alt
        else:
            if (round(time.time()*1.5)) %2 == 0:
                return 41,223,self._larg-6,self._alt
            else:
                return 8,223,self._larg-6,self._alt

    def collide(self, other: 'Actor'):
        if isinstance(other, Proiettile_Buono):
            self._vita -= other.get_danno()
            if self._vita <= 0:
                self._arena.add_punti(self._punti)
                self._arena.set_ninv()
                Esplosione(self._arena,self._x,self._y,1)
                self._arena.remove(self)
        if isinstance(other, Player):
            self._arena.remove(self)
        if isinstance(other, Scudo):
            self._arena.remove(self)

    def spara(self):
        if random.randrange(self._prob) == 1:
            Proiettile_Cattivo(arena,self._x + self._larg //2,self._y + self._alt)

    def get_danno(self):
        return self._danno

class Player(Actor):
    def __init__(self, arena, x, y):

        self._y = y
        self._larg = 26
        self._alt = 16
        self._x = x -self._larg //2
        self._spawn = self._x
        self._dx = 0
        self._bordo = 50
        self._speed = 5
        self._ricarica = 0.35
        self._prima = 0
        self._vite = 3
        self._arena = arena
        arena.add(self)

    def move(self):
        arena_w, arena_h = self._arena.size()

        self._x += self._dx
        if self._x < self._bordo:
            self._x = self._bordo
        elif self._x > arena_w - self._larg - self._bordo:
            self._x = arena_w - self._larg - self._bordo

    def go_left(self):
        self._dx= -self._speed

    def go_right(self):
        self._dx= +self._speed

    def stay(self):
        self._dx = 0

    def spara(self):
        if time.time()  >= self._prima+ self._ricarica:
            Proiettile_Buono(self._arena,self._x + self._larg // 2,self._y)
            Fiammata(self._arena,self._x+8,self._y-16,0.15)
            self._prima = time.time()

    def collide(self, other):
        if isinstance(other,Invader) or isinstance(other,Proiettile_Cattivo):
            screen.fill(ROSSO)

            pygame.display.flip()
            clock.tick(10)
            self._vite -= 1
            Esplosione(self._arena,self._x + 10,self._y + 5,1)
            self._x = self._spawn
            if self._vite < 0:
                Game_Over(self._arena.get_punteggio())

    def position(self):
        return self._x, self._y, self._larg, self._alt

    def symbol(self):
        return 278,226, self._larg, self._alt

    def get_vite(self):
        return self._vite

    def set_ricarica(self,nuova):
        self._ricarica = nuova

class Proiettile_Buono(Actor):
    def __init__(self,arena,x,y):
        self._x = x
        self._y = y
        self._larg = 4
        self._alt = 12
        self._speed = 10
        self._danno = 10
        self._arena = arena
        arena.add(self)

    def move(self):
        self._y -= self._speed
        if self._y <0:
            self._arena.remove(self)

    def collide(self, other):
        if isinstance(other, Invader):
            self._arena.remove(self)
        if isinstance(other, Scudo):
            self._arena.remove(self)

    def get_danno(self):
        return self._danno

    def position(self):
        return self._x, self._y, self._larg, self._alt

    def symbol(self):
        return 200, 1488, self._larg, self._alt

class Proiettile_Cattivo(Actor):
    def __init__(self,arena,x,y):
        self._x = x
        self._y = y
        self._larg = 4
        self._alt = 16
        self._speed = 10
        self._danno = 20
        self._arena = arena
        arena.add(self)

    def move(self):
        aw,ah = self._arena.size()
        self._y += self._speed
        if self._y > ah:
            self._arena.remove(self)

    def collide(self, other):
        if isinstance(other, Player):
            self._arena.remove(self)
        if isinstance(other, Scudo):
            self._arena.remove(self)

    def position(self):
        return self._x, self._y, self._larg, self._alt

    def symbol(self):
        return 216, 1491, self._larg, self._alt

    def get_danno(self):
        return self._danno

class Scudo(Actor):
    def __init__(self, arena, x, y):
        self._x = x
        self._y = y
        self._larg = 44
        self._alt = 32
        self._vita = 200
        self._vitamax = self._vita
        self._arena = arena
        arena.add(self)

    def position(self):
        return self._x, self._y, self._larg, self._alt

    def move(self):
        pass

    def symbol(self) -> (int, int, int, int):
        if self._vita < self._vitamax / 4:
            return 374, 209, self._larg, self._alt
        elif self._vita < self._vitamax / 2:
            return 481, 263, self._larg, self._alt
        elif self._vita < self._vitamax / 4*3:
            return 481, 208, self._larg, self._alt
        else:
            return 317, 211, self._larg, self._alt

    def collide(self, other: 'Actor'):
        if isinstance(other, Proiettile_Cattivo) or isinstance(other, Invader):
            self._vita -= other.get_danno()
            if self._vita <= 0:
                Esplosione_Grande(arena,self._x- 25,self._y - 10,2)
                arena.remove(self)

class Astronave(Actor):
    def __init__(self, arena, x, y,bordo):
        self._x = x
        self._y = y
        self._bordo = bordo
        self._dx = 4
        self._larg = 48
        self._alt = 21
        self._ricarica = 10
        self._inizio_effetto = 0
        self._durata_effetto = 3
        self._ultimo = 0
        self._punti = 150
        self._attivato = False
        self._arena = arena
        arena.add(self)

    def position(self):
        return self._x, self._y, self._larg, self._alt

    def move(self):
        aw,ah = arena.size()
        if self._x < self._bordo or self._x + self._larg> aw - self._bordo:
            self._dx = -self._dx

        self._x += self._dx

        if self._attivato:
            if time.time() > self._inizio_effetto + self._durata_effetto:
                player.set_ricarica(0.35)

    def symbol(self) -> (int, int, int, int):
        if time.time()  >= self._ultimo + self._ricarica:
            return 216,222,self._larg,self._alt
        else:
            return 0,0,1,1

    def collide(self, other: 'Actor'):
        if time.time()  >= self._ultimo + self._ricarica:
            if isinstance(other, Proiettile_Buono):
                self._ultimo = time.time()
                self._arena.add_punti(self._punti)
                Esplosione(self._arena,self._x,self._y,1)
                player.set_ricarica(0.1)
                self._attivato = True
                self._inizio_effetto  = time.time()

class Esplosione(Effetto):
    def __init__(self,arena,x,y,tempo):
        self._x = x
        self._y = y
        self._larg = 26
        self._alt = 16
        self._tempo = tempo
        self._nato = time.time()
        self._arena = arena
        arena.add_effetto(self)

    def anima(self):
        if time.time()  >= self._nato+ self._tempo:
            self._arena.remove_effetto(self)

    def position(self):
        return self._x, self._y, self._larg, self._alt

    def symbol(self) -> (int, int, int, int):
        return 438,274,self._larg,self._alt

class Esplosione_Grande(Effetto):
    def __init__(self,arena,x,y,tempo):
        self._x = x
        self._y = y
        self._larg = 104
        self._alt = 64
        self._tempo = tempo
        self._nato = time.time()
        self._arena = arena
        arena.add_effetto(self)

    def anima(self):
        if time.time()  >= self._nato+ self._tempo:
            self._arena.remove_effetto(self)

    def position(self):
        return self._x, self._y, self._larg, self._alt

    def symbol(self) -> (int, int, int, int):
        return 481,1138,self._larg,self._alt

class Fiammata(Effetto):
    def __init__(self,arena,x,y,tempo):
        self._x = x
        self._y = y
        self._larg = 8
        self._alt = 16
        self._tempo = tempo
        self._nato = time.time()
        self._arena = arena
        arena.add_effetto(self)

    def anima(self):
        if time.time()  >= self._nato+ self._tempo:
            self._arena.remove_effetto(self)

    def position(self):
        return self._x, self._y, self._larg, self._alt

    def symbol(self) -> (int, int, int, int):
        return 371,273,self._larg,self._alt

def Crea_Invaders(num):
    aw,ah = arena.size()
    spazio_inv = 50
    bordo = 50
    ix = 0
    riga = 0
    tipo = 2
    for i in range(num):
        if i >= 10:
            tipo = 1
        if i >=30:
            tipo = 0
        Invader(arena ,(ix % (aw - bordo * 2)) + bordo, 60 + riga * 40, spazio_inv, bordo,tipo)
        ix += spazio_inv
        riga = (i+1) // ((aw  - bordo * 2) // spazio_inv)

def Crea_Scudi():
    larg_scudo = 44
    aw,ah = arena.size()
    for i in range(4):
        Scudo(arena, aw // 5 *i + (aw - (aw // 5*3 + larg_scudo)) // 2, ah // 10 * 7)

def Crea_Astronave():
    Astronave(arena,100,20,50)

def Disegna_Interfaccia(vite):
    x, y, larg, alt = player.position()
    aw, ah = arena.size()
    surface = font.render(str(vite + 1), True, BIANCO)
    screen.blit(surface, (20, ah - surface.get_height() - 20))

    for i in range(vite):
        disegno = sprites.subsurface(player.symbol())
        screen.blit(disegno , (50 + (i * (larg+5)),ah//12 *11))

    surface = font.render('Score: '+ str(arena.get_punteggio()), True, BIANCO)
    screen.blit(surface, (aw//2, ah - surface.get_height() - 20))

def Game_Over(punteggio):
    screen.fill(NERO)

    aw, ah = arena.size()

    surface = font.render('GAME OVER!', True, ROSSO)
    screen.blit(surface, (aw // 2 - surface.get_width() // 2, 200))

    surface = font.render('Score: ' + str(punteggio), True, BIANCO)
    screen.blit(surface, (aw // 2 - surface.get_width() // 2,300))

    pygame.display.flip()
    clock.tick(0.5)
    pygame.quit()
    quit()

def Hai_Vinto(punteggio):
    screen.fill(NERO)

    aw, ah = arena.size()

    surface = font.render('HAI VINTO!', True, ROSSO)
    screen.blit(surface, (aw // 2 - surface.get_width() // 2, 200))

    surface = font.render('Score: ' + str(punteggio), True, BIANCO)
    screen.blit(surface, (aw // 2 - surface.get_width() // 2, 300))

    pygame.display.flip()
    clock.tick(0.3)
    pygame.quit()
    quit()

if __name__ == "__main__":
    W,H = 600,600

    pygame.init()
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()

    NERO = (0,0,0)
    BIANCO = (255,255,255)
    ROSSO =(255,0,0)
    VERDE = (0,255,0)

    chiudi = False
    go_right = False
    go_left = False
    sparando = False

    sprites = pygame.image.load('invaders-transp.png')
    font = pygame.font.SysFont('invaders', 48)

    arena  = Arena(W,H)
    player = Player(arena,W//2,5 * H//6)
    Crea_Invaders(50)
    Crea_Scudi()
    Crea_Astronave()


    while not chiudi:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                chiudi  = True
                print("Uscito")
                continue
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
                go_right = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
                go_left = True
            if e.type == pygame.KEYUP and e.key == pygame.K_RIGHT:
                go_right = False
            if e.type == pygame.KEYUP and e.key == pygame.K_LEFT:
                go_left = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                sparando = True
            if e.type == pygame.KEYUP and e.key == pygame.K_SPACE:
                sparando = False

        if go_right:
            player.go_right()

        if go_left:
            player.go_left()

        if (not go_left and not go_right) or  (go_left and go_right):
            player.stay()

        if sparando:
            player.spara()

        screen.fill(NERO)

        arena.move_all()
        arena.draw_all()

        Disegna_Interfaccia(player.get_vite())

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
