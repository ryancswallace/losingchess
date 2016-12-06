import losing_board
import game
import evaluation
import chess
import softmax
import multilayer
import td_lambda
import time

def play_game(agent_1, eval_func_1, depth_1, agent_2, eval_func_2, depth_2, td_parameters, softmax_parameters, multilayer_parameters, board=losing_board.LosingBoard(no_kings=False)):
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

    # construct final agents, and game
    a1 = agent_1(color=chess.WHITE, eval_func=evaluator_1, depth=depth_1, ant_eval_func=evaluator_2)
    a2 = agent_2(color=chess.BLACK, eval_func=evaluator_2, depth=depth_2, ant_eval_func=evaluator_1)
 
    game_to_play = game.Game(board, a1, a2)

    # begin
    start = time.time()
    game_to_play.play()
    end = time.time()
    print(end - start)

