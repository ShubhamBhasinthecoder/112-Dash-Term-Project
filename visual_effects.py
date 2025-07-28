#file for the sound effects in the game. temporary addition, may not add this feature
#replacing this with an additional file for extra visual effects.
from cmu_graphics import *
import random
import math

class VisualEffect:
    def __init__(self, effectType, x, y, maxLife=30):
        self.type = effectType
        self.x = x
        self.y = y
        self.life = maxLife
        self.maxLife = maxLife
    
    def update(self):
        self.life -= 1
    
    def isExpired(self):
        return self.life <= 0
    
    def draw(self, cameraOffset, screenWidth):
        screenX = self.x - cameraOffset
        if -50 < screenX < screenWidth + 50:
            alpha = self.life / self.maxLife
            if self.type == 'jump':
                size = 20 * alpha
                drawCircle(screenX, self.y, size, fill='white', border='gray', borderWidth=2)
            elif self.type == 'coin':
                drawLabel('♪', screenX, self.y, size=int(20 * alpha), fill='gold')
            elif self.type == 'death':
                size = 30 * alpha
                drawStar(screenX, self.y, size, 8, fill='red')
            elif self.type == 'powerup':
                drawLabel('✨', screenX, self.y, size=int(25 * alpha), fill='cyan')
            elif self.type == 'victory':
                drawLabel('🎉', screenX, self.y, size=int(30 * alpha), fill='gold')

class VisualEffectManager:
    def __init__(self):
        self.effects = []
    
    def addEffect(self, effectType, x, y):
        effect = VisualEffect(effectType, x, y)
        self.effects.append(effect)
    
    def update(self):
        for effect in self.effects:
            effect.update()
        
        self.effects = [effect for effect in self.effects if not effect.isExpired()]
    
    def draw(self, cameraOffset, screenWidth):
        for effect in self.effects:
            effect.draw(cameraOffset, screenWidth)


def addVisualEffect(app, effectType, x, y):
    if not hasattr(app, 'effectManager'):
        app.effectManager = VisualEffectManager()
    app.effectManager.addEffect(effectType, x, y)

def updateVisualEffects(app):
    if hasattr(app, 'effectManager'):
        app.effectManager.update()

def drawVisualEffects(app):
    if hasattr(app, 'effectManager'):
        app.effectManager.draw(app.cameraOffset, app.width)
