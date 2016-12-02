import chess
import random

class Agent:
    def __init__(self, eval_func, color=chess.WHITE, depth='1'):
        self.color = color
        self.eval_func = eval_func
        self.depth = int(depth) - 1
        if self.depth < 0:
            raise Exception("Depth must be >= 0")

    def get_move(self, game_state):
        raise Exception("Undefined!")


class RandomAgent(Agent):
    def get_move(self, game_state):
        moves = game_state.get_legal_moves()
        if len(moves) == 0:
            return None
        else:
            move = random.sample(moves, 1)[0]
            return move


class AlphaBetaAgent(Agent):
    def get_move(self, game_state, return_value=False):
        """
        Return minimax move using self.depth, self.eval_func, and alpha-beta pruning.
        """
        moves = game_state.get_legal_moves()
        if len(moves) == 0:
            return None

        values = {}
        alpha = -99999
        for move in moves:
            values[move] = self._alpha_beta_value(move, game_state, -99999, 99999, 0, self.color)
            alpha = max(alpha, values[move])

        # return action with max utility,
        # random action if there's a tie
        best_val = max(values.values())
        best_actions = []
        for k, v in values.iteritems():
            if v == best_val:
                best_actions.append(k)
        best_action = random.sample(best_actions, 1)[0]
        if return_value:
            return (best_action, best_val)
        else:
            return best_action


    def _alpha_beta_value(self, move, game_state, alpha, beta, depth, color):
        """
        Helper function for performing alpha-beta pruning.
        """
        # get next game state
        next_state = game_state.generate_successor(move)

        # has agent won?
        if next_state.is_game_over():
            return 99999

        # does agent move next?
        next_color = not color

        # has max depth been reached?
        if depth == self.depth:
            return self.eval_func(next_state, color)

        # get information about next state
        next_moves = next_state.get_legal_moves()

        # if this agent is to move
        if next_color == self.color: 

            # increment depth
            depth += 1

            # if we've reached a terminal state
            # update alpha and return terminal value
            if next_moves == []:
                term_val = self.eval_func(next_state, next_color)
                alpha = max(alpha, term_val)
                return term_val

            # find next action with max utility
            v = -99999
            for mv in next_moves:
                mvValue = self._alpha_beta_value(mv, next_state, alpha, beta, depth, next_color)
                v = max(v, mvValue)
                # prune if value is great enough
            if v > beta:
                return v
            alpha = max(alpha, v)
            return v

        # if opponent is to move
        else:
            # if we've reached a terminal state
            # return terminal value without updating alpha/beta
            if next_moves == []:
                term_val = self.eval_func(next_state, next_color)
                return term_val

            # find next action with min utility
            v = 99999
            for mv in next_moves:
                mvValue = self._alpha_beta_value(mv, next_state, alpha, beta, depth, next_color)
                v = min(v, mvValue)
                #prune if value is small enough
                if v < alpha:
                    return v
                beta = min(beta, v)
            return v

