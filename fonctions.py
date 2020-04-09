#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 18:33:26 2019

@author: Bilal and Antoine
"""

# =============================================================================
# PRÉLIMINAIRE
# =============================================================================
 
from render_connect4 import *
from random import randrange
# =============================================================================
# 2 Mise en place du jeu Puissance 4
# =============================================================================

# 2.1  Représentation du plateau de jeu, initialisation et affichage

def grid(nr, nc):
    
    """ Create a grid with a number of row and columns entered as parameters.

        :param nr: (int) any integer, it is the number of rows
        :param nc: (int) any integer, it is the number of columns
        :return: (list) the grid of Connect4
    """
    
    return [[0 for i in range(nc)] for i in range(nr)]

g = grid(6,7)

def nr(g):
    """ Return the number of rows of the grid.
        
        :param g: (list) the grid of Connect4
        :return: (int) number of rows
    """
    
    return len(g)

def nc(g):
    """ Return the number of column of the grid.
        
        :param g: (list) the grid of Connect4
        :return: (int) number of columns
    """
    
    return len(g[0])

def display_grid(g):
    """ Print a grid corresponding at our grid of Connect4.

        :param g: (list) the grid of Connect4
        
    """
    
    char = ['-','O','X']
    
    for r in g:
        
        ligne = ''
        
        for elt in r:
            
            ligne += char[elt]
            
        print(ligne) 
        
    print("="*nc(g))
    for i in range(nc(g)):
        print(i, end = '')
    print("\n")
        
        
# 2.2  Jouer un coup
        
def is_valid(c,g):
    """ Says if it is true that the playturn is valid.

    :param c: (int) the column s number where the player want to play
    :param g: (list) the grid of Connect4
    :return: (bool) True if the playturn is valid, else False
    """
    
    return c < nc(g) and c >= 0 and g[0][c] == 0

def ask_player(g):
    """ Ask player which column he wants to play.

        :param g: (list) the grid of Connect4
        :return: (int) the column s number where the player played
    """
    
    ask = input('Chose a column :) \n\t ')
    good = False
    
    while not good:
        cpt = 0
        value = ''
        for i in ask.split(' '):
            if i != '':
                cpt += 1
                value = i
        if (cpt != 1) or (value != "0" and value != "1" and value != "2" and value != "3" and value != "4" and value != "5" and value != "6") or (not is_valid(int(value), g)):
            ask = input('Hey could you please choose a valid column !\n\t')
        else:
            good = True
        
    return int(value)

    
def play_turn(c, p, g):
    """ Modify the grid when a playturn is played.

        :param c: (int) the column where the player played
        :param p: (int) the value corresponding of the coin s player
        :param g: (list) the grid of Connect4
        :return: (tuple) a tuple, containing the grid changed and the row where the playturn has been played
    """
    
    r= 0
    for i in range(nr(g)):
        if g[i][c] != 0:
            r += 1
    g[nr(g)-r-1][c] = p
    return (g, nr(g)-r-1)


def coup(player, g, p):
    """ Make action depending of the player.

        :param player: (str) the player
        :param g: (list) the grid of Connect4
        :param p: (int) the value corresponding of the coin s player
        :return: (function) the function which allows the player to play
    """
    
    if player == 'h':
        
        return ask_player(g)
        
    elif player == 'ia1':
        
        return ia_aleat(g)
    
    elif player == 'ia2':
        
        return ia_win(g, p)
    
    elif player == 'ia3':
        
        return ia_win2(g,p)
    
    elif player == 'ia4':
        
        return move_ia(g ,2, p)
        
        
def play(player1='h', player2='ia3'):
    """ Start the game. It s the main function.

        :param g: (list) the grid of Connect4, it s initialised with a grid with 6 rows and 7 columns
        :param player1: (str) the first player
        :param player2: (str) the second player
    """
    g = grid(6,7)
        
    
    i = 0
    draw_connect4(g)
    player = [player1, player2]
    
    while any(g[0][j] == 0 for j in range(nc(g))):
        
        p = i%2 + 1
        c = coup(player[p-1], g, p)
        (g,r) = play_turn(c, p, g)
        i += 1
#        display_grid(g)
        draw_connect4(g)
        
        if is_win(g, r, c, p):
            
            print("Victoire de joueur{}".format(p))
            break
    if all(g[0][j] != 0 for j in range(nc(g))) and  not is_win(g, r, c, p):
        print('DRAW!!')          

wait_quit()
        

# 2.5 Coup gagnant
        
        
def lc_horizontal(coords, g):
    """ Returns the horizontal combination of seven coordinates centered on the coordinates entered as parameter

        :param coords: (tuple) coordinates of a coin
        :param g: (list) the grid of Connect4
        :return: (list) list of the possibles combinations of four coordinates which are horizontally around the coordinates
    """
    
    c = coords[1]
    r = coords[0]
    return [(r, c+i) for i in range(-3, 4) if c+i >= 0 and c+i < nc(g)]  

def lc_vertical(coords, g):
    """ Returns the vertical combination of seven coordinates centered on the coordinates entered as parameter

        :param coords: (tuple) coordinates of a coin
        :param g: (list) the grid of Connect4
        :return: (list) list of the possibles combinations of four coordinates which are horizontally around the coordinates
    """
    
    c = coords[1]
    r = coords[0]

    return [(r+i, c) for i in range(-3, 4) if r+i >= 0 and r+i < nr(g)]  

def lc_increasing_diag(coords, g):
    """ Returns the increasing diagonal combination of seven coordinates centered on the coordinates entered as parameter

        :param coords: (tuple) coordinates of a coin
        :param g: (list) the grid of Connect4
        :return: (list) list of the possibles combinations of four coordinates which are horizontally around the coordinates
    """
    
    c = coords[1]
    r = coords[0]

    return [(r+i, c-i) for i in range(-3, 4) if c-i < nc(g) and c-i >= 0 and r+i >= 0 and r+i < nr(g)]  

def lc_decreasing_diag(coords, g):
    """ Returns the decreasing diagonal combination of seven coordinates centered on the coordinates entered as parameter

        :param coords: (tuple) coordinates of a coin
        :param g: (list) the grid of Connect4
        :return: (list) list of the possibles combinations of four coordinates which are horizontally around the coordinates
    """
    
    c = coords[1]
    r = coords[0]

    return [(r-i, c-i) for i in range(-3, 4) if c-i >= 0 and c-i < nc(g) and r-i >= 0 and r-i < nr(g)]
                    
    
def is_align4(g, lc, p):
    """ Says if it is true that there are 4 coins aligned.

        :param g: (list) the grid of Connect4
        :param lc: (list) list containing 4 coordinates
        :param p: (int) the value corresponding of the coin of the player who is playing the playturn
        :return: (bool) True if there are 4 coins aligned, else False
    """
    
    if len(lc) >= 4:

        for i in range(len(lc)-3):

            k = 0
            
            for elt in lc[i: i+4:]:

                if g[elt[0]][elt[1]] == p:
                    
                    k += 1
                
            if k == 4:
            
                return True
    
    return False

def is_win(g, r, c, p):
    """ Says if a playturn makes the player wins or not.

        :param g: (list) the grid of Connect4
        :param r: (int) the row where the coin will lay
        :param c: (int) the column where the coin will lay
        :param p: (int) the value corresponding of the coin s player
        :return: (bool) True if there 4 coins aligned, False else
    """
    
    lcs = [lc_horizontal((r,c), g), lc_vertical((r,c), g), lc_increasing_diag((r,c), g), lc_decreasing_diag((r,c), g)]
    return any([is_align4(g, lcs[i], p) for i in range(4)])

    
# =============================================================================
# 3 Faire jouer l'ordinateur
# =============================================================================
    
# 3.1 Jeu aléatoire
    
def ia_aleat(g):
    """ Makes the ia plays randomly.

        :param g: (list) the grid of Connect4
        :return: (int) the column where the ia is going to play, chosen randomly between the valid columns
    """
    
    liste_coups = [i for i in range(nc(g)) if is_valid(i, g)]
    
    return liste_coups[randrange(len(liste_coups))]

# 3.2 Analyser tous les coups possibles
    
# -- 3.2.1 Analyse de la victoire

def unmove(g, c):
    """ Remove a coins from a specific column.

        :param g: (list) the grid of Connect4
        :param c: (int) the column s number of the column where the coin is removed
    """
    
    for i in range(len(g)):
        
        if g[i][c] != 0:
            
            g[i][c] = 0
            
            break
            
            
def ia_win(g, p):
    """ Makes the ia checks if his playturn could be winning. If there a possibility to win, returns the column which makes him wins.
        Else, return a random column.

        :param g: (list) the grid of Connect4
        :param p: (int) the value corresponding of the coin s player
        :return: (int) the number of a column, corresponding to a winning one or to a random one, it s depending on the ia s luck
    """
    
    
    copy = list.copy(g)
    
    for i in range(nc(copy)):
        
        (copy, r) = play_turn(i, p, copy)
        
        if is_win(g, r, i, p):
            
            unmove(copy, i)
            return i
        
        else:
            
            unmove(copy, i)
        
    return ia_aleat(g)

# -- 3.2.2 Evaluation de la grille
    

def get_Player(lc, g):
    """ Converses a list of coordinates into a list of 0, 1 or 2, depending on who played on each coordinates.
    
    :param lc: (list) a list of coordinates
    :param g: (list) the grid of Connect4
    :return: (list) a list of 0, 1 or 2, depending on who played on each coordinates
    """
    return [g[c[0]][c[1]] for c in lc]
    


def Score(fourtuple, p):
    """ Calculates the score of a combination of four coordinates.

        :param fourtuple: (list) a list of 0, 1 or 2, depending on who played on each coordinates
        :param p: (int) the value corresponding of the coin s player
        :return: (int) the score of the combination
    """
    
    Player = 0
    Enemy = 0
    enemyScore = [-1,-10,-5000,-10000000]
    playerScore = [1,10,1000,100000]
    
    for i in range(len(fourtuple)):
        
        if fourtuple[i] == p:
            Player += 1
            
        elif fourtuple[i] != 0 and fourtuple[i] != p:
            Enemy += 1
    if Player > 0 and Enemy > 0 or Player == 0 and Enemy == 0:
        return 0
    elif Player != 0 and Enemy == 0:
        return playerScore[Player-1]
    elif Player == 0 and Enemy != 0:
        return enemyScore[Enemy-1]
    

def lc_horizontal2(coords, g):
    """ Returns the horizontal combination of the coordinate selected and the three following horizontally.

        :param coords: (tuple) coordinates of a coin
        :param g: (list) the grid of Connect4
        :return: (list) list of the possibles combinations of four coordinates which are horizontally around the coordinates
    """
    
    c = coords[1]
    r = coords[0]
    return [(r, c+i) for i in range(0, 4) if c+i >= 0 and c+i < nc(g)]  
    
def lc_vertical2(coords, g):
    """ Returns the vertical combination of of the coordinate selected and the three following vertically.

        :param coords: (tuple) coordinates of a coin
        :param g: (list) the grid of Connect4
        :return: (list) list of the possibles combinations of four coordinates which are horizontally around the coordinates
    """
    
    c = coords[1]
    r = coords[0]

    return [(r+i, c) for i in range(0, 4) if r+i >= 0 and r+i < nr(g)]

def lc_increasing_diag2(coords, g):
    """ Returns the increasing diagonal combination of the coordinate selected and the three following.

        :param coords: (tuple) coordinates of a coin
        :param g: (list) the grid of Connect4
        :return: (list) list of the possibles combinations of four coordinates which are horizontally around the coordinates
    """
    
    c = coords[1]
    r = coords[0]

    return [(r+i, c-i) for i in range(0, 4) if c-i < nc(g) and c-i >= 0 and r+i >= 0 and r+i < nr(g)]  

def lc_decreasing_diag2(coords, g):
    """ Returns the decreasing diagonal combination of the coordinate selected and the three following.

        :param coords: (tuple) coordinates of a coin
        :param g: (list) the grid of Connect4
        :return: (list) list of the possibles combinations of four coordinates which are horizontally around the coordinates
    """
    
    c = coords[1]
    r = coords[0]

    return [(r-i, c-i) for i in range(-3, 1) if c-i >= 0 and c-i < nc(g) and r-i >= 0 and r-i < nr(g)]



def computeScore(coords, g, p):
    """ Calculate the Best Score around a especially coodinate selected.

        :param coords: (tuple) coordinates of a coin
        :param g: (list) the grid of Connect4
        :param p: (int) the player
        :return: (int) the score of a coordinate
    """
    lcs = [lc_horizontal2(coords, g), lc_vertical2(coords, g), lc_increasing_diag2(coords, g), lc_decreasing_diag2(coords, g)]
    Scores = 0
    pions = [get_Player(lc,g) for lc in lcs]
    for elt in pions:
        Scores += Score(elt,p)
    return Scores

def computeGrid(g,p):
    """ Computes the Grid's score 
    
        :param g: (list) the grid of Connect4
        :param p: (int) the player
        :return: (int) the grid scocre

    """
    grid_score = 0
    
    for i in range(nr(g)):
        for j in range(nc(g)):
            grid_score += computeScore((i,j), g, p)
    
    return grid_score
        
    
def OptimusColumn(g,p):
    """ Returns the column which give us the best play.
    
        :param g: (list) the grid of Connect4
        :param p: (int) the player
        :return: (int) the best column
    """
    listScore = []
    copy = list.copy(g)
    for c in range(nc(copy)):
        if is_valid(c, copy):
            (copy, r) = play_turn(c,p, copy)
            listScore.append(computeGrid(copy, p))
            unmove(copy, c)
        else:
            listScore.append(-100000000000000000000000000000000000000000000000)
            
    return listScore.index(max(listScore))        

 
def ia_win2(g, p):
    """ Makes the ia checks if his playturn could be winning. If there a possibility to win, returns the column which makes him wins.
        Else, return a random column.

        :param g: (list) the grid of Connect4
        :param p: (int) the value corresponding of the coin s player
        :return: (int) the number of a column, corresponding to the best playturn
    """
    
    
    copy = list.copy(g)
    
    for i in range(nc(copy)):
        
        (copy, r) = play_turn(i, p, copy)
        
        if is_win(g, r, i, p):
            
            unmove(copy, i)
            return i
        
        else:
            
            unmove(copy, i)
        
    return OptimusColumn(g,p)

# =============================================================================
# 4 Analyser plusieurs tours de jeu à l'avance
# =============================================================================

# 4.1  Enumération de toutes les grilles

def move_ia(g ,nb_round, player):
    """ Simulates nb_round turnplays to helping the ia to take decisions.

        :param g: (list) the grid of Connect4
        :param nb_round: (int) the number of turnplays we want to simulate
        :param player: (int) the value corresponding of the coin s player
        :return: none
    """
    
    end = False
    list_move = [[0,-10000000000000000000,-1000000000000000000]]
    
    player_round = player
    backtrack = False
    next_move = False
    
    while not(end):
        if len(list_move) == 0:
            end = True
            
        elif next_move:
            next_move = False
            if Score > list_move[-1][2]:
                list_move[-1][2] = Score
                best_column = list_move[-1][0]
            unmove(g, list_move[-1][0])
            list_move[-1][0] += 1
                        
        elif backtrack:
            backtrack = False
            list_move.pop()
            next_move = True
            player_round = player_round%2 + 1
                        
        elif list_move[-1][0] == nc(g):
            backtrack = True
            
        elif is_valid(list_move[-1][0],g) == False:
            list_move[-1][0] += 1
            
        else:
            column = list_move[-1][0]
            (g,row) = play_turn(column, player_round, g)
            
                        
            if is_win(g, row, column, player_round):
                Score = computeGrid(g,player_round)
                next_move = True
            
            elif len(list_move) == nb_round:
                Score = computeGrid(g,player_round)
                next_move = True
            else:
                list_move.append([0,-10000000000000000000,-1000000000000000000])
                player_round = player_round%2 + 1
    return best_column
    
    
if __name__=="__main__":
    play('h','ia3')