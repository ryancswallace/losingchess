import game
import chess
import chess_agents
import evaluation
import losing_board
import pickle
import multilayer
import vectorize
import sys
import StringIO
import random
from copy import deepcopy
from scipy.stats import binom

class StatsGenerator:

    def __init__(self, sig_level, max_iter=30, null_p=.5, stop_at_significance=False):

        self.sig_level = sig_level
        self.null_p = null_p
        self.max_iter = max_iter
        self.stop_at_significance = stop_at_significance

    def compare_agents(self, a1, a2, board, verbose=False):

        a1_victory_history = []
        a1_color_history = []

        order = [a1,a2]

        for i in range(self.max_iter):
            tmp_board = deepcopy(board)
            winning_agent = None
            if i % 2 == 0:
                g = game.Game(tmp_board, a1, a2, get_stats=True)
                winning_agent = g.play(max_turns=200)
            else:
                g = game.Game(tmp_board, a2, a1, get_stats=True)
                winning_agent = g.play(max_turns=200)
            if winning_agent == chess.WHITE:
                a1_victory_history.append(True)
            else:
                a1_victory_history.append(False)

            # check if significance has been reached, excluding draws
            no_draws = [g for g in a1_victory_history if g is not None]
            n = len(no_draws)
            x = sum(no_draws)
            p_val = binom.cdf(x, n, self.null_p)
            if self.stop_at_significance:
                if p_val < self.sig_level/2 or p_val > 1 - self.sig_level/2:
                    if sum(no_draws) < len(no_draws)/2:
                        self.print_results(a2, a1, no_draws, p_val)
                        return a2, [not a for a in a1_victory_history], p_val
                    else:
                        self.print_results(a1, a2, no_draws, p_val)
                        return a1, a1_victory_history, p_val

        self.print_results(a1, a2, a1_victory_history, p_val)
        return a1, a1_victory_history, p_val

    def print_results(self, win_agent, lose_agent, history, p):

        if p > .5:
            p = 1 - p

        print
        print win_agent.__class__.__name__ + " with evaluator '" + str(win_agent.eval_func.im_class)[11:] + "' and depth " + str(win_agent.depth)
        print "wins " + str(sum(history)) + " out of " + str(len(history)) + " games against"
        print lose_agent.__class__.__name__ + " with evaluator '" + str(lose_agent.eval_func.im_class)[11:] + "' and depth " + str(lose_agent.depth)
        print "p-value: " + str(p)
        print
        if p > self.sig_level:
            print "No significant difference found."

        print
        return


if __name__ == "__main__":

    anti_pawn = evaluation.AntiPawn()
    counter1 = evaluation.WeightedPieceCount()

    multilayer_model = multilayer.Multilayer(1000, 10, 3, 1, vectorize.piece_count_vector)
    multilayer_model.train()
    multilayer_eval = evaluation.MultilayerEval(multilayer_model)

    a1 = chess_agents.AlphaBetaAgent(color=chess.WHITE, eval_func=multilayer_eval.evaluate, depth=1, ant_eval_func=counter1.evaluate)
    a2 = chess_agents.RandomAgent(color=chess.BLACK, eval_func=counter1.evaluate, depth=1, ant_eval_func=multilayer_eval.evaluate)
    board = losing_board.LosingBoard(no_kings=False)

    s = StatsGenerator(.05, max_iter=30)
    out = s.compare_agents(a1, a2, board)

