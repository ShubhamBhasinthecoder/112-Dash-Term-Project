#file for all the graphics in the game

from cmu_graphics import *
import math
import random

def updateBackground(app):
    
    app.backgroundOffset += 1
    for star in app.starField:
        star['x'] -= star['speed']
        if star['x'] < -10:
            star['x'] = app.width + 10
            star['y'] = random.randint(0, app.height - app.groundHeight)

def drawBackground(app):
    
    for i in range(app.height):
        
        blueShade = 135 + int(math.sin(app.timer * 0.01 + i * 0.01) * 20)
        drawLine(0, i, app.width, i, fill=rgb(max(0, blueShade - 50), 
                max(0, 206 + int(math.sin(app.timer * 0.02) * 30)), 
                max(0, 235 - int(i * 50 / app.height))))
    
    
    for star in app.starField:
        starX = star['x'] - app.cameraOffset * 0.3  
        if -10 < starX < app.width + 10:
            twinkle = star['size'] + math.sin(app.timer * 0.1 + star['x'] * 0.01) * 0.5
            drawCircle(starX, star['y'], max(1, twinkle), fill='white')
    
    
    groundX = -app.cameraOffset
    
    for i in range(0, app.width + int(app.cameraOffset * 2), 20):
        groundShade = int(100 + math.sin((i + app.timer) * 0.1) * 20)
        drawRect(groundX + i, app.height - app.groundHeight, 20, app.groundHeight, 
                fill=rgb(0, max(0, groundShade), 0))
    
    
    drawRect(groundX, app.height - app.groundHeight, app.width + app.cameraOffset * 2, 
             8, fill='limeGreen')

def drawEnhancedUI(app):
    
    drawRect(10, 10, 140, 45, fill='black', border='white', borderWidth=2)
    drawLabel(f'Score: {app.score}', 80, 25, size=14, fill='white', bold=True)
    drawLabel(f'Best: {app.bestScore}', 80, 40, size=12, fill='yellow')
    
    
    drawRect(160, 10, 120, 45, fill='black', border='white', borderWidth=2)
    
    coinSize = 8 + math.sin(app.timer * 0.1) * 1
    drawStar(185, 32, coinSize, 5, fill='gold')
    drawLabel(f': {app.coinsCollected}', 220, 32, size=16, fill='white', bold=True)
    
    
    uiY = 65
    activeCount = 0
    for powerUp, duration in app.activePowerUps.items():
        if duration > 0:
            powerUpX = 10 + activeCount * 130
            
            if duration < 60 and duration % 10 < 5:
                continue
            
            powerUpColors = {
                'invincible': 'cyan',
                'doubleJump': 'lime', 
                'slowTime': 'purple',
                'magnetCoins': 'gold'
            }
            
            drawRect(powerUpX, uiY, 120, 25, fill=powerUpColors.get(powerUp, 'white'), 
                    border='black', borderWidth=2)
            drawLabel(f'{powerUp}: {duration//60+1}s', powerUpX + 60, uiY + 12, 
                     size=10, fill='black', bold=True)
            activeCount += 1
    
    
    progress = min(app.player['x'] / app.levelLength, 1.0)
    progressBarWidth = 200
    barX = app.width - progressBarWidth - 20
    
    drawRect(barX, 10, progressBarWidth, 20, fill='black', border='white', borderWidth=2)
    
    
    if progress < 0.3:
        progressColor = 'red'
    elif progress < 0.7:
        progressColor = 'yellow'
    else:
        progressColor = 'lime'
    
    drawRect(barX + 2, 12, int(progress * (progressBarWidth - 4)), 16, fill=progressColor)
    drawLabel(f'{int(progress * 100)}%', barX + progressBarWidth//2, 20, 
             size=12, fill='white', bold=True)
    
    
    modeColors = {'normal': 'blue', 'hardcore': 'red', 'practice': 'green'}
    drawRect(app.width - 150, 40, 140, 20, 
            fill=modeColors.get(app.gameMode, 'blue'), border='white', borderWidth=2)
    drawLabel(f'Mode: {app.gameMode.upper()}', app.width - 80, 50, 
             size=12, fill='white', bold=True)

