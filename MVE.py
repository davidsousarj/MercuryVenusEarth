#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Average Distance between Mercury and Earth vs. Venus and Earth
# See https://physicstoday.scitation.org/do/10.1063/PT.6.3.20190312a/full/
# Author: David Sousa david@pos.iq.ufrj.br 
# License: Creative Commons

# Importing Libraries
import pygame
import sys
from pygame.locals import *
import numpy as np
from math import pi, sqrt, cos, sin

# Initial Data (Units: Time/years; Distance/AU)
M_Af = 0.307499 #aphelion
M_Pr = 0.466697 #perihelion
M_e  = 0.205630 #eccentricity
M_T  = 0.31726  #synodic period

V_Af = 0.718    #aphelion
V_Pr = 0.728    #perihelion
V_e  = 0.006772 #eccentricity
V_T  = 1.5987   #synodic period

E_Af = 0.98329134 #aphelion
E_Pr = 1.01671388 #perihelion
E_e  = 0.01671123 #eccentricity
E_T  = 1.0000     #synodic period

# ellipse parameters
M_a = (M_Af + M_Pr)/2
M_c = M_a*M_e
M_b = sqrt(1 - M_e)*M_a

V_a = (V_Af + V_Pr)/2
V_c = V_a*V_e
V_b = sqrt(1 - V_e)*V_a

E_a = (E_Af + E_Pr)/2
E_c = E_a*E_e
E_b = sqrt(1 - E_e)*E_a

# Initial positions
x_M, y_M = (M_a, 0)
x_V, y_V = (V_a, 0)
x_E, y_E = (E_a, 0)

# Average distances
Av_ME = E_a - M_a
Av_VE = E_a - V_a

# Time
h  = 1/360.
tf = 10000
t  = np.arange(0,tf,h)

# Initialize the screen
w = 255
red,green,blue,white,black = (w,0,0),(0,w,0),(0,0,w),(w,w,w),(0,0,0)

sx, sy = 600, 600  # screen size in pixels
SX, SY = 2.0, 2.0  # screen size in AU
px, py = 8, 8      # planet size
margin = 15

clocktick = 50 # 0 for fastest animation, microseconds elapsed between steps
pygame.init()
clock  = pygame.time.Clock()
screen = pygame.display.set_mode((sx,sy))
myfont = pygame.font.SysFont("Sans", 20)
pygame.display.set_caption( 'Mercury, Venus, and Earth by DavidSousa' )

score = pygame.Rect(margin, 510, sx - 2*margin, 80)
sky   = pygame.Rect(margin, margin, sx - 2*margin, sy - 2*margin - 100)

orb1  = pygame.Rect(sx/2. - sx/2.*M_a/SX, sy/2. - sy/2.*M_b/SY, sx*M_a/SX, sy*M_b/SY)
orb2  = pygame.Rect(sx/2. - sx/2.*V_a/SX, sy/2. - sy/2.*V_b/SY, sx*V_a/SX, sy*V_b/SY)
orb3  = pygame.Rect(sx/2. - sx/2.*E_a/SX, sy/2. - sy/2.*E_b/SY, sx*E_a/SX, sy*E_b/SY)
# Movement process
for i in xrange(0,len(t)-1): 
	# Parametric equations of the ellipse (assuming constant velocity)
	x_M = M_a*cos(2*pi*t[i]/M_T)
	y_M = M_b*sin(2*pi*t[i]/M_T)
	x_V = V_a*cos(2*pi*t[i]/V_T)
	y_V = V_b*sin(2*pi*t[i]/V_T)
	x_E = E_a*cos(2*pi*t[i]/E_T)
	y_E = E_b*sin(2*pi*t[i]/E_T)
	# Distances
	d_ME = sqrt((x_E - x_M)**2 + (y_E - y_M)**2)
	d_VE = sqrt((x_E - x_V)**2 + (y_E - y_V)**2)
	# Average distances
	Av_ME = (Av_ME*i + d_ME)/(i+1)
	Av_VE = (Av_VE*i + d_VE)/(i+1)
	
	# Close event
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit(); sys.exit();

	# Drawing the screen 
	msElapsed = clock.tick(clocktick)

	X1 = int(sx/2. + sx/2.*x_M/SX )
	Y1 = int(sy/2. - sy/2.*y_M/SY )
	X2 = int(sx/2. + sx/2.*x_V/SX )
	Y2 = int(sy/2. - sy/2.*y_V/SY )
	X3 = int(sx/2. + sx/2.*x_E/SX )
	Y3 = int(sy/2. - sy/2.*y_E/SY )

	screen.fill((200,200,200))
	pygame.draw.rect(screen, white, sky, 0)
	pygame.draw.circle(screen, red, (sx//2, sy//2), 10)
	pygame.draw.ellipse(screen, black, orb1, 1)
	pygame.draw.ellipse(screen, black, orb2, 1)
	pygame.draw.ellipse(screen, black, orb3, 1)

	planet1 = pygame.Rect(X1, Y1, px, py)
	planet2 = pygame.Rect(X2, Y2, px, py)
	planet3 = pygame.Rect(X3, Y3, px, py)

	pygame.draw.rect(screen, black, planet1, 0)
	pygame.draw.rect(screen, green, planet2, 0)
	pygame.draw.rect(screen, blue , planet3, 0)
	pygame.draw.rect(screen, white, score,   0)

	d1="Dist. media Mercurio-Terra = %.6f AU" %Av_ME
	d2="Dist. media Venus-Terra    = %.6f AU" %Av_VE
	tempo="Tempo = %.3f / %.3f Anos" %(t[i],t[-1])
	label1 = myfont.render(d1, 1, blue, white)
	label2 = myfont.render(d2, 1, blue, white)
	label3 = myfont.render(tempo, 1, blue, white)
	screen.blit(label1, (margin, sy - 90))
	screen.blit(label2, (margin, sy - 70))
	screen.blit(label3, (margin, sy - 30))

	pygame.display.update()

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit(); sys.exit();
