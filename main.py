"""
Maxim Costa 103

Jeux Isola en python

version: non optimiser
version 1.0

"""

from pygame.locals import *
from os import system, name
from time import sleep
from tkinter import simpledialog
from random import randint as rdi

import csv
import tkinter as tk
import os
import pygame
import sys


class Game:
    def __init__(self):
        """
        initialise tout les variable de la classe
        """
        pygame.init()

        # Ouverture de la fenétre Pygame
        self.fenetre = None

        self.mode = mode
        self.Plateau = []

        self.turn = 0
        self.taille_sprite = 50

        self.White = (255, 255, 255)
        self.Black = (0, 0, 0)
        self.Red = (255, 0, 0)
        self.Blue = (0, 0, 255)
        self.Marron = (139, 69, 19)
        self.Green = (0, 255, 0)
        self.Grey = (128, 128, 128)

        self.nbPlayers = self.user_input(
            "Nombre de joueur (min:2,max:8) ", "nbPlayer")
        self.NamePlayer = self.user_input(
            "Enter le nom du joueur ", "NamePlayer", option=self.nbPlayers)
        self.list_of_pairs = [(self.NamePlayer[p1], self.NamePlayer[p2]) for p1 in range(
            len(self.NamePlayer)) for p2 in range(p1+1, len(self.NamePlayer))]
        self.save_Columns = ['Match', 'Winner', 'nbcoups']
        self.save = []
        self.csv_file = "Names.csv"

    def display(self):
        """
        permet d'afficher le plateau de jeux en ligne de commande pour debugger
        """
        for alpha in [" "]+[chr(i) for i in range(65, 73)]:
            print(f" {alpha}", end=" |")
        print()
        for k, i in enumerate(self.Plateau[1:-1]):
            print("-"*(len(i)*3+6))
            print(f" {k+1}", end=" | ")
            for j in i[1:-1]:
                print(" " if j == 0 else "#" if j == 3 else j, end=" | ")
            print()
        print("-"*(len(self.Plateau[-1])*3+6))

    def displayPygame(self):
        """
        permet d'afficher le plateau de jeux
        """
        num_ligne = 0
        for ligne in self.Plateau[1:-1]:
            num_case = 0
            for sprite in ligne[1:-1]:
                x = num_case * self.taille_sprite
                y = num_ligne * self.taille_sprite
                if sprite == 0:
                    pygame.draw.rect(
                        self.fenetre, self.White, (x+1, y+1, self.taille_sprite-2, self.taille_sprite-2))
                elif sprite == 3:
                    pygame.draw.rect(
                        self.fenetre, self.Black, (x, y, self.taille_sprite, self.taille_sprite))
                elif sprite == 1:
                    pygame.draw.rect(
                        self.fenetre, self.White, (x+1, y+1, self.taille_sprite-2, self.taille_sprite-2))
                    pygame.draw.rect(
                        self.fenetre, self.Blue, (x+4, y+4, self.taille_sprite-8, self.taille_sprite-8))
                elif sprite == 2:
                    pygame.draw.rect(
                        self.fenetre, self.White, (x+1, y+1, self.taille_sprite-2, self.taille_sprite-2))
                    pygame.draw.rect(
                        self.fenetre, self.Red, (x+4, y+4, self.taille_sprite-8, self.taille_sprite-8))
                num_case += 1
            num_ligne += 1
        # Rafraichissement de l'écran
        pygame.display.flip()

    def text_objects(self, text, color):
        """
        text = str(), color = tuple(int(),int(),int())
        permet d'afficher plus de init la police
        """
        smallfont = pygame.font.SysFont("comicsansms", 15)
        textSurface = smallfont.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def text_to_button(self, msg, color, buttonx, buttony, buttonwidth, buttonheight):
        """
        msg = str(), color = tuple(int(),int(),int()), buttonx = int(), buttony = int(), buttonwidth = int(), buttonheight = int()
        permet de créer un text dans une surface pygame (rect)
        """
        textSurf, textRect = self.text_objects(msg, color)
        textRect.center = ((buttonx + (buttonwidth / 2)),
                           buttony + (buttonheight / 2))
        self.fenetre.blit(textSurf, textRect)

    def PlateauGene(self):
         """
        genere un plateau de jeux plus initialise les cordonner de base des joueur ainsi que leur nombre de mouvement
        """
        self.CorJ = [[3, 1], [4, 8]]
        self.NBTour = [0, 0]

        self.Plateau = [[0 for x in range(8)] for y in range(6)]
        self.Plateau = [[3]+self.Plateau[i]+[3]
                        for i in range(len(self.Plateau))]
        self.Plateau = [[3]*len(self.Plateau[0])] + \
            self.Plateau+[[3]*len(self.Plateau[0])]
        for k, (y, x) in enumerate(self.CorJ):
            self.Plateau[y][x] = k+1

    def verifMove(self, old, new):
        """
        input: old = tuple(int(),int()), new = tuple(int(),int())
        old,new sont les cordonner de l'enciens et la nouvelle position
        ouput: true or false
        """
        try:
            if (1 >= (old[0] - new[0]) >= -1) and (1 >= (old[1] - new[1]) >= -1) and (self.Plateau[new[0]][new[1]] == 0):
                return True
            else:
                return False
        except IndexError:
            return False

    def Move(self, move):
        """
        input: pos = tuple(int(),int())
        pos sont les cordonner de la nouvelle postion
        ouput: true or false
        """
        if self.verifMove(self.CorJ[self.turn], move):
            self.Plateau[self.CorJ[self.turn][0]][self.CorJ[self.turn][1]] = 0
            self.Plateau[move[0]][move[1]] = self.turn + 1
            self.CorJ[self.turn] = list(move)
            return True
        else:
            return False

    def verifCaseBlock(self, pos):
        """
        input: pos = tuple(int(),int())
        pos sont les cordonner de la case a bloquer
        ouput: true or false
        """
        try:
            if self.Plateau[pos[0]][pos[1]] == 0:
                return True
            else:
                return False
        except IndexError:
            return False

    def CaseBlock(self, pos):
        """
        input: pos = tuple(int(),int())
        pos sont les cordonner de la case a bloquer
        ouput: true or false
        """
        if self.verifCaseBlock(pos):
            self.Plateau[pos[0]][pos[1]] = 3
            return True
        else:
            return False

    def changeTurn(self):
        """
        on change le tour
        """
        self.NBTour[self.turn] += 1
        self.turn = (self.turn+1) % 2

    def verifWin(self):
        """
        on verifie s'il y a un gagnant en regardant les case autour.
        ouput: true or false
        """
        y, x = self.CorJ[self.turn]
        verif = [(x+1, y), (x+1, y+1), (x+1, y-1), (x-1, y),
                 (x-1, y+1), (x-1, y-1), (x, y+1), (x, y-1)]
        verif = [False if (self.Plateau[y][x] != 0)
                 else True for (x, y) in verif]
        if not True in verif:
            return ((self.turn+1) % 2)
        else:
            return False

    def user_input(self, Otext, mode, option=None):
        """
        input: Otext = str(), mode = str(), option = int()

        Otext est le texte original afficher
        mode est le mode en cours (soit le nombre de joueur soit le nom des joueur)
        option est le nombre de joueur

        output: int() or list()
        """
        self.fenetre = pygame.display.set_mode((640, 480))
        center_x, center_y = 320, 240

        clock = pygame.time.Clock()
        font = pygame.font.SysFont('Comic Sans MS,Arial', 24)

        answer = "" if mode == "nbPlayer" else []
        i = 1
        text = Otext + " : " if mode == "nbPlayer" else Otext+f" {i} : "

        prompt = font.render(f"{text} : ", True, self.Blue)
        prompt_rect = prompt.get_rect(center=(center_x, center_y))

        user_input_value = ""
        user_input = font.render(user_input_value, True, self.Green)
        user_input_rect = user_input.get_rect(topleft=prompt_rect.topright)
        continuer = True
        while continuer:
            prompt = font.render(f"{text}", True, self.Blue)
            prompt_rect = prompt.get_rect(center=(center_x, center_y))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    continuer = False

                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if mode == "nbPlayer":
                            try:
                                answer = int(user_input_value)
                                if 8 >= answer >= 2:
                                    continuer = False
                                else:
                                    text = Otext + "error : "
                                    user_input_value = ""
                            except:
                                text = Otext + " !(NaN)! : "
                                user_input_value = ""
                        elif mode == "NamePlayer":
                            if user_input_value is not None:
                                answer.append(user_input_value)
                                if len(answer) < option:
                                    i += 1
                                    text = Otext + f" {i} : "
                                    user_input_value = ""
                                else:
                                    continuer = False

                    elif event.key == pygame.K_BACKSPACE:
                        user_input_value = user_input_value[:-1]
                    else:
                        user_input_value += event.unicode
                    user_input = font.render(
                        user_input_value, True, self.Green)
                    user_input_rect = user_input.get_rect(
                        topleft=prompt_rect.topright)
            clock.tick(30)
            self.fenetre.fill(0)
            self.fenetre.blit(prompt, prompt_rect)
            self.fenetre.blit(user_input, user_input_rect)
            pygame.display.flip()
        return answer

    def start(self):
        """
        permet de démarer je jeux et de faire n partie selon le nombre de joueur
        """
        self.PlateauGene()
        self.fenetre = pygame.display.set_mode((400, 400))

        loopget = 0
        for k, paire in enumerate(self.list_of_pairs):

            continuer = True
            win = False
            loopget = 0
            move = False
            pos = None
            error = None

            self.PlateauGene()
            while continuer:
                win = self.verifWin()
                if win != False:
                    print(
                        f"player {paire[win]} is the winner, nb move : {self.NBTour[win]}")
                    self.save.append(
                        {'Match': paire, 'Winner': paire[win], 'nbcoups': self.NBTour[win]})
                    continuer = False

                pygame.draw.rect(self.fenetre, self.White, (10, 310, 380, 80))
                self.text_to_button(
                    f"match: {' vs '.join(paire)}", self.Black, 10, 310, 380, 30)
                self.text_to_button(
                    f"turn : {paire[self.turn]}", self.Black, 10, 310, 380, 60)
                self.text_to_button(
                    f"turn : {'Choisir une case a bloquer (right click)' if loopget else 'Déplacer votre pion (left click)'}", self.Black, 10, 310, 380, 90)

                if error is not None:
                    self.text_to_button(
                        f"error : {error}", self.Black, 10, 310, 380, 120)
                pygame.time.Clock().tick(60)
                for event in pygame.event.get():
                    if event.type == QUIT:
                        continuer = False
                        quit()
                    if event.type == MOUSEBUTTONDOWN and event.button == 1 and loopget == 0:
                        move = ((event.pos[1] // 50) + 1,
                                (event.pos[0] // 50) + 1)
                        print(move)
                        if self.Move(move):
                            loopget = 1
                            error = None
                        else:
                            error = "Mouvement impossible"
                    if event.type == MOUSEBUTTONDOWN and event.button == 3 and loopget == 1:
                        pos = ((event.pos[1] // 50) + 1,
                               (event.pos[0] // 50) + 1)
                        print(pos)
                        if self.CaseBlock(pos):
                            self.changeTurn()
                            loopget = 0
                            error = None
                        else:
                            error = "Vous ne pouver pas bloquer cette case"
                self.displayPygame()
        try:
            with open(self.csv_file, 'w') as csvfile:
                csvfile.write(','.join(self.NamePlayer)+"\n")
                writer = csv.DictWriter(csvfile, fieldnames=self.save_Columns)
                writer.writeheader()
                for data in self.save:
                    writer.writerow(data)
        except IOError:
            print("I/O error")

 
game = Game()
game.start()