def drawStartScreen(app):
    
    drawRect(0, 0, app.width, app.height, fill='darkBlue')
    
    
    for i in range(10):
        x = (app.timer * 2 + i * 80) % (app.width + 100) - 50
        y = 100 + i * 40 + math.sin(app.timer * 0.05 + i) * 30
        size = 20 + math.sin(app.timer * 0.1 + i) * 10
        colors = ['orange', 'blue', 'green', 'red', 'purple']
        drawRect(x, y, size, size, fill=colors[i % len(colors)], 
                border='white', borderWidth=2)
    
    
    menuY = app.height/2 - 120
    drawRect(app.width/2 - 255, menuY - 5, 510, 250, 
            fill='cyan', border='blue', borderWidth=3)
    drawRect(app.width/2 - 250, menuY, 500, 240, 
            fill='white', border='black', borderWidth=4)
    
    
    drawLabel('ENHANCED 112 DASH', app.width/2, menuY + 30, 
             size=24, fill='blue', bold=True)
    
    
    drawLabel('Select Game Mode:', app.width/2, menuY + 70, size=16, fill='black', bold=True)
    
    modes = [
        ('1 - NORMAL MODE', 'green', 'Easy difficulty with standard gameplay'),
        ('2 - HARDCORE MODE', 'red', 'Increased difficulty and obstacles'),
        ('3 - PRACTICE MODE', 'blue', 'Infinite lives for practice')
    ]
    
    for i, (mode, color, desc) in enumerate(modes):
        modeY = menuY + 95 + i * 25
        modeColor = color if app.gameMode != mode.split()[2].lower() else 'gold'
        drawLabel(mode, app.width/2 - 100, modeY, size=14, fill=modeColor, bold=True)
        drawLabel(desc, app.width/2 + 50, modeY, size=10, fill='gray')
    
    
    drawLabel('S - Change Skin:', app.width/2 - 100, menuY + 170, size=14, fill='black')
    skinColors = ['orange', 'blue', 'green']
    for i, color in enumerate(skinColors):
        skinX = app.width/2 + i * 40 - 20
        border = 'gold' if i == app.player['skin'] else 'black'
        drawRect(skinX, menuY + 155, 25, 25, fill=color, border=border, borderWidth=3)
    
    
    buttonColor = 'lime' if app.timer % 60 < 30 else 'green'
    drawRect(app.width/2 - 150, menuY + 190, 300, 35, 
            fill=buttonColor, border='darkGreen', borderWidth=3)
    drawLabel('CLICK or SPACE to START', app.width/2, menuY + 207, 
             size=16, fill='white', bold=True)
    
    
    if app.bestScore > 0:
        drawLabel(f'Best Score: {app.bestScore}', app.width/2, 50, 
                 size=18, fill='gold', bold=True)

def drawGameOverScreen(app):
    
    drawRect(0, 0, app.width, app.height, fill='darkRed')
    
    
    for i in range(20):
        x = random.randint(0, app.width)
        y = random.randint(0, app.height)
        size = random.randint(10, 30)
        drawPolygon(x, y, x+size, y+size//2, x+size//2, y+size, 
                   fill='red', border='darkRed')
    
    
    drawRect(app.width/2 - 200, app.height/2 - 80, 400, 160, 
            fill='white', border='red', borderWidth=5)
    drawRect(app.width/2 - 195, app.height/2 - 75, 390, 10, fill='pink')
    
    
    drawLabel('GAME OVER!', app.width/2, app.height/2 - 40, 
             size=28, fill='red', bold=True)
    
    
    drawLabel(f'Final Score: {app.score}', app.width/2, app.height/2 - 10, 
             size=16, fill='black', bold=True)
    drawLabel(f'Coins Collected: {app.coinsCollected}', app.width/2, app.height/2 + 10, 
             size=16, fill='gold', bold=True)
    drawLabel(f'Distance Traveled: {int(app.player["x"])}m', app.width/2, app.height/2 + 30, 
             size=14, fill='blue')
    
    
    drawRect(app.width/2 - 100, app.height/2 + 50, 200, 30, 
            fill='orange', border='red', borderWidth=3)
    drawLabel('Press R to Restart', app.width/2, app.height/2 + 65, 
             size=14, fill='white', bold=True)

def drawWinScreen(app):
    
    drawRect(0, 0, app.width, app.height, fill='darkGreen')
    
    
    for i in range(15):
        x = (app.timer * 3 + i * 50) % app.width
        y = 50 + (app.timer + i * 30) % 200
        size = 5 + math.sin(app.timer * 0.2 + i) * 3
        colors = ['yellow', 'orange', 'red', 'purple', 'blue']
        drawStar(x, y, size, 6, fill=colors[i % len(colors)])
    
    
    drawRect(app.width/2 - 220, app.height/2 - 90, 440, 180, 
            fill='white', border='green', borderWidth=5)
    drawRect(app.width/2 - 215, app.height/2 - 85, 430, 12, fill='lightGreen')
    
    
    drawLabel('VICTORY!', app.width/2, app.height/2 - 50, 
             size=32, fill='green', bold=True)
    
    
    drawLabel(f'Final Score: {app.score}', app.width/2, app.height/2 - 15, 
             size=18, fill='black', bold=True)
    drawLabel(f'Coins Collected: {app.coinsCollected}', app.width/2, app.height/2 + 5, 
             size=18, fill='gold', bold=True)
    drawLabel(f'Completion Time: {app.gameTime//60}s', app.width/2, app.height/2 + 25, 
             size=16, fill='blue')
    
    
    if app.coinsCollected > 20:
        rating = 'PERFECT!'
    elif app.coinsCollected > 10:
        rating = 'GREAT!'
    else:
        rating = 'GOOD!'
    drawLabel(f'Rating: {rating}', app.width/2, app.height/2 + 45, 
             size=16, fill='purple', bold=True)
    
    
    drawRect(app.width/2 - 120, app.height/2 + 65, 240, 30, 
            fill='lime', border='green', borderWidth=3)
    drawLabel('Press R for New Challenge!', app.width/2, app.height/2 + 80, 
             size=14, fill='darkGreen', bold=True)
