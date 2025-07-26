#file for all the particle effects and the powerup particles.
from cmu_graphics import *
import random
import math

def addParticle(app, x, y, color, particleType='explosion'):
    
    if particleType == 'explosion':
        for _ in range(8):
            app.particles.append({
                'x': x,
                'y': y,
                'vx': random.uniform(-5, 5),
                'vy': random.uniform(-8, 2),
                'color': color,
                'life': 30,
                'maxLife': 30,
                'type': 'explosion'
            })
    elif particleType == 'coin':
        for _ in range(5):
            app.particles.append({
                'x': x,
                'y': y,
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-5, -2),
                'color': 'gold',
                'life': 20,
                'maxLife': 20,
                'type': 'sparkle'
            })
    elif particleType == 'jump':
        for _ in range(3):
            app.particles.append({
                'x': x,
                'y': y + 25,
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(1, 3),
                'color': 'white',
                'life': 15,
                'maxLife': 15,
                'type': 'dust'
            })
