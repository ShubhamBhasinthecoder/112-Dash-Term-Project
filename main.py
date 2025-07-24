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
