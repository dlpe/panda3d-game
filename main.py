#!/usr/bin/python


import os
import sys
import threading
import time
from datetime import datetime
from math import pi, sin, cos, radians, sqrt
from functools import wraps

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from panda3d.core import DirectionalLight, WindowProperties, Filename
from panda3d.core import CollisionHandlerFloor, CollisionPlane, CollisionBox, CollisionNode, CollisionRay, Plane, Vec3, Point3, CollisionHandlerQueue, CollisionTraverser, CollisionSphere, CollisionHandlerPusher, TextNode, Fog
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import DGG, DirectSlider, DirectWaitBar
from direct.particles.ParticleEffect import ParticleEffect
from direct.gui.OnscreenImage import OnscreenImage

FORWARD = 'w'
BACKWARDS = 's'
LEFT = 'a'
RIGHT = 'd'
ATTACK_BTN = 'f'

# Load stuff
PATH = os.path.dirname(__file__)
MODELS_PATH = os.path.join(PATH, 'models')
ENV = os.path.join(MODELS_PATH, 'environment')
SCALE_TXT = 'scale'

# Animacoes
T_POSE = 't-pose'

IDLE = 'idle'
FIGHT = 'fight-stand'
WALK = 'walk'
TURNR = 'turn-right'
TURNL = 'turn-left'
ATTACK = 'attack'
HIT = 'hit'
DEATH = 'death'

ANIM = [
    IDLE,
    FIGHT,
    WALK,
    #TURNR,
    #TURNL,
    ATTACK,
    #HIT,
    #DEATH
]

TIME = 30.0
BOUNDARY = 40.0
ATTACK_PWR = 10.0

class Model(object):
    PACE = 1.0
    def __init__(self, name, game, pos = None):
        self.name = name
        self.game = game
        path = os.path.join(MODELS_PATH, name)
        anim = {}
        self.pace = Model.PACE
        self.is_moving = False

        # Init animacoes
        for a in ANIM:
            anim[a] = os.path.join(MODELS_PATH, name, a)
        try:
            print anim
            self.actor = Actor(
                os.path.join(path, T_POSE), anim)

            scale = open(os.path.join(path, SCALE_TXT)).read()
            scale = float(scale)
            self.actor.setScale(scale, scale, scale)

        except IOError as ie:
            print 'Could\'t load character %s due to: %s' % (name, ie.message)
            raise
        else:
            self.actor.reparentTo(game.render)
            box = CollisionBox(self.actor.getPos(), 1, 1, 1)
            fromObject = self.actor.attachNewNode(CollisionNode('cnode'))
            fromObject.node().addSolid(box)
            fromObject.node().addSolid(CollisionRay(0, 0, 0, 0, 0, -1))

            self.game.lifter.addCollider(fromObject, self.actor)

            self.traverser = CollisionTraverser('traverser name')
            self.queue = CollisionHandlerQueue()
            self.traverser.addCollider(fromObject, self.queue)
            self.traverser.traverse(game.render)
 
            # Be natural
            self.stand()

    def getActor(self):
        return self.actor

    def blend(self, anim1, anim2, p1 = 0.5, p2 = 0.5):
        self.actor.enableBlend()
        self.actor.setControlEffect(anim1, p1)
        self.actor.setControlEffect(anim2, p2)
        self.actor.loop(anim1)
        self.actor.loop(anim2)

    def disableBlend(self):
        self.actor.disableBlend()

    def stand(self):
        self.actor.loop(IDLE)
    def fight(self):
        self.actor.loop(FIGHT)
    def walk(self, direction = None):
        self.actor.loop(WALK)
        threading.Thread(target = self.move).start()
    def turn(self, direction):
        self.actor.loop(
            TURNR if direction == RIGHT else (
                TURNL if direction == LEFT else None))

    def close(self, direction = None):
        # TODO: move
        self.actor.loop(CLOSE)
    def attack(self, direction = None):
        # TODO: move
        self.actor.loop(ATTACK)
        self.is_moving = False

    def hit(self):
        # TODO: move
        self.actor.loop(HIT)
    def die(self, direction = None):
        # TODO: move
        self.actor.loop(DEATH)

    def move(self):
        self.is_moving = True
        delta = datetime.now()
        while self.is_moving:
            pos = self.getActor().getPos()
            hpr = self.getActor().getHpr()

            co = cos(radians(hpr[0]))
            se = sin(radians(hpr[0]))

            # Movimenta na direcao do Model
            x = pos[0] + (se * self.pace)
            y = pos[1] - (co * self.pace)

            if x > BOUNDARY: x = BOUNDARY
            if y > BOUNDARY: y = BOUNDARY
            if x < -BOUNDARY: x = -BOUNDARY
            if y < -BOUNDARY: y = -BOUNDARY

            if not self.colliding(x,y):
                self.getActor().setPos(x, y, pos[2])

            #for car in self.game.cars:
            #    car['life_bar'].setHpr(hpr)

            time.sleep(0.1)

            print self.getActor().getPos()
            print self.queue.getEntries()

    # Provisory method. Colliders to be implemented when time :(
    def provisoryCollide(self):
        self.colliders = open('.rocks', 'r+').read().splitlines()
        self.colliders += open('car/list', 'r+').read().splitlines()
        self.colliders = [tuple(x.split()) for x in self.colliders]

    def colliding(self, x, y):
        for c in self.colliders:
            distance = sqrt((float(x) - float(c[0]))**2 + (float(y) - float(c[1]))**2)
            if distance < float(c[2]):
                print c
                return True
        return False


