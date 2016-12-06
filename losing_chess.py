import chess_agents
import evaluation
import vectorize
import play

import sys

# maps from arguments to possible agents and evaluators
agent_choices = {'human': chess_agents.HumanAgent, 'random': chess_agents.RandomAgent, 
                 'minimax': chess_agents.MinimaxAgent, 'alpha_beta': chess_agents.AlphaBetaAgent, 
                 'expectimax': chess_agents.ExpectimaxAgent}

eval_choices = {'weighted_count': evaluation.WeightedPieceCount, 'anti_pawn': evaluation.AntiPawn, 
                'weighted_count_captures': evaluation.WeightedPieceCountWCaptures, 'softmax': evaluation.SoftmaxEval, 
                'multilayer': evaluation.MultilayerEval, 'TD': evaluation.TDTrainEval, 'none': None}

# parameters for training the learning methods
td_parameters = 10, 10, 1, 1, 0.7, 12, False, vectorize.piece_count_vector
softmax_parameters = 10, 10, 1, 1, vectorize.piece_count_vector
multilayer_parameters = 10, 10, 1, 1, vectorize.piece_count_vector

# validate and sort input 
args = sys.argv[1:]
if len(args) != 6:
    print 'Usage: python losing_chess.py agent_1 eval_func_1 depth_1 agent_2 eval_func_2 depth_2'
    sys.exit()

try:
    agent_1 = agent_choices[args[0]]
    eval_func_1 = eval_choices[args[1]]
    depth_1 = int(args[2])

    agent_2 = agent_choices[args[3]]
    eval_func_2 = eval_choices[args[4]]
    depth_2 = int(args[5])
except KeyError:
    print 'Invalid option'
    sys.exit()

# play the game
play.play_game(agent_1, eval_func_1, depth_1, agent_2, eval_func_2, depth_2, td_parameters, softmax_parameters, multilayer_parameters)