import sys #importation des modules
import os
import pygame
import time
import random
from pygame.locals import *

"""
------------------------------  INITIALISATION DE PYGAME  ------------------------------
"""
pygame.init()
pygame.font.init()


"""
------------------------------  INITIALISATION DU MODULE SONORE  ------------------------------
"""
try:
	pygame.mixer.pre_init(44100,-16,2,2048)
	pygame.mixer.init()
except pygame.error:
	print("Avertissement #2 : Aucune interface audio trouvée  ")


"""
------------------------------  PARAMETRES  ------------------------------
"""
	## On récupère la taille de l'ecran
l,h = pygame.display.Info().current_w,pygame.display.Info().current_h  
	## On créer la fenêtre du jeu
ecran = pygame.display.set_mode((l,h- 100))

	## Ligne pour bloquer les messages dans le terminal
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

"""
------------------------------  FONCTIONS INTERMEDIAIRES  ------------------------------	
"""

def texte(text,size):
	"""
	Entrées :	- text : Texte à afficher
				- size : Taille du texte

	Sortie  :	- Le texte prêt à afficher  	
	"""
	f = pygame.font.Font(None,size)
	textFont = f.render(text,True,(255,255,255))
	return textFont

def dansBoite(box,x,y):
	"""
	Entrées	:	- box : Liste de tupple (représente les coordonées du coin haut gauche et bas droit d'un rectangle)
				- x : position x
				- y : possition y

	Sortie  : 	- Indique si le point (x,y) est dans le rectangle représentée par box
	"""
	if x>box[0][0] and x < box[1][0] and  y>box[0][1] and y < box[1][1]:
		return True
	else:
		return False

def music(chemin):
	"""
	Lance le son chemin et ne plante pas si il n'y a pas de moyen de lire le son
	"""
	try:
		pygame.mixer.music.load(chemin)  
		pygame.mixer.music.play(-1)
	except pygame.error:
		v = os.path.exists(chemin)	## Vérifie si le fichier existe
		if not v:
			raise Exception("Erreur #1 : Le fichier audio n'a pas été trouvé -> {}".format(chemin))
		
def image(chemin,x,y):
	"""Creer une instance image de dimension x*y """
	try:
		img = pygame.image.load(chemin)
		img = pygame.transform.scale(img, (x, y))
		return img
	except pygame.error :
		v = os.path.exists(chemin)	## Vérifie si le fichier existe
		if not v:
			raise Exception("Erreur #3 : Le fichier image n'a pas été trouvé -> {}".format(chemin))

"""
------------------------------  SCENES DU JEU  ------------------------------
"""

def intro():
	"""
	Affiche le générique d'introduction
	"""
	jeu = True
	music("data/music/intro.mp3")
		## Taille de la police
	size = 80
		## Génération des textes
	leo = texte("Léo ...", size)
	Lv = texte("... et Louis-Victor",size)
	presente = texte("Présentent ",size)
		## Variable temporelle
	t=0	
		## Temps par texte
	t1=1/3
		# Boucle de l'affichage
	while jeu:
			## Detection de la croix
		for event in pygame.event.get():
			if event.type == QUIT:
				jeu = False

		if t < t1:
			ecran.fill((0,0,0))
			ecran.blit(leo, (l/2,h/2)) 
		elif t<2*t1:
			ecran.fill((0,0,0))
			ecran.blit(Lv, (l/2,h/2)) 
		elif t<3*t1:
			ecran.fill((0,0,0))
			ecran.blit(presente, (l/2,h/2)) 
		else:
			menu()
			jeu = False

		time.sleep(0.002)
		pygame.display.flip()
		t+=0.002
		
