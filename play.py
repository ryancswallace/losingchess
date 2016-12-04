import losing_board
import game
import chess_agents
import evaluation
import vectorize
import chess
import softmax
import multilayer
import td_lambda

import sys

# maps from arguments to possible agents and evaluators
agent_choices = {'human': chess_agents.HumanAgent, 'random': chess_agents.RandomAgent, 'alpha_beta': chess_agents.AlphaBetaAgent}

eval_choices = {'weighted_count': evaluation.WeightedPieceCount, 'anti_pawn': evaluation.AntiPawn, 
                'weighted_count_captures': evaluation.WeightedPieceCountWCaptures, 'softmax': evaluation.SoftmaxEval, 
                'multilayer': evaluation.MultilayerEval, 'TD': evaluation.TDTrainEval, 'none': None}

# default parameters for training the learning methods
td_parameters = 10, 10, 1, 1, 0.7, 12, False, vectorize.piece_count_vector
softmax_parameters = 10, 10, 1, 1, vectorize.piece_count_vector
multilayer_parameters = 10, 10, 1, 1, vectorize.piece_count_vector

# validate and sort input 
args = sys.argv[1:]
if len(args) != 6:
    print 'Usage: python play.py agent_1 eval_func_1 depth_1 agent_2 eval_func_2 depth_2'
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

# agent 1 evaluator
if eval_func_1 == evaluation.SoftmaxEval:
    model = softmax.Softmax(*softmax_parameters)
    model.train()
    evaluator_1 = evaluation.SoftmaxEval(model).evaluate

elif eval_func_1 == evaluation.MultilayerEval:
    model = multilayer.Mutlilayer(*multilayer_parameters)
    model.train()
    evaluator_1 = evaluation.MultilayerEval(model).evaluate

elif eval_func_1 == evaluation.TDTrainEval:
    model = td_lambda.TDLeafLambda(*td_parameters)
    model.train()
    evaluator_1 = evaluation.TDTrainEval(model).evaluate

elif eval_func_1 == None:
    evaluator_1 = None

else:
    evaluator_1 = eval_func_1().evaluate

# agent 2 evaluator
if eval_func_2 == evaluation.SoftmaxEval:
    model = softmax.Softmax(*softmax_parameters)
    model.train()
    evaluator_2 = evaluation.SoftmaxEval(model).evaluate

elif eval_func_2 == evaluation.MultilayerEval:
    model = multilayer.Mutlilayer(*multilayer_parameters)
    model.train()
    evaluator_2 = evaluation.MultilayerEval(model).evaluate

elif eval_func_2 == evaluation.TDTrainEval:
    model = td_lambda.TDLeafLambda(*td_parameters)
    model.train()
    evaluator_2 = evaluation.TDTrainEval(model).evaluate

elif eval_func_2 == None:
    evaluator_2 = None

else:
    evaluator_2 = eval_func_2().evaluate

# construct final agents, board, and game
a1 = agent_1(color=chess.WHITE, eval_func=evaluator_1, depth=depth_1)
a2 = agent_2(color=chess.BLACK, eval_func=evaluator_2, depth=depth_2)

board = losing_board.LosingBoard(no_kings=False)
game = game.Game(board, a1, a2)

# begin
game.play()

