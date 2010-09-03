#! /usr/bin/python2.6
#  -*- coding: utf-8 -*-
# Requires pygame
#       Py3De - Python 3D engine.
#       
#       Copyright 2010 Mateus Zitelli <zitellimateus@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.


import pygame
from pygame.locals import *
from math import *
from time import *
from random import *
import numpy as np
import sys

class Circle: #Point object
	def __init__(self,x,y,z,size=1,color = (255,0,0)):
		self.x , self.y , self.z, self.size = x , y , z, size # Point location
		self.pertence = []
		self.color = color

	def render(self, surface, x, y, radius):
		pygame.draw.circle(surface,self.color,(x,y),radius)
		
class Luz:
	def __init__(self,x,y,z,lum):
		self.x,self.y,self.z = x,y,z
		self.lum = lum

class Face:
	def __init__(self,lista,color):
		self.points = lista
		self.color = color
		self.render_points = []
		self.med = ()
		self.m = []

	def render(self,surface):
		#pygame.draw.polygon(surface,self.color, self.render_points)
		pygame.draw.lines(surface, (255,0,0),self.render_points[0], self.render_points,1)


class Camera:
	def __init__(self,x,y,z,rotationx,rotationy,zoom):
		self.angle = 90.0/zoom
		self.x,self.y,self.z,self.rx,self.ry,self.zoom = x,y,z,rotationx,rotationy,zoom