def menu():
	"""
	Affiche le menu
	"""
	music("data/music/menu.mp3")
	jeu = True
		## Textes au repos
	optiontxt = texte("Infos",80)
	Jouertxt = texte("Jouer",80)
	Quittertxt = texte("Quitter",80)
		## Textes quand la souris passe dessus
	optiontxtS = texte("Infos",100)
	JouertxtS = texte("Jouer",100)
	QuittertxtS = texte("Quitter",100) 
	Merci = texte("Merci d'avoir joué !",100)

		## Rectangles autour des textes
	jouerBox = [(l/2,(h/2)-100),((l/2+200,(h/2)))]
	optionBox = [(l/2,(h/2)),((l/2+200,(h/2)+100))]
	QuitterBox = [(l/2,(h/2)+100),((l/2+230,(h/2)+200))]

	while jeu:
			## On récupère la possition de la souris
		x,y = pygame.mouse.get_pos()

			## Detection de la croix
		for event in pygame.event.get():
				if event.type == QUIT:
					jeu = False
		
		ecran.fill((0,0,0))
		if dansBoite(jouerBox,x,y):
			ecran.blit(JouertxtS, jouerBox[0]) 
				## Récupère l'état des boutons sous la forme d'un tupple 0/1 (Gauche,molette,Droite)
			press = pygame.mouse.get_pressed()
			if press[0] == 1:
				print("Jouer")
		else:
			ecran.blit(Jouertxt, jouerBox[0])

		if dansBoite(optionBox,x,y):
			ecran.blit(optiontxtS, optionBox[0]) 
			press = pygame.mouse.get_pressed()
			if press[0] == 1:
				info()
				jeu = False
		else:		
			ecran.blit(optiontxt, optionBox[0]) 

		if dansBoite(QuitterBox,x,y):	
			ecran.blit(QuittertxtS, QuitterBox[0]) 
			press = pygame.mouse.get_pressed()
			if press[0] == 1:
				ecran.fill((0,0,0))
				ecran.blit(Merci, (l/2-200,h/2)) 
				pygame.display.flip()
				time.sleep(1)
				jeu = False
		else:
			ecran.blit(Quittertxt, QuitterBox[0]) 

		time.sleep(0.002)
		pygame.display.flip()


		

def info():
	jeu = True
	flecheNorm = image("data/picture/Back_Arrow.png",100,100)
	flecheBig = image("data/picture/Back_Arrow.png",150,150)
	# flecheNorm = pygame.image.load("data/picture/Back_Arrow.png")
	# flecheNorm = pygame.transform.scale(flecheNorm, (100, 100))
	# flecheBig = pygame.image.load("data/picture/Back_Arrow.png")
	# flecheBig = pygame.transform.scale(flecheBig, (150, 150))

	Titre = texte("Titre",100)
	create = texte("Jeu Créé par Louis-Victor et Léo",50)
	version = texte("Version : 0.1",50)
	Annee = texte("MPSI - 2019/2020",50)

	flecheBox = [(50,50),(150,150)]

	while jeu:
			## On récupère la possition de la souris
		x,y = pygame.mouse.get_pos()

		ecran.fill((0,0,0))
		
			## Detection de la croix
		for event in pygame.event.get():
				if event.type == QUIT:
					jeu = False
		if dansBoite(flecheBox,x,y):
			ecran.blit(flecheBig, (flecheBox[0][0],flecheBox[0][1]))
			press = pygame.mouse.get_pressed()
			if press[0] == 1:
				menu()
				jeu=False
		else:
			ecran.blit(flecheNorm, (flecheBox[0][0],flecheBox[0][1]))

		ecran.blit(Titre, (l/2,50))
		ecran.blit(create, (l/2,200))
		ecran.blit(version, (l/2,300)) 
		ecran.blit(Annee, (l/2,400))

		time.sleep(0.002)
		pygame.display.flip()

def jeuEspace():
	jeu = True
	fusée = image("data/picture/fusee.png",100,100)
	# fuséeflamme = image("data/picture/fuseeflamme.png",100,100)
	angle = 0
	incr_angle = 90
	x,y= l/2,h/2
	

	while jeu:
		for event in pygame.event.get():
			if event.type == QUIT:
				jeu = False
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					jeu = False
				if event.key == K_z:
					print("Z")
				if event.key == K_s:
					print("S")
				if event.key == K_d:
					fusée = pygame.transform.rotate(fusée, incr_angle)
					print("d")
				if event.key == K_q:
					fusée = pygame.transform.rotate(fusée, incr_angle)
					print("q")

		# fusée = pygame.transform.rotate(fusée, angle)
		ecran.fill((0,0,0))
		# ecran.blit(fond,(0,0))
		ecran.blit(fusée, (x,y)) # perso
		time.sleep(0.002)
		pygame.display.flip()




		
		


"""
while jeu:
	for event in pygame.event.get():
		if event.type == QUIT:
			jeu = False
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				jeu = False
			if event.key == K_z:
				print("Z")
			if event.key == K_s:
				print("S")
			if event.key == K_d:
				print("D")
			if event.key == K_q:
				print("Q")

	# ecran.blit(fond,(0,0))
	# ecran.blit(ballon, (x,y)) # perso
	time.sleep(0.002)
	pygame.display.flip()
"""

jeuEspace()






