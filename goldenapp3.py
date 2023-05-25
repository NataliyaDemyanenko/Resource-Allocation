#!/usr/bin/env python3
import math
from math import *
import matplotlib.pyplot as plt
import networkx as nx
from cooperative_game import * 
import pickle
import string

def powerset(s):
     x = len(s)
     masks = [1 << i for i in range(x)]
     for i in range(1 << x):
         yield [ss for mask, ss in zip(masks, s) if i & mask]

def goldenapp():
     entries={}
     party_names={}
     polls={}

     entries = pickle.load( open( 'save.p', "rb" ) )

     s=0
     party_num=0
     for k in range(0, 15):
         try:
             polls[k]=float(entries[k+1,3])
             s=s+1
         except ValueError:
             party_num=s

    


     # Initialize parties and coalitions (labelled by letters)

     labels=['']*party_num
     colors=['']*party_num
     excluded=['']*party_num
     
     parties = list(string.ascii_uppercase)[0:party_num]

     for k in range(0, party_num):
         party_names[k]=str(entries[k+1,0])
         labels[k]=str(entries[k+1,1])
         colors[k]=str(entries[k+1,2])
     
     vn=0                     #votes needed for majority
     vn=int(entries[(0,1)]) 
     print(vn)
    

     label = dict(zip(parties,labels))  
     color = dict(zip(parties,colors))
     coalitions = powerset(parties)



     # Computing seats, Shapley values and all winning coalitions

     P=0
     for i in range(len(polls)):
         P += polls[i]
    
     print(P)

     quota=0
     quota= vn/P
     print(quota)
    
     # Initialize proportions of seats (precise and rounded)    

     s ={}
     sround = {}    
     pl = {} 
     i = 0  
     for p in parties:
         pl[p]=polls[i]
         s[p] = polls[i]/P
         sround[p]= round(float(s[p]*100),1)
         i+=1


     # Initialize proportions of seats (precise and rounded)    

     worth = {}                                           # Assign worth to coalitions
     for i in tuple(coalitions):
         sumsp=0
         for r in tuple(i):
             sumsp = sumsp +  s[r]
         worth[tuple(i)]=0
         if (sumsp > quota):
             worth[tuple(i)] = 1        
         #worth[tuple(i)] = ( copysign(1,(sumsp - 0.5)) + 1)/2
         #if ( copysign(1,(sumsp - 0.5)) + 1)==1:
             #worth[tuple(i)] = 0
         for j in tuple(powerset(i)):                       # Make game monotonic
             worth[tuple(i)]=max(worth[tuple(i)], worth[tuple(j)])

     #print('worth', worth)
     letter_game = CooperativeGame(worth)
     sh = letter_game.shapley_value()
     print( "{:<10} {:<10} {:<10} {:<10} {:<10}".format('Label', 'State', 'Votes', '%', 'Strength') )
     for k in parties:
         lb = label[k]
         num = sround[k]
         v = max(sh[k],0)
         print( "{:<10} {:<10} {:<10} {:<10} {:<10}".format(k, lb, round(float(pl[k]),2), num, v) )    

     letter_function = {}
     for k in worth.keys():            # Find all winning coalitions
         if worth[k] != 0:
             letter_function[k]=worth[k]


     # Find all minimal winning coalitions

     non_minimal_winning={}
     for k in letter_function.keys():
         for j in letter_function.keys():
             if (j!= k) and (set(k).intersection(set(j)) == set(k)):             
                 non_minimal_winning[j]=letter_function[j]

     minimal_winning={}
     for k in letter_function.keys():
         if not(k in non_minimal_winning.keys()):
             minimal_winning[k]=letter_function[k]


     # Find all stable coalitions
              
     chi = {}
     power = {}
     for k in minimal_winning.keys():
         S = 0
         for j in k:
             S += max(sh[j],0)
         chi[k] = minimal_winning[k]/S
         print(k,worth[k], chi[k])

