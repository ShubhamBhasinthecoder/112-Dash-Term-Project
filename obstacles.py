#file for generation of all obstacles in the game/powerups/effects in a second file

from cmu_graphics import *
import math
import random
from utils import checkCollision, isLandingOn
from effects import addParticle
from visual_effects import addVisualEffect

def handleBlockCollisions(app):
    for block in app.blocks:
        if block.get('moving', False):
            block['y'] = block['originalY'] + math.sin(app.timer * 0.1) * block.get('moveRange', 30)
        if block['type'] == 'spike':
            block['animFrame'] = app.timer
        if block['type'] in ('platform',) and isLandingOn(app.player, block):
            app.player['y'] = block['y'] - app.player['height']
            app.player['vy'] = 0
            app.player['onGround'] = True
            break
        elif block['type'] in ('platform',) and checkCollision(app.player, block):
            if app.player['invulnerable'] == 0 and app.activePowerUps['invincible'] == 0:
                app.gameState = 'gameOver'
                addParticle(app, app.player['x'] + 15, app.player['y'] + 15, 'red', 'explosion')
                app.cameraShake = 10
                return
        elif block['type'] == 'spike' and checkCollision(app.player, block):
            if app.player['invulnerable'] == 0 and app.activePowerUps['invincible'] == 0:
                app.gameState = 'gameOver'
                addParticle(app, app.player['x'] + 15, app.player['y'] + 15, 'red', 'explosion')
                app.cameraShake = 10
                addVisualEffect(app, 'death', app.player['x'], app.player['y'])
                return

def handleCoinCollection(app):
    for coin in app.coins:
        if not coin['collected']:
            coin['animFrame'] += 1
            if app.activePowerUps['magnetCoins'] > 0:
                dx = app.player['x'] - coin['x']
                dy = app.player['y'] - coin['y']
                distance = math.sqrt(dx*dx + dy*dy)
                if distance < 100:
                    coin['x'] += dx * 0.1
                    coin['y'] += dy * 0.1
            if checkCollision(app.player, coin):
                coin['collected'] = True
                app.coinsCollected += 1
                app.score += 10
                addParticle(app, coin['x'], coin['y'], 'gold', 'coin')
                addVisualEffect(app, 'coin', coin['x'], coin['y'])

def handlePowerUpCollection(app):
    for powerUp in app.powerUps:
        if not powerUp['collected']:
            powerUp['animFrame'] += 1
            if checkCollision(app.player, powerUp):
                powerUp['collected'] = True
                app.activePowerUps[powerUp['type']] = 300  
                addParticle(app, powerUp['x'], powerUp['y'], 'cyan', 'explosion')
                addVisualEffect(app, 'powerup', powerUp['x'], powerUp['y'])

def drawBlocks(app):
    for block in app.blocks:
        x = block['x'] - app.cameraOffset
        if -50 < x < app.width + 50:
            y, w, h = block['y'], block['width'], block['height']
            if block['type'] == 'platform':
                if block.get('moving', False):
                    glowSize = 3 + math.sin(app.timer * 0.2) * 2
                    drawRect(x - glowSize, y - glowSize, w + glowSize*2, h + glowSize*2, 
                            fill='lightBlue', border='blue', borderWidth=1)
                drawRect(x, y, w, h, fill='saddleBrown')
                drawRect(x, y, w, 4, fill='peru')  
                drawRect(x + w - 3, y, 3, h, fill='brown')  
                drawRect(x, y + h - 3, w, 3, fill='brown')  
                drawRect(x, y, 3, h, fill='burlywood')  
                for i in range(0, w, 10):
                    drawLine(x + i, y + 2, x + i, y + h - 2, fill='brown')
                
            elif block['type'] == 'spike':
                animOffset = math.sin(block.get('animFrame', 0) * 0.1) * 2
                spikeColor = 'red' if animOffset > 0 else 'darkRed'
                glowSize = 2 + math.sin(app.timer * 0.3) * 1
                drawPolygon(x - glowSize, y + h + glowSize, 
                           x + w/2, y - glowSize, 
                           x + w + glowSize, y + h + glowSize, 
                           fill='orange')
                drawPolygon(x, y + h + animOffset, 
                           x + w/2, y + animOffset, 
                           x + w, y + h + animOffset, 
                           fill=spikeColor)
                drawPolygon(x + 3, y + h, x + w/2, y + 3, x + w/2, y + h, 
                           fill='crimson')
                drawPolygon(x + w/2, y + 3, x + w - 3, y + h, x + w, y + h, 
                           fill='maroon')
                
            elif block['type'] == 'wall':
                drawRect(x, y, w, h, fill='gray')
                drawRect(x, y, w, 3, fill='lightGray')  
                drawRect(x + w - 2, y, 2, h, fill='dimGray')  
                for i in range(0, h, 15):
                    drawLine(x, y + i, x + w, y + i, fill='darkGray')
                for i in range(0, w, 8):
                    drawLine(x + i, y, x + i, y + h, fill='darkGray')
