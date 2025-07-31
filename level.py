#file for creation of the random generated obstacles and levels.

import random
from utils import isJumpPossible

def updateCamera(app):
    shake = 0
    if app.cameraShake > 0:
        shake = random.randint(-app.cameraShake, app.cameraShake)
        app.cameraShake -= 1
    app.cameraOffset = max(0, app.player['x'] - 200) + shake
#Random Level generation math for the randomisation of level blocks and obstacles.
def createRandomLevel(app):
    blocks = []
    coins = []
    powerUps = []
    groundLevel = app.height - app.groundHeight
    playerSpawnX = app.player['x']
    playerSpawnWidth = 150
    playerSpawnZone = (playerSpawnX - 50, playerSpawnX + playerSpawnWidth)
    currentX = 150
    currentY = app.height - app.groundHeight
    themes = ['normal', 'spiky', 'platformy', 'challenging']
    while currentX < app.levelLength:
        if currentX % 500 == 0:
            currentTheme = random.choice(themes)
        obstacles = ['platform', 'spikes', 'small_gap', 'stairs', 'low_wall', 'moving_platform']
        if app.difficulty > 1:
            obstacles.extend(['double_spikes', 'narrow_gap', 'high_wall'])
        obstacle = random.choice(obstacles)
        if obstacle == 'platform':
            platformWidth = random.randint(80, 160)
            gap = random.randint(40, 80)
            height = random.randint(20, 80)
            newY = max(groundLevel - height - 20, groundLevel - 200)
            platformX = currentX + gap
            if (platformX < playerSpawnZone[1] and platformX + platformWidth > playerSpawnZone[0]):
                currentX += gap + platformWidth
                continue
            if isJumpPossible(currentX, currentY, platformX, newY, app):
                blocks.append({
                    'x': platformX,
                    'y': newY,
                    'width': platformWidth,
                    'height': 20,
                    'type': 'platform',
                    'moving': False
                })
                for i in range(random.randint(1, 3)):
                    coinX = platformX + 20 + i * 35
                    coinY = min(newY - 30, groundLevel - 50)
                    if not (coinX < playerSpawnZone[1] and coinX + 15 > playerSpawnZone[0]):
                        coins.append({
                            'x': coinX,
                            'y': coinY,
                            'width': 15,
                            'height': 15,
                            'collected': False,
                            'animFrame': 0
                        })
                if random.random() < 0.1:
                    powerUpX = platformX + platformWidth // 2
                    powerUpY = newY - 35
                    powerUpType = random.choice(['invincible', 'doubleJump', 'slowTime', 'magnetCoins'])
                    powerUps.append({
                        'x': powerUpX,
                        'y': powerUpY,
                        'width': 20,
                        'height': 20,
                        'type': powerUpType,
                        'collected': False,
                        'animFrame': 0
                    })
                
                currentX += gap + platformWidth
                currentY = newY
            else:
                fallbackY = max(currentY, groundLevel - 40)
                fallbackX = currentX + 20
                if not (fallbackX < playerSpawnZone[1] and fallbackX + 120 > playerSpawnZone[0]):
                    blocks.append({
                        'x': fallbackX,
                        'y': fallbackY,
                        'width': 120,
                        'height': 20,
                        'type': 'platform',
                        'moving': False
                    })
                currentX += 140
                currentY = fallbackY
        elif obstacle == 'moving_platform':
            platformWidth = 80
            gap = random.randint(50, 90)
            height = random.randint(30, 70)
            newY = max(groundLevel - height - 20, groundLevel - 150)
            platformX = currentX + gap
            if isJumpPossible(currentX, currentY, platformX, newY, app):
                blocks.append({
                    'x': platformX,
                    'y': newY,
                    'width': platformWidth,
                    'height': 20,
                    'type': 'platform',
                    'moving': True,
                    'moveRange': 50,
                    'moveSpeed': 2,
                    'originalY': newY
                })
                currentX += gap + platformWidth + 20
                currentY = newY
            else:
                currentX += 50
        elif obstacle == 'spikes':
            spikeCount = random.randint(2, 4)
            spikeWidth = 25
            
            if random.random() > 0.3:
                warningPlatformY = max(currentY - 40, groundLevel - 60)
                if not (currentX < playerSpawnZone[1] and currentX + 80 > playerSpawnZone[0]):
                    blocks.append({
                        'x': currentX,
                        'y': warningPlatformY,
                        'width': 80,
                        'height': 20,
                        'type': 'platform',
                        'moving': False
                    })
                startX = currentX + 80
                currentY = warningPlatformY
            else:
                startX = currentX
            spikeY = groundLevel - 25
            for i in range(spikeCount):
                spikeX = startX + i * spikeWidth
                if not (spikeX < playerSpawnZone[1] and spikeX + 25 > playerSpawnZone[0]):
                    blocks.append({
                        'x': spikeX,
                        'y': spikeY,
                        'width': 25,
                        'height': 25,
                        'type': 'spike',
                        'animFrame': 0
                    })  
            landingY = max(currentY, groundLevel - 20)
            landingX = startX + spikeCount * spikeWidth + 10
            if not (landingX < playerSpawnZone[1] and landingX + 100 > playerSpawnZone[0]):
                blocks.append({
                    'x': landingX,
                    'y': landingY,
                    'width': 100,
                    'height': 20,
                    'type': 'platform',
                    'moving': False
                })
            currentX = startX + spikeCount * spikeWidth + 110
            currentY = landingY
        else:  
            currentX += 100
    return blocks, coins, powerUps
