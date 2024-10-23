import argparse
import cassiopeia.data.CassiopeiaTree as castree
import cassiopeia.solver as solver
import numpy
import os
import pandas as pd
import treeswift
import sys



def get_character(character):
    df = pd.read_csv(character, sep=",", index_col = 0)
    df.index = df.index.astype(str)
    return df

def get_probs(mutation):
    df = pd.read_csv(mutation)

    prob_map = {}

    for index, row in df.iterrows():
        character=row['character']
        
        ## Note their example data use c0, c1,..., as character but we need (int, (int, float)) type.

        ## Also note in our simulate data we use 0,1,..., character 
        ## in bio data use c0, c1,...
        #character = int(character)
        
        state = int(row['state'])
        prob = float(row['probability'])

        if character not in prob_map:
            prob_map[character] = {}
        prob_map[character][state] = prob

    return prob_map


def run_NJ(tree):
    sol = solver.NeighborJoiningSolver(add_root = True)
    sol.solve(tree)
    return tree.get_newick()
    
def run_greedy(tree):
    sol = solver.VanillaGreedySolver()
    sol.solve(tree)
    return tree.get_newick()

def main(args):
    character = get_character(args.character_matrix)
    #probs = get_probs(args.mutation)
    #tree = castree(character_matrix=character, priors=probs)
    
    tree = castree(character_matrix=character)
    method = args.method
    res = ""
     
    
    if method == 0:
        res = run_NJ(tree)    
    elif method == 1:
        res = run_greedy(tree)
    
    with open(args.output, 'w') as wf:
        wf.write(res + "\n")



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--character_matrix", type = str, required=True)

    parser.add_argument("-m", "--mutation", type=str, required=True)

    parser.add_argument("-o", "--output", type=str,required=True)

    parser.add_argument("--method", type=int, required=True, help="0 : NJ, 1:greedy")

    main(parser.parse_args())
