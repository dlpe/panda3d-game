#!/usr/bin/python


import os
import sys
from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from panda3d.core import DirectionalLight, WindowProperties

FORWARD = 'w'
BACKWARDS = 's'
LEFT = 'a'
RIGHT = 'd'

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
    TURNR,
    TURNL,
    ATTACK,
    HIT,
    DEATH
]

class Model(object):
    def __init__(self, name, game, pos = None):
        self.name = name
        self.game = game
        self.path = os.path.join(MODELS_PATH, name)
        #anim = {}
        self.actors = {}
        # Init animacoes
        scale = open(os.path.join(self.path, SCALE_TXT)).read()
        self.scale = float(scale)
        #self.actor.setScale(scale, scale, scale)

        for a in ANIM:
            #anim[a] = os.path.join(MODELS_PATH, name, a)
            self.actors[a] = self.make_actor(a)
        #try:
            #print anim
            #self.actor = Actor(
            #    os.path.join(path, T_POSE), anim)

            #scale = open(os.path.join(path, SCALE_TXT)).read()
            #scale = float(scale)
            #self.actor.setScale(scale, scale, scale)

        #except IOError as ie:
        #    print 'Could\'t load character %s due to: %s' % (name, ie.message)

        #else:
            #if isinstance(pos, tuple):
        # Init default animation
        self.current = self.actors[IDLE]
        self.current.reparentTo(game.render)
            # Be natural
        self.attack()
            #self.anim_contrl = self.actor.getAnimControl("walk")
            #print dir(self.anim_contrl)
            #self.anim_contrl.loop('stand')

    def make_actor(self, anim):
       actor = Actor(os.path.join(self.path, anim)) 
       actor.setScale(self.scale, self.scale, self.scale)
       return actor

    def blend(self, anim1, anim2, p1 = 0.5, p2 = 0.5):
        selfactor.enableBlend()
        self.actor.setControlEffect(anim1, p1)
        self.actor.setControlEffect(anim2, p2)
        self.actor.loop(anima1)
        self.actor.loop(anim2)

    def disableBlend(self):
        self.actor.disableBlend()

    def stand(self):
        self.actor = self.actors[IDLE]
    def fight(self):
        self.actor = self.actors[FIGHT]
    def walk(self, direction = None):
        # TODO: move
        self.actor = self.actors[WALK]
    def turn(self, direction):
        self.actor = self.actors[
            TURNR if direction == RIGHT else (
                TURNL if direction == LEFT else None)]

    def close(self, direction = None):
        # TODO: move
        self.actor = self.actors[CLOSE]
    def attack(self, direction = None):
        # TODO: move
        self.actor = self.actors[ATTACK]
    def hit(self):
        # TODO: move
        self.actor = self.actors[HIT]
    def die(self, direction = None):
        # TODO: move
        self.actor = self.actors[DEATH]

    def move(self):
        pass

class Player(Model, DirectObject): 
    def __init__(self, name, game, pos = None):
        Model.__init__(self, name, game, pos)
        self.accept(FORWARD, self.forward)
        self.accept(BACKWARDS, self.backwards)
        self.accept(LEFT, self.left)
        self.accept(RIGHT, self.right)

    def forward(self, when):
        print "key ", when
    def backwards(self, when):
        print "key ", when
    def right(self, when):
        print "key ", when
    def left(self, when):
        print "key ", when


class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.base = self
        self.setup()

        # Load the environment model.
        self.scene = self.loader.loadModel(ENV)
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # Create Ambient Light
        self.light = DirectionalLight('ambientLight')
        self.light.setColor((1, 1, 1, 1))
        self.light = render.attachNewNode(self.light)
        #render.setLight(self.light)

        self.load_characters()
        # Add the spinCameraTask procedure to the task manager.
        #self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        #self.pandaActor.setScale(0.005, 0.005, 0.005)
        #self.pandaActor.reparentTo(self.render)
        #self.pandaActor.loop('walk')

        #self.out = Actor('/home/andre/Downloads/Walking/char.egg')
        #self.out.setScale(0.005, 0.005, 0.005)
        #self.out.reparentTo(self.render)
        #self.out.loop('')
        # Create the four lerp intervals needed for the panda to
        # walk back and forth.
        ''' 
        pandaPosInterval1 = self.pandaActor.posInterval(13,
                                                        Point3(0, -10, 0),
                                                        startPos=Point3(0, 10, 0))
        pandaPosInterval2 = self.pandaActor.posInterval(13,
                                                        Point3(0, 10, 0),
                                                        startPos=Point3(0, -10, 0))
        pandaHprInterval1 = self.pandaActor.hprInterval(3,
                                                        Point3(180, 0, 0),
                                                        startHpr=Point3(0, 0, 0))
        pandaHprInterval2 = self.pandaActor.hprInterval(3,
                                                        Point3(0, 0, 0),
                                                        startHpr=Point3(180, 0, 0))
 
        # Create and play the sequence that coordinates the intervals.
        self.pandaPace = Sequence(pandaPosInterval1,
                                  pandaHprInterval1,
                                  pandaPosInterval2,
                                  pandaHprInterval2,
                                  name="pandaPace")
        self.pandaPace.loop()
        ''' 
    def load_characters(self):
        self.actors = [
            Model(char, self)
            for char 
            in os.listdir(MODELS_PATH)
            if os.path.isdir(os.path.join(MODELS_PATH, char))
        ]

        # TODO: Character selection!!!
        self.player = self.actors[0]

    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

    def setup(self):
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
        self.base.accept('escape', sys.exit, [0])

        self.lastMouseX, self.lastMouseY = None, None
        self.hideMouse = False

        self.setMouseMode(WindowProperties.M_absolute)
        self.manualRecenterMouse = True
        self.cam.setPos(0, 20, -1)
        self.cam.lookAt(0, 0, 0)

        self.mouseTask = taskMgr.add(self.mouseTask, "Mouse Task")

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
        self.cam.setPos(self.player.actor.getPos() + (0, 10, 0))
        return Task.cont


if __name__ == '__main__':
    game = Game()
    game.run()
