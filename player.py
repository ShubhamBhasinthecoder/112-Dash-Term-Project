#file for animations of the player/physics of the player square

from cmu_graphics import *
import math
from effects import addParticle
from visual_effects import addVisualEffect
from utils import canJump

def updatePlayerAnimation(app):
    
    app.player['animFrame'] += 1
    if not app.player['onGround']:
        app.player['rotation'] += 5
    else:
        app.player['rotation'] = 0
    
    
    app.player['trail'].append((app.player['x'], app.player['y']))
    if len(app.player['trail']) > 8:
        app.player['trail'].pop(0)

def updatePlayerMovement(app):
    
    moveSpeed = app.autoScrollSpeed
    if app.activePowerUps['slowTime'] > 0:
        moveSpeed *= 0.5
    app.player['x'] += moveSpeed

def handleJumping(app):
    
    if app.player['jumpHeld'] and canJump(app):
        app.player['vy'] = app.jumpStrength
        app.player['onGround'] = False
        addParticle(app, app.player['x'] + 15, app.player['y'] + 30, 'white', 'jump')
        addVisualEffect(app, 'jump', app.player['x'], app.player['y'])
        
        
        if not app.player['onGround'] and app.activePowerUps['doubleJump'] > 0:
            app.activePowerUps['doubleJump'] = 0
            addParticle(app, app.player['x'] + 15, app.player['y'] + 15, 'cyan', 'explosion')

def updatePhysics(app):
    
    gravityForce = app.gravity
    if app.activePowerUps['slowTime'] > 0:
        gravityForce *= 0.7
    
    app.player['vy'] += gravityForce
    app.player['y'] += app.player['vy']

def handleGroundCollision(app):
    
    groundY = app.height - app.groundHeight - app.player['height']
    if app.player['y'] >= groundY:
        app.player['y'] = groundY
        app.player['vy'] = 0
        app.player['onGround'] = True
    else:
        app.player['onGround'] = False

def performJump(app):
    
    app.player['vy'] = app.jumpStrength
    app.player['onGround'] = False
    app.player['jumpHeld'] = True

def drawPlayer(app):
    
    playerX = app.player['x'] - app.cameraOffset
    if -50 < playerX < app.width + 50:
        
        drawRect(playerX + 3, app.player['y'] + 3, app.player['width'], 
                app.player['height'], fill='darkGray')
        
        
        drawPlayerSprite(app, playerX, app.player['y'])

def drawPlayerSprite(app, x, y):
    
    
    for i, (trailX, trailY) in enumerate(app.player['trail']):
        if i < len(app.player['trail']) - 1:
            trailScreenX = trailX - app.cameraOffset
            alpha = i / len(app.player['trail'])
            
            trailColor = 'lightGray' if alpha > 0.5 else 'gray'
            drawRect(trailScreenX, trailY, app.player['width'], app.player['height'], 
                    fill=trailColor)
    
    
    if app.player['invulnerable'] > 0 and app.player['invulnerable'] % 10 < 5:
        return  
    
    if app.activePowerUps['invincible'] > 0:
        
        drawRect(x - 3, y - 3, app.player['width'] + 6, app.player['height'] + 6, 
                fill='cyan', border='blue', borderWidth=2)
    
    
    if app.player['skin'] == 0:  
        mainColor, borderColor = 'orange', 'darkOrange'
    elif app.player['skin'] == 1:  
        mainColor, borderColor = 'blue', 'darkBlue'
    else:  
        mainColor, borderColor = 'green', 'darkGreen'
    
    
    if abs(app.player['rotation']) > 0:
        
        offsetX = math.sin(math.radians(app.player['rotation'])) * 2
        offsetY = math.cos(math.radians(app.player['rotation'])) * 2
        drawRect(x + offsetX, y + offsetY, app.player['width'], app.player['height'], 
                fill=mainColor, border=borderColor, borderWidth=3)
    else:
        drawRect(x, y, app.player['width'], app.player['height'], 
                fill=mainColor, border=borderColor, borderWidth=3)
    
    
    drawRect(x + 2, y + 2, app.player['width'] - 4, 6, fill='gold')
    
    
    eyeOffset = math.sin(app.timer * 0.3) * 2
    drawCircle(x + 7, y + 10 + eyeOffset, 3, fill='white')
    drawCircle(x + 23, y + 10 + eyeOffset, 3, fill='white')
    drawCircle(x + 7, y + 10 + eyeOffset, 2, fill='black')
    drawCircle(x + 23, y + 10 + eyeOffset, 2, fill='black')
    
    
    mouthY = y + 20 + math.sin(app.timer * 0.2) * 1
    drawArc(x + 15, mouthY, 8, 6, 0, 180, fill='black')
