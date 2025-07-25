#main file for running everything
from cmu_graphics import *
from player import *
from graphics import *
from obstacles import *
from level import *
from visual_effects import *
from utils import *
from effects import *

def onAppStart(app):
    app.width = 800
    app.height = 600
    app.groundHeight = 100
    app.gameState = 'start'
    
    #Player with animation states
    app.player = {
        'x': 100,
        'y': app.height - app.groundHeight - 30,
        'width': 30,
        'height': 30,
        'vy': 0,
        'onGround': True,
        'jumpHeld': False,
        'animFrame': 0,
        'rotation': 0,
        'trail': [],
        'invulnerable': 0,
        'skin': 0  #Different player skins
    }
    
    #Physics
    app.gravity = 1.0
    app.jumpStrength = -16
    app.playerSpeed = 4
    app.autoScrollSpeed = 5
    app.score = 0
    app.timer = 0
    app.gameTime = 0
    
    #Game elements
    app.blocks = []
    app.coins = []
    app.powerUps = []
    app.particles = []
    app.coinsCollected = 0
    app.levelLength = 3000
    app.cameraOffset = 0
    app.cameraShake = 0
    
    #Visual effects
    app.backgroundOffset = 0
    app.starField = []
    for _ in range(50):
        app.starField.append({
            'x': random.randint(0, app.width),
            'y': random.randint(0, app.height - app.groundHeight),
            'size': random.randint(1, 3),
            'speed': random.uniform(0.5, 2)
        })
    
    #Power-up system
    app.activePowerUps = {
        'invincible': 0,
        'doubleJump': 0,
        'slowTime': 0,
        'magnetCoins': 0
    }
    
    #Game modes
    app.gameMode = 'normal'  # normal, hardcore, practice
    app.difficulty = 1
    app.achievements = []
    app.bestScore = 0

    #Visual
    app.visualEffects = []
    
    #Jump physics
    app.maxJumpHeight = abs(app.jumpStrength * app.jumpStrength) / (2 * app.gravity)
    app.maxJumpDistance = (2 * abs(app.jumpStrength) / app.gravity) * (app.playerSpeed + app.autoScrollSpeed)

def onStep(app):
    if app.gameState != 'playing':
        app.timer += 1  #For animations in menus
        return
    
    app.timer += 1
    app.gameTime += 1
    app.score = app.timer // 10
    
    #Update background elements
    updateBackground(app)
    
    #Player animations
    updatePlayerAnimation(app)
    
    #Automatic horizontal movement
    updatePlayerMovement(app)
    
    #Rapid jumping when holding jump key
    handleJumping(app)
    
    #Physics
    updatePhysics(app)
    
    #Camera
    updateCamera(app)
    
    #Ground collision
    handleGroundCollision(app)
    
    #Block collisions
    handleBlockCollisions(app)
    
    #Coin collection with magnet effect
    handleCoinCollection(app)
    
    #Power-up collection
    handlePowerUpCollection(app)
    
    #Particle system adjustments
    updateParticles(app)
    updatePowerUps(app)
    
    #visual effects
    updateVisualEffects(app)
    
    #Death conditions
    if app.player['y'] > app.height:
        app.gameState = 'gameOver'
        addVisualEffect(app, 'death', app.player['x'], app.player['y'])
    
    #Win condition
    if app.player['x'] >= app.levelLength:
        app.gameState = 'win'
        if app.score > app.bestScore:
            app.bestScore = app.score
        addVisualEffect(app, 'victory', app.player['x'], app.player['y'])

def onKeyPress(app, key):
    if app.gameState == 'start':
        if key == 'space':
            startGame(app)
        elif key == '1':
            app.gameMode = 'normal'
        elif key == '2':
            app.gameMode = 'hardcore'
            app.difficulty = 2
        elif key == '3':
            app.gameMode = 'practice'
        elif key == 's':
            app.player['skin'] = (app.player['skin'] + 1) % 3
    elif app.gameState == 'playing':
        if (key == 'space' or key == 'w' or key == 'up') and canJump(app):
            performJump(app)
    elif app.gameState in ('gameOver', 'win'):
        if key == 'r':
            startGame(app)

def onKeyRelease(app, key):
    if key == 'space' or key == 'w' or key == 'up':
        app.player['jumpHeld'] = False

def onMousePress(app, x, y):
    if app.gameState == 'start':
        startGame(app)
    elif app.gameState == 'playing':
        if canJump(app):
            performJump(app)
    elif app.gameState in ('gameOver', 'win'):
        startGame(app)

def startGame(app):
    app.gameState = 'playing'
    app.timer = 0
    app.gameTime = 0
    app.score = 0
    app.coinsCollected = 0
    app.player['x'] = 100
    app.player['y'] = app.height - app.groundHeight - app.player['height']
    app.player['vy'] = 0
    app.player['onGround'] = True
    app.player['jumpHeld'] = False
    app.player['rotation'] = 0
    app.player['trail'] = []
    app.player['invulnerable'] = 0
    app.cameraOffset = 0
    app.cameraShake = 0
    app.particles = []
    app.visualEffects = []
    
    #Reset power-ups
    for key in app.activePowerUps:
        app.activePowerUps[key] = 0
    
    app.blocks, app.coins, app.powerUps = createRandomLevel(app)

def redrawAll(app):
    drawBackground(app)
    drawBlocks(app)
    drawCoins(app)
    drawPowerUps(app)
    drawParticles(app)
    drawPlayer(app)
    drawVisualEffects(app)
    
    #UI
    if app.gameState == 'playing':
        drawEnhancedUI(app)
    
    #Game state screens
    if app.gameState == 'start':
        drawStartScreen(app)
    elif app.gameState == 'gameOver':
        drawGameOverScreen(app)
    elif app.gameState == 'win':
        drawWinScreen(app)
runApp()
