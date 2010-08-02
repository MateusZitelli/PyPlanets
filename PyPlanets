#! /usr/bin/python2.6
#  -*- coding: utf-8 -*-
# Requires pygame
"""
Copyright (C) 2010 Mateus Zitelli (zitellimateus@gmail.com)
PyGravity is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import pygame
from pygame.locals import *
from math import *
import sys
import time
from decimal import *
import random
pygame.init()

class Corpo:
	def __init__(self,cordx,cordy,velxA,velyA,massa): #(x,y,speedX,speedY,mass)
		self.x = cordx
		self.y = cordy
		self.mass = massa 
		self.velx = float(velxA/10**0) #Cuidado: dependendo do valor pode estourar o Float
		self.vely = float(velyA/10**0)
		self.raio = (self.mass/pi*5)**(1/2.0)
		self.cor = (int(255-random.random()*200),int(255-random.random()*200),int(255-random.random()*200))

class Simulacao:
	def __init__(self,tamanho):
		self.tamanho = tamanho
		self.surface = pygame.display.set_mode((self.tamanho[0],self.tamanho[1]))
		self.corpos = []
		self.zoom = 1.0
		self.vezes = 0
		self.pintar = False
		self.pausado = True
		self.valores = {}


	def interacao(self,corpo_a,corpo_b):
		if not (corpo_a,corpo_b) in self.valores and not (corpo_b,corpo_a) in self.valores:
			const_gravitacional = 6.67428E-11
			xdif,ydif = (corpo_a.x-corpo_b.x) , (corpo_a.y-corpo_b.y)
			dist = sqrt((xdif)**2+(ydif)**2) #Simplified to the next formula
			if dist < (corpo_a.raio+corpo_b.raio): dist = corpo_a.raio+corpo_b.raio
			forc = (const_gravitacional*(corpo_a.mass*10**10)*(corpo_b.mass*10**10))/(dist*10**6)**2 #F = (Constant*massA*massB)/dist**2
		else:
			if (corpo_b,corpo_a) in self.valores:
				val = self.valores[(corpo_b,corpo_a)]
				forc = val[0]
				xdif,ydif = -val[1][0],-val[1][1]
				dist = val[2]
		#velAbs = (a.velx+a.vely)				#    Correcao relativistica	     
		#c = 299792458.0/10**6					# Gera problemas na simualacao
		#massa_relativistica = a.mass/sqrt(1-velAbs**2/c**2)    #
		if dist <= corpo_a.raio+corpo_b.raio+10:
			aceleration = 0
		else:
			aceleration = (forc/corpo_a.mass)*10**3
		Xcomp = xdif/dist
		Ycomp = ydif/dist
		corpo_a.velx -= aceleration * Xcomp
		corpo_a.vely -= aceleration * Ycomp
		self.valores[(corpo_a,corpo_b)] = (forc,(xdif,ydif),dist)
		return forc
	##############################
	#Move os objetos a cada ciclo#
	##############################
	def move(self):
		self.valores = {}
		for cA in self.corpos:
			for cB in self.corpos:
				if cA != cB:
					self.interacao(cA,cB)

		for obj in self.corpos:
			obj.x += obj.velx
			obj.y += obj.vely
	#################################
	#"Pinta" os objetos a cada ciclo#
	#################################
	def draw(self):
		if not self.pintar:
			self.surface.fill((0,0,0))
		for C in self.corpos:
			#Simulacao de Zoom#
			distx = abs(C.x - self.tamanho[0]/2.0)
			disty = abs(C.y - self.tamanho[1]/2.0)
			if C.x < self.tamanho[0]/2.0:
				x = C.x + distx*(1-self.zoom)
			else:
				x = C.x - distx*(1-self.zoom)

			if C.y < self.tamanho[1]/2.0:
				y = C.y + disty*(1-self.zoom)
			else:
				y = C.y - disty*(1-self.zoom)

			pygame.draw.circle(self.surface,C.cor,(int(x),int(y)),int(round(C.raio*self.zoom)))
		pygame.display.flip()

	def orbitas(self,n): #cria corpos distribuidos uniformemente em um quadrado
		for i in range(n):
			tam = round(min((self.tamanho[0],self.tamanho[1]))/sqrt(n))
			y,x = divmod(i,int(round(sqrt(n))))
			self.corpos.append(Corpo(x*tam,y*tam,0,0,10))

	def criar(self,n,massa): #Cria corpos de forma randomica pela tela
		for i in range(n):
			self.corpos.append(Corpo(random.random()*self.tamanho[0],random.random()*self.tamanho[1],0,0,massa))

	def demo(self):
		self.zoom = 0.1
		self.corpos = []
		self.surface.fill((0,0,0))
		self.corpos.append(Corpo(400,-500,0.7,0.0,500.0))
		self.corpos.append(Corpo(400,1500,-0.7,0.0,500.0))
		self.corpos.append(Corpo(400,0,2.0,0.0,50.0))

	def scan(self): #Precisa de melhorias # Gera uma imagem do campo gravitacional.
		potencia = []
		self.valores = {}
		for i in range(180):
			for j in range(160):
				valponto = 0
				a = Corpo(i*5,j*5,0,0,1)
				for C in self.corpos:
					valponto += self.interacao(a,C)
				potencia.append(valponto)
		ma = max(potencia)
		for val in range(len(potencia)):
			y,x = divmod(val,160)
			temp = potencia[val]/float(ma)*255			
			pygame.draw.circle(self.surface,(temp,temp,temp),(x*5,y*5),1)
		print len(potencia)
		pygame.display.flip()
		while True:
			event = pygame.event.poll()
			if event.type == KEYDOWN:break

	def GetInput(self): #Verificacao de eventos
		key_pressed = pygame.key.get_pressed()
		mouse = pygame.mouse.get_pressed()

		for event in pygame.event.get():
			if event.type == QUIT or key_pressed[K_ESCAPE]:
				pygame.quit() #Fim do Script
				sys.exit()

			if mouse[0] and not key_pressed[K_n]:
				mouse_x,mouse_y = pygame.mouse.get_pos()
				#Correcao para o Zoom#
				distx,disty = abs(mouse_x-self.tamanho[0]/2.0),abs(mouse_y-self.tamanho[1]/2.0)
				if mouse_x < self.tamanho[0]/2.0:
					x = mouse_x + distx*(1-self.zoom**-1)
				else:
					x = mouse_x - distx*(1-self.zoom**-1)

				if mouse_y < self.tamanho[1]/2.0:
					y = mouse_y + disty*(1-self.zoom**-1)
				else:
					y = mouse_y - disty*(1-self.zoom**-1)
				print x,y
				self.corpos.append(Corpo(x,y,0.0,0.0,100.0))

			if mouse[1]:
				mouse_x,mouse_y = pygame.mouse.get_pos()
				#Correcao para o Zoom#
				distx,disty = abs(mouse_x-self.tamanho[0]/2.0),abs(mouse_y-self.tamanho[1]/2.0)
				if mouse_x < self.tamanho[0]/2.0:
					x = mouse_x + distx*(1-self.zoom**-1)
				else:
					x = mouse_x - distx*(1-self.zoom**-1)

				if mouse_y < self.tamanho[1]/2.0:
					y = mouse_y + disty*(1-self.zoom**-1)
				else:
					y = mouse_y - disty*(1-self.zoom**-1)
				print x,y
				self.corpos.append(Corpo(x,y,0.0,0.0,1000.0))

			if mouse[2]:
				mouse_x,mouse_y = pygame.mouse.get_pos()
				#Correcao para o Zoom#
				distx,disty = abs(mouse_x-self.tamanho[0]/2.0),abs(mouse_y-self.tamanho[1]/2.0)
				if mouse_x < self.tamanho[0]/2.0:
					x = mouse_x + distx*(1-self.zoom**-1)
				else:
					x = mouse_x - distx*(1-self.zoom**-1)

				if mouse_y < self.tamanho[1]/2.0:
					y = mouse_y + disty*(1-self.zoom**-1)
				else:
					y = mouse_y - disty*(1-self.zoom**-1)
				print x,y
				self.corpos.append(Corpo(x,y,2.0,0.0,100.0))

			if key_pressed[K_DOWN]: #Move a camera para BAIXO quando apertado a SETA PARA BAIXO.
				for i in self.corpos:
					i.y -= 50/self.zoom

			elif key_pressed[K_UP]: #Move a camera para CIMA quando apertado a SETA PARA CIMA.
				for i in self.corpos:

					i.y += 50/self.zoom

			elif key_pressed[K_LEFT]: #Move a camera para ESQUERDA quando apertado a SETA PARA ESQUERDA.
				for i in self.corpos:
					i.x += 50/self.zoom

			elif key_pressed[K_RIGHT]: #Move a camera para DIREITA quando apertado a SETA PARA DIREITA.
				for i in self.corpos:
					i.x -= 50/self.zoom

			if key_pressed[K_r]: #Deixa o rastro dos objetos #Precisa de melhoras, nao funciona com a variacao do zoom.
				self.pintar = not self.pintar

			elif key_pressed[K_c]: #Deleta todos objetos da tela
				self.corpos = []
				self.surface.fill((0,0,0))
				self.zoom = 1.0

			elif key_pressed[K_n] and mouse[0]:	#				Cria um novo corpo na tela				      #
				local = pygame.mouse.get_pos()  #A velocidade e definida pela distancia que o mouse for arrastado do ponto de inicio do clique#
				tela_rastro = pygame.display.set_mode((self.tamanho[0],self.tamanho[1]))#		Estado rudimentar, precisa de melhoras			      #
				while True:
					tela_rastro.fill((0,0,0))
					for event in pygame.event.get():
						pass
					ate = pygame.mouse.get_pos()
					velocidadeX = (ate[0]-local[0])/100.0
					velocidadeY = (ate[1]-local[1])/100.0
					pygame.draw.line(tela_rastro,(255,255,255),local,ate)
					pygame.display.flip()
					event2 = pygame.event.poll()
					if event2.type == MOUSEBUTTONUP: break
				print "New Body:"
				massa = raw_input("Mass:")
				self.corpos.append(Corpo(local[0],local[1],velocidadeX,velocidadeY,float(massa)))

			elif key_pressed[K_p]: #tecla P => Pausa/Roda o jogo
				self.pausado = not self.pausado

			elif key_pressed[K_t]: #Tecla T => Corpos randomicos pela tela
				self.criar(input("How many Bodies?"),input("\nMass:"))

			elif key_pressed[K_KP_PLUS]: #Tecla + => Almenta o Zoom
				self.zoom *= 2.0

			elif key_pressed[K_KP_MINUS]: #Tecla - => Diminui o Zoom
				self.zoom /= 2.0

			elif key_pressed[K_o]: #Tecla O => Gera quadrado de corpos
				self.orbitas(input("How many Bodies?"))

			elif key_pressed[K_0]: #Tecla 0 => Zoom volta ao padrao
				self.zoom = 1.0

			elif key_pressed[K_s]: #Tecla S => Scan do campo gravitacional
				self.scan()

			elif key_pressed[K_d]: #Tecla D => Demo: 3 body problem
				self.demo()



	def Collision_with_edge(self): #Detecta colisao com as bordas, movendo os corpos pro outro lado#
		for P in self.corpos:
			if P.x > self.tamanho[0]:   P.x = 0;
			if P.x < 0:     P.x = self.tamanho[0];
			if P.y > self.tamanho[1]:   P.y = 0;
			if P.y < 0:     P.y = self.tamanho[1];

	#Detecta a colisao estre objetos#
	def aglomerationDetect(self):
		for C in self.corpos:
			for C2 in self.corpos:
				if C != C2:
					Distancia2 = sqrt(  ((C.x-C2.x)**2)  +  ((C.y-C2.y)**2)  )

					if Distancia2 < (C.raio+C2.raio) and Distancia2 > (C.raio+C2.raio)/3.0*2: #Objects collision
						Distancia = C.raio+C2.raio
						dif = (C.x-C2.x,C.y-C2.y)
						anglo = atan2(dif[0],dif[1])
						razao = C.raio/C2.raio
						inter = (C.x+C.raio*-sin(anglo),C.y+C.raio*-cos(anglo))
						C.x = inter[0] + C.raio*sin(anglo)
						C.y = inter[1] + C.raio*cos(anglo)
						C2.x = inter[0] + C2.raio*-sin(anglo)
						C2.y = inter[1] + C2.raio*-cos(anglo)
						C.velx = (C.velx*C.mass+C2.velx*C2.mass)/(C2.mass+C.mass)
						C.vely = (C.vely*C.mass+C2.vely*C2.mass)/(C2.mass+C.mass)
						C2.velx,C2.vely = C.velx,C.vely

					elif Distancia2 <= (C.raio+C2.raio)/3.0*2: #Objects Fusion
						C.velx = ((C.mass*C.velx)+(C2.mass*C2.velx))/(C.mass+C2.mass)
						C.vely = ((C.mass*C.vely)+(C2.mass*C2.vely))/(C.mass+C2.mass)
						C.x = ((C.mass*C.x)+(C2.mass*C2.x))/(C.mass+C2.mass)
						C.y = ((C.mass*C.y)+(C2.mass*C2.y))/(C.mass+C2.mass)
						C.mass += C2.mass
						C.raio = sqrt(C.mass/pi*5)
						C.cor = ((C.cor[0]+C2.cor[0])/2.0,(C.cor[1]+C2.cor[1])/2.0,(C.cor[2]+C2.cor[2])/2.0)
						self.corpos.remove(C2)

	def main_loop(self): #Roda a simulacao
		clock = pygame.time.Clock()
		while True:
			clock.tick(200)
			self.vezes += 1
			self.GetInput()
			if not self.pausado:
				self.move()
				self.aglomerationDetect()
				#self.Collision_with_edge()
			self.draw()

if __name__ == "__main__":
	if not len(sys.argv[1:]):
		print "The correct syntax is \'python pygravity X_size Y_size\'"
		print "But the simulation will run in the default mode (800x600)."
		jogo = Simulacao((800,600))
	elif len(sys.argv[1:]) == 2:
		jogo = Simulacao((int(sys.argv[1]),int(sys.argv[2])))
	else:
		print "The correct sintax is \'python pygravity X_size Y_size\'"
		sys.exit()
	jogo.main_loop()