class Player(Model, DirectObject): 
    def __init__(self, name, game, pos = None):
        Model.__init__(self, name, game, pos)
        self.accept(FORWARD, self.forward)
        self.accept(FORWARD + '-up', self.forward_up)
        self.accept(BACKWARDS, self.backwards)
        self.accept(BACKWARDS + '-up', self.backwards_up)
        self.accept(LEFT, self.left)
        self.accept(LEFT + '-up', self.left_up)
        self.accept(RIGHT, self.right)
        self.accept(RIGHT + '-up', self.right_up)
        self.accept(ATTACK_BTN, self.attack)
        self.accept(ATTACK_BTN + '-up', self.attack_up)

        self.provisoryCollide()
        self.punch = self.game.base.loader.loadSfx("punch.ogg")
        self.explode = self.game.base.loader.loadSfx("explosion.ogg")

    def forward(self):
        self.walk()
    def backwards(self):
        print "key "
    def right(self):
        print "key "
    def left(self):
        print "key "
    def forward_up(self):
        self.stand()
        self.is_moving = False
    def backwards_up(self):
        pass
    def right_up(self):
        pass
    def left_up(self):
        pass
    def attack(self):
        self.attacking = True
        Model.attack(self)
        for i, car in enumerate(self.game.cars):
            if distance(car['pos'], self.getActor().getPos()) < car['pos'][2]:
                threading.Thread(target=timed_call([self.hit], t = 1, args = i)).start()

    def attack_up(self):
        self.attacking = False
        self.stand()

    def hit(self, i):
        car = self.game.cars[i]
        while self.attacking and self.game.running:
            print car
            self.punch.play()
            car['life'] -= ATTACK_PWR
            if car['life'] <= 0.0:
                self.game.loadParticleConfig('fireish.ptf', car['model'])
                self.explode.play()
                time.sleep(2)
                self.game.loadParticleConfig('smokering.ptf', car['model'])
                time.sleep(5)
                car['model'].hide()
                self.game.cars_pos = [x for x in self.game.cars_pos if distance(x, car['pos']) > 0]
                print self.game.cars_pos

                #self.game.add_cars(cars_pos=self.game.cars_pos)
                self.attacking = False
                if self.game.running:
                    self.game.end_game(won=True)

            time.sleep(1)

def timed_call(funcs, t=0, args = None):
    def f():
        time.sleep(t)
        for func in funcs:
            print 'calling %s' % func
            func(args)
    return f

