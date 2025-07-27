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

def updateParticles(app):
    for particle in app.particles[:]:
        particle['x'] += particle['vx']
        particle['y'] += particle['vy']
        particle['vy'] += 0.3  
        particle['life'] -= 1
        
        if particle['life'] <= 0:
            app.particles.remove(particle)

def drawParticles(app):
    for particle in app.particles:
        x = particle['x'] - app.cameraOffset
        if -20 < x < app.width + 20:
            alpha = particle['life'] / particle['maxLife']
            size = 3 * alpha
            
            if particle['type'] == 'explosion':
                drawCircle(x, particle['y'], max(1, size), fill=particle['color'])
            elif particle['type'] == 'sparkle':
                drawStar(x, particle['y'], max(1, size), 4, fill=particle['color'])
            elif particle['type'] == 'dust':
                drawCircle(x, particle['y'], max(1, size), fill=particle['color'])

def updatePowerUps(app):
    for powerUp in app.activePowerUps:
        if app.activePowerUps[powerUp] > 0:
            app.activePowerUps[powerUp] -= 1
