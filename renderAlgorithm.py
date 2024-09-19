import os
import math

def getCommandLines(txt):
    str_command = txt.split('\n');
    return str_command

def getCommandTitle(cmd):
    title = cmd.split(' ')[0]
    return title

def renderOnce(win, txt):
    commands = getCommandLines(txt)
    for cmd in commands:
        title = getCommandTitle(cmd)
        if title == '#domain:':
            win.domain(cmd)
        if title == '#sphere:':
            win.sphere(cmd)
        if title == '#cylinder:':
            win.cyliner(cmd)
        # if title == '#plate:':
        #     win.plane(cmd)
        if title == '#box:':
            win.box(cmd)
        # if title == '#triangle:':
        #     win.triangle(cmd)
        # if title == '#cone:':
        #     win.cone(cmd)

def CalculateAngle(xMin, xMax, yMin, yMax, zMin, zMax):
    vector = [xMax - xMin, yMax - yMin, zMax - zMin]
    angleX = math.atan2(vector[1], vector[0])
    angleX = angleX*180/math.pi
    angleY = 180 - angleX
    angleZ = math.atan2(vector[2], math.sqrt((vector[0]**2 + vector[1]**2)))
    angleZ = angleZ*180/math.pi
    return angleX, angleY, angleZ

def CalculateMovement(axisX, axisY, axisZ, angleX, angleY, angleZ):
    # rotate around x axis
    moveY = axisY*math.cos(angleX * math.pi / 180) - axisZ*math.sin(angleX * math.pi / 180) 
    moveZ = axisY*math.sin(angleX * math.pi / 180) + axisZ*math.cos(angleX * math.pi / 180)
    axisY = moveY
    axisZ = moveZ
    # rotate around y axis
    moveX = axisX*math.cos(angleY * math.pi / 180) + axisZ*math.sin(angleY * math.pi / 180) 
    moveZ = -axisX*math.sin(angleY * math.pi / 180) + axisZ*math.cos(angleY * math.pi / 180)
    axisX = moveX
    axisZ = moveZ
    # rotate around z axis
    moveX = axisX*math.cos(angleZ * math.pi / 180) - axisY*math.sin(angleZ * math.pi / 180) 
    moveY = axisX*math.sin(angleZ * math.pi / 180) + axisY*math.cos(angleZ * math.pi / 180)
    axisX = moveX
    axisY = moveY
    
    return axisX, axisY, axisZ