class Scene:
	def __init__(self, width, eigth, camera):
		self.width = width
		self.eigth = eigth
		self.objects = [] #Objects in the scene
		self.faces = []
		self.surface = pygame.display.set_mode((width, eigth))
		self.camera = camera
		self.view_distance = (self.width) / (tan(radians(self.camera.angle)/2.0))
		
	def render_order(self):
		if len(self.faces):
			self.m_point()
			self.ordem_mesh = sorted(self.faces,key = lambda face: sqrt((face.med[0]-self.camera.x)**2+(face.med[1]-self.camera.y)**2+(face.med[2]-self.camera.z)**2))
			self.cores()
			self.ordem_mesh.reverse()
		self.ordem_point = sorted(self.objects,key = lambda point: sqrt((point.x-self.camera.x)**2+(point.y-self.camera.y)**2+(point.z-self.camera.z)**2))
		self.ordem_point.reverse()
		
	def m_point(self):
		for face in self.faces:
			maximo = (max(face.points, key = lambda ponto: ponto.x),max(face.points, key = lambda ponto: ponto.y),max(face.points, key = lambda ponto: ponto.z))
			minimo =  (min(face.points, key = lambda ponto: ponto.x),min(face.points, key = lambda ponto: ponto.y),min(face.points, key = lambda ponto: ponto.z))
			face.med = ((maximo[0].x+minimo[0].x)/2.0,(maximo[1].y+minimo[1].y)/2.0,(maximo[2].z+minimo[2].z)/2.0)
			
	def cores(self):
		max_min_z = [max(self.faces,key = lambda face: face.med[2]).med[2],min(self.faces,key = lambda face: face.med[2]).med[2]]
		for face in self.faces:
			if max_min_z[0]-max_min_z[1]:
				cor = (face.med[2]-max_min_z[1])/(max_min_z[0]-max_min_z[1])*255
			else:
				cor = 175
			#if cor > 255: print cor
			face.color = (255-cor,255-cor,255-cor)

	def clean(self):
		self.faces = []
		self.objects = []
			
	def event_checker(self):
		vel = 1
		vela = radians(10)
		pygame.event.get()
		key_pressed = pygame.key.get_pressed()
		mouse = pygame.mouse.get_pressed()
		chaged = False
		if key_pressed[K_ESCAPE]:
			pygame.quit()
			sys.exit()
		if key_pressed[K_RIGHT]:
			for obj in self.objects:
				anglo = atan2(obj.x,obj.z)
				dist = sqrt(obj.z**2 + obj.x ** 2)
				obj.x = sin(anglo+vela)*dist
				obj.z = cos(anglo+vela)*dist
				chaged = True
		if key_pressed[K_LEFT]:
			for obj in self.objects:
				anglo = atan2(obj.x,obj.z)
				dist = sqrt(obj.z**2 + obj.x ** 2)
				obj.x = sin(anglo-vela)*dist
				obj.z = cos(anglo-vela)*dist
				chaged = True
		if key_pressed[K_UP]:
			for obj in self.objects:
				anglo = atan2(obj.y,obj.z)
				dist = sqrt(obj.z**2 + obj.y ** 2)
				obj.y = sin(anglo+vela)*dist
				obj.z = cos(anglo+vela)*dist
				chaged = True
		if key_pressed[K_DOWN]:
			for obj in self.objects:
				anglo = atan2(obj.y,obj.z)
				dist = sqrt(obj.z**2 + obj.y ** 2)
				obj.y = sin(anglo-vela)*dist
				obj.z = cos(anglo-vela)*dist
				chaged = True
		if key_pressed[K_e]:
			for obj in self.objects:
				anglo = atan2(obj.y,obj.x)
				dist = sqrt(obj.x**2 + obj.y ** 2)
				obj.y = sin(anglo-vela)*dist
				obj.x = cos(anglo-vela)*dist
				chaged = True
				
		if key_pressed[K_q]:
			for obj in self.objects:
				anglo = atan2(obj.y,obj.x)
				dist = sqrt(obj.x**2 + obj.y ** 2)
				obj.y = sin(anglo+vela)*dist
				obj.x = cos(anglo+vela)*dist
				chaged = True


		if mouse[0]:
			self.camera.z += vel
			chaged = True
		if mouse[1]:
			self.camera.z -= vel
			chaged = True
		if chaged: self.render_order()

	def rotacao(self):
		for obj in self.corpos:
			anglo = atan2(obj.x,obj.z)
			dist = sqrt(obj.z**2 + obj.x ** 2)
			a,b = sin(radians(anglox)),cos(radians(anglox))
			obj.x = a*dist
			obj.z = b*dist
			dist = sqrt(obj.z**2 + obj.y ** 2)
			anglo = atan2(obj.y,obj.z)
			a,b = sin(radians(angloy)),cos(radians(angloy))
			obj.y = a*dist
			obj.z = b*dist

	def render(self,mesh = True, vertex = True):
		self.surface.fill((0,0,0))
		if  mesh and len(self.faces):
			for face in self.ordem_mesh:
				for obj in face.points:
					anglo1 = atan2(obj.x,obj.z)
					distx = sqrt(obj.z**2 + obj.x ** 2)
					a1,b1 = sin(anglo1+radians(self.camera.rx)),cos(anglo1+radians(self.camera.rx))
					ax = a1*distx
					az = b1*distx
					anglo2 = atan2(obj.y,az)
					disty = sqrt(az**2 + obj.y ** 2)
					a2,b2 = sin(anglo2+radians(self.camera.ry)),cos(anglo2+radians(self.camera.ry))
					ay = a2*disty
					az += b2*disty
					dist = sqrt((self.camera.x-ax)**2+(self.camera.y-ay)**2+(self.camera.z-az)**2)
					aparent_x = (ax-self.camera.x)*self.view_distance/dist
					aparent_y = -(ay-self.camera.y)*self.view_distance/dist
					face.render_points.append((aparent_x+self.width/2,aparent_y+self.eigth/2))
				face.render(self.surface)
				face.render_points = []
		if vertex:
			self.render_order()
			for obj in self.ordem_point:
				anglo1 = atan2(obj.x,obj.z)
				distx = sqrt(obj.z**2 + obj.x ** 2)
				a1,b1 = sin(anglo1+radians(self.camera.rx)),cos(anglo1+radians(self.camera.rx))
				ax = a1*distx
				az = b1*distx
				anglo2 = atan2(obj.y,az)
				disty = sqrt(az**2 + obj.y ** 2)
				a2,b2 = sin(anglo2+radians(self.camera.ry)),cos(anglo2+radians(self.camera.ry))
				ay = a2*disty
				az += b2*disty
				dist = sqrt((self.camera.x-ax)**2+(self.camera.y-ay)**2+(self.camera.z-az)**2)
				if dist == 0: dist = 0.01
				aparent_x = (ax-self.camera.x)*self.view_distance/dist
				aparent_y = -(ay-self.camera.y)*self.view_distance/dist
				aparent_size = obj.size*300/dist
				obj.render(self.surface,aparent_x+self.width/2,aparent_y+self.eigth/2,aparent_size)

		pygame.display.flip()

	def demo(self):
		open_obj("./Objs/macaco.obj",self)
		while True:
			self.event_checker()
			self.render(1,0)


def open_obj(arquivo,cena):
	arq = open(arquivo,"r")
	for line in arq.readlines():
		line = line.split()
		if "v" in line:
			if line[0] == "v":
				cena.objects.append(Circle(float(line[1])*-1,float(line[2])*-1,float(line[3])*-1,0.1))
		if "f" in line:
			if line[0] == "f":
				pontos = []
				for i in line[1:]:
					i = i.split("/")[0]
					pontos.append(cena.objects[int(i)-1])
				ra = random()
				cena.faces.append( Face( pontos, (255*ra,255*ra,255*ra) ) )
	if len(cena.faces):
		cena.m_point()
		cena.cores()
	cena.render_order()

if __name__ ==  "__main__":
	cena = Scene(1300,800,Camera(0,0,-50,0,0,2))
	cena.demo()