def distance(a, b):
    return sqrt((float(a[0]) - float(b[0]))**2 + (float(a[1]) - float(b[1]))**2)

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.base = self
        self.cars = []
        self.setup()

        # Load the environment model.
        self.scene = self.loader.loadModel(ENV)
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)
        self.lifter = CollisionHandlerFloor()

        # Create Ambient Light
        self.light = DirectionalLight('ambientLight')
        self.light.setColor((1, 1, 1, 1))
        self.light = render.attachNewNode(self.light)

        myFog = Fog("Fog Name")
        myFog.setColor(0.4,0.2,0.2)
        myFog.setExpDensity(0.01)
        render.setFog(myFog)

        p = self.load_characters()
        self.camera.reparentTo(self.player.getActor())

        rock = CollisionBox((-22.0, 7, 0), 5, 5, 5)
        cnodePath = self.scene.attachNewNode(CollisionNode('cnode'))
        cnodePath.node().addSolid(rock)

        fromObject = self.scene.attachNewNode(CollisionNode('colNode'))
        fromObject.node().addSolid(CollisionSphere(-22, 7, 0, 20))
 
        self.pusher = CollisionHandlerPusher()
        self.pusher.addCollider(fromObject, self.scene)

        self.add_cars()

        threading.Thread(target=self.decrease_timer).start()

        self.theme_music = self.base.loader.loadSfx("stft.ogg")
        self.theme_music.setLoop(True)
        self.theme_music.play()

    def decrease_timer(self):
        self.time_left = TIME
        previous = datetime.now()
        self.textObject = OnscreenText(text = 'Time Left: %s' % TIME, pos = (0.85,0.85),
            scale = 0.13,fg=(1,0,0,1),align=TextNode.ACenter, mayChange=1)
        while self.time_left > 0 and self.running:
            if (datetime.now() - previous).total_seconds() < 1.0:
                time.sleep(0.5)
                continue
            
            previous = datetime.now()
            timer_text = 'Time left: %s' % self.time_left
            self.textObject.setText(timer_text)
            self.time_left = self.time_left - 1
        if self.running:
            self.end_game()

    def end_game(self, won=False):
        self.running = False
        myFog = Fog("Fog Name")
        myFog.setColor(0,0,0)
        myFog.setExpDensity(1)
        render.setFog(myFog)
        self.theme_music.stop()

        version = 'happy' if won else 'sad'
        imageObject = OnscreenImage(image = '%s.jpg' % version, pos = (0, 0, 0))
        self.theme_music = self.base.loader.loadSfx('%s.ogg' % version)
        self.theme_music.play()
        self.textObject.setText('')
        newTextObject = OnscreenText(text = 'You %s!' % ('win' if won else 'lose'), 
            pos=(0,0), scale = 0.13,fg=(1,0,0,1),align=TextNode.ACenter, mayChange=1)


        #time.sleep(6)
        sys.exit(0)
 

    # Goal temporario. Precisa ser melhorado para incluir inimigos de vdd
    def add_cars(self, cars_pos = None):
        if not cars_pos:
            self.cars_pos = open('car/list', 'r+').read().splitlines()
            self.cars_pos = [tuple(x.split()) for x in self.cars_pos]

        else:
            self.cars_pos = cars_pos

        print self.cars_pos
        for i, car in enumerate(self.cars_pos):
            model = self.loader.loadModel('car/car%s' % i)
            model.reparentTo(self.render)
            model.setScale(1, 0.8, 0.8)
            model.setPos(float(car[0]), float(car[1]), 0.2)
            self.cars.append({
                'model': model,
                'pos': car,
                'life': 100
                })

    def load_characters(self):
        self.actors = [
            Player(char, self)
            for char 
            in os.listdir(MODELS_PATH)
            if os.path.isdir(os.path.join(MODELS_PATH, char))
        ]

        # TODO: Character selection!!!
        self.player = self.actors[0]

        return self.player.getActor()

    def setup(self):
        self.running = True
        self.disableMouse()
        self.mouseMagnitude = 1
        self.rotateX, self.rotateY = 0, 0

        self.base.accept('0', lambda: self.setMouseMode(WindowProperties.M_absolute))
        self.base.accept('1', lambda: self.setMouseMode(WindowProperties.M_relative))
        self.base.accept('2', lambda: self.setMouseMode(WindowProperties.M_confined))
        self.base.accept('C', lambda: self.toggleRecenter())
        self.base.accept('c', lambda: self.toggleRecenter())
        self.base.accept('S', lambda: self.toggleMouse())
        self.base.accept('s', lambda: self.toggleMouse())
        self.base.accept('escape', lambda: self.close_game())

        self.lastMouseX, self.lastMouseY = None, None
        self.hideMouse = False

        self.setMouseMode(WindowProperties.M_absolute)
        self.manualRecenterMouse = True
        self.cam.setPos(0, 10, 2)
        self.cam.lookAt(0, 0, 1)

        self.mouseTask = taskMgr.add(self.mouseTask, "Mouse Task")
        self.base.enableParticles()
        self.particles = []
        #self.p = ParticleEffect()
        #self.p.loadConfig('particle-config')

        # self.p.start(parent = render, renderParent = render)


    def loadParticleConfig(self, filename, par):
        # Start of the code from steam.ptf
        p = ParticleEffect()
        p.loadConfig(Filename(filename))
        # Sets particles to birth relative to the teapot, but to render at
        # toplevel
        p.start(par)
        p.setPos(3.000, 0.000, 2.250)
        p.setScale(5)

        self.particles.append(p)

    def close_game(self):
        self.running = False
        sys.exit()

    def setMouseMode(self, mode):
        self.mouseMode = mode
        wp = WindowProperties()
        wp.setMouseMode(mode)
        self.base.win.requestProperties(wp)
        self.base.taskMgr.doMethodLater(0, self.resolveMouse, "Resolve mouse setting")

    def resolveMouse(self, t):
        wp = self.base.win.getProperties()

        actualMode = wp.getMouseMode()
        self.mouseMode = actualMode

        self.rotateX, self.rotateY = -.5, -.5
        self.lastMouseX, self.lastMouseY = None, None
        self.recenterMouse()

    def recenterMouse(self):
        self.base.win.movePointer(0,
              int(self.base.win.getProperties().getXSize() / 2),
              int(self.base.win.getProperties().getYSize() / 2))


    def toggleRecenter(self):
        self.manualRecenterMouse = not self.manualRecenterMouse

    def toggleMouse(self):
        self.hideMouse = not self.hideMouse
        wp = WindowProperties()
        wp.setCursorHidden(self.hideMouse)
        self.base.win.requestProperties(wp)

    def mouseTask(self, task):
        mw = self.base.mouseWatcherNode
        hasMouse = mw.hasMouse()
        if hasMouse:
            x, y = mw.getMouseX(), mw.getMouseY()
            if self.lastMouseX is not None:
                if self.manualRecenterMouse:
                    dx, dy = x, y
                else:
                    dx, dy = x - self.lastMouseX, y - self.lastMouseY
            else:
                dx, dy = 0, 0

            self.lastMouseX, self.lastMouseY = x, y

        else:
            x, y, dx, dy = 0, 0, 0, 0

        if self.manualRecenterMouse:
            self.recenterMouse()
            self.lastMouseX, self.lastMouseY = 0, 0

        # scale position and delta to pixels for user
        w, h = self.win.getSize()

        # rotate box by delta
        self.rotateX -= dx * 10 * self.mouseMagnitude
        #self.rotateY -= dy * 10 * self.mouseMagnitude

        self.player.actor.setH(self.rotateX)
        self.player.actor.setP(self.rotateY)

        #for car in self.cars:
            #print 'setting to %s' % self.cam.getHpr()
            #car['life'].lookAt(self.cam)

        return Task.cont


if __name__ == '__main__':
    game = Game()
    game.run()
