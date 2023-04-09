import time
import pygame
import sys
import random
from copy import deepcopy

#déclarations pygame
pygame.init()
pygame.display.set_caption("Wish Blast")
screen = pygame.display.set_mode((300, 300))
background = pygame.image.load('board.png')
screen.blit( background, (0, 0) )
pygame.display.flip()

#images
croix = pygame.image.load('croix.png')
#screen.blit( croix, (0, 0) )
cercle = pygame.image.load('cercle.png')
#screen.blit( cercle, (100, 0) )

board = [[0] * 3 for i in range(3)]
winner = 0 #0 si égalité, 1 si j1 win et 2 si j2 win

def case_disponible(x:int, y:int)->bool:
    if board[y][x] == 0:
        return True
    else:
        return False

def afficher(x, y, joueur):
    if joueur == 1:
        screen.blit( croix, (x*100, y*100) )
    else:
        screen.blit( cercle, (x*100, y*100) )
    pygame.display.flip()

def is_win(board)->bool:
    """
    Prend en paramètre un plateau de jeu 3*3 de morpion
    Retourne True si un joueur a gagné ou qu'il y a égalité
    et False sinon
    """
    global winner
    #alignement horizontale
    for ligne in board:
        if ligne[0] == ligne[1] == ligne[2] and ligne[0] != 0:
            winner = ligne[0]
            return True
    #alignement verticale
    for colonne in range(3):
        if board[0][colonne] == board[1][colonne] == board[2][colonne] and board[0][colonne] != 0:
            winner = board[0][colonne]
            return True
    #alignement oblique_descendant
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != 0:
        winner = board[0][0]
        return True
    #alignement oblique montant
    if board[2][0] == board[1][1] == board[0][2] and board[2][0] != 0:
        winner = board[2][0]
        return True
    #égalité
    for ligne in board:
        for case in ligne:
            if case == 0:
                return False
    #Aucun alignement trouvé et plus de cases libre
    winner = 0
    return True










def minimax(boardBis, ordi_coup):
    if is_win(boardBis):
        if winner == 1:
            return 100
        elif winner == 2:
            return -100
        else:
            return 0

    if ordi_coup:
        meilleur_score = -100
        for i in range(3):
            for j in range(3):
                if boardBis[j][i] == 0:
                    boardBis[j][i] = 1
                    score = minimax(boardBis, False)
                    boardBis[j][i] = 0
                    if score > meilleur_score:
                        meilleur_score = score
        return meilleur_score

    else:#coup joueur
        meilleur_score = 100
        for i in range(3):
            for j in range(3):
                if boardBis[j][i] == 0:
                    boardBis[j][i] = 2
                    score = minimax(boardBis, True)
                    boardBis[j][i] = 0
                    if score < meilleur_score:
                        meilleur_score = score
        return meilleur_score

def coup_ordi(board):
    meilleur_score = -100
    meilleur_coup = (0, 0)
    boardBis = deepcopy(board)
    print(board)
    for i in range(3):
        for j in range(3):
            if boardBis[j][i] == 0:
                boardBis[j][i] = 1
                score = minimax(boardBis, False)
                boardBis[j][i] = 0
                if score > meilleur_score:
                    meilleur_score = score
                    meilleur_coup = (i, j)

    return meilleur_coup

























def jouer():
    """
    Fonction principal qui effectue les coups des joueurs
    """
    #good luck
    print("   __ _  ___   ___   __| | | |_   _  ___| | __")
    print("  / _` |/ _ \ / _ \ / _` | | | | | |/ __| |/ /")
    print(" | (_| | (_) | (_) | (_| | | | |_| | (__|   <")
    print("  \__, |\___/ \___/ \__,_| |_|\__,_|\___|_|\_\|")
    print("  |___/")

    #boucle jusqu'a ce qu'il y est un gagnant ou une égalité
    tour = 1
    joueur_tour = 0
    while not is_win(board):
        keys=pygame.key.get_pressed()
        events = pygame.event.get()
        joueur_tour = tour%2 + 1

        if joueur_tour == 1:
            x, y = coup_ordi(board)
            afficher(x, y, joueur_tour)
            board[y][x] = joueur_tour
            tour+=1

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                joueur_tour = tour%2 + 1
                x, y = x//100, y//100
                if case_disponible(x, y):
                    board[y][x] = joueur_tour
                    afficher(x, y, joueur_tour)
                    tour+=1
    time.sleep(1.5)
    pygame.quit()
    sys.exit()
jouer()
print(board)














