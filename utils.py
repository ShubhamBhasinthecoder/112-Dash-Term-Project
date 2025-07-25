#functionalities for the player state checks and the game.
import random
import math

def checkCollision(p, b):
    return (
        p['x'] < b['x'] + b['width'] and
        p['x'] + p['width'] > b['x'] and
        p['y'] < b['y'] + b['height'] and
        p['y'] + p['height'] > b['y']
    )

def isLandingOn(player, block):
    playerBottom = player['y'] + player['height']
    onTop = playerBottom >= block['y'] - 15 and playerBottom <= block['y'] + 15
    horizontalOverlap = (
        player['x'] + player['width'] > block['x'] and
        player['x'] < block['x'] + block['width']
    )
    falling = player['vy'] > 0
    return onTop and horizontalOverlap and falling

def canJump(app):
    doubleJumpAvailable = app.activePowerUps['doubleJump'] > 0 and not app.player['onGround']
    return (app.player['onGround'] and app.player['vy'] >= 0) or doubleJumpAvailable

def isJumpPossible(startX, startY, endX, endY, app):
    distance = endX - startX
    heightDiff = startY - endY
    
    if distance > app.maxJumpDistance * 1.2:
        return False
    if heightDiff > app.maxJumpHeight * 0.9:
        return False
    if heightDiff < -30:
        return False
    return True
