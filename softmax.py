import parse
import random
import numpy as np

import tensorflow as tf

class Softmax:
    def __init__(self, num_training_iterations, num_sample_positions, learning_rate):
        # parameters of training
        self.num_training_iterations = num_training_iterations
        self.num_sample_positions = num_sample_positions
        self.learning_rate = learning_rate

        # the weight matrix and bias vector to be calculated
        self.W = None
        self.b = None

    def train(self, print_accuracy=False):
        # get vectorized, labeled training data
        all_training_boards = parse.pgn_to_boards('data/all_losing.pgn', labels=True, vectorized=True)
        num_boards = len(all_training_boards)
        self.vector_len = len(all_training_boards[0][0])

        # encode label as one hot vector
        for i, (board_vector, label) in enumerate(all_training_boards):
            one_hot_vector = []
            if label == 0:
                one_hot_vector = [1,0,0]
            elif label == 0.5:
                one_hot_vector = [0,1,0]
            elif label == 1:
                one_hot_vector = [0,0,1]
            else:
                raise Exception('Invalid label.')

            all_training_boards[i] = (all_training_boards[i][0], one_hot_vector)

        # holders for training board vectors, and true labels
        x = tf.placeholder(tf.float32, [None, self.vector_len])
        y_ = tf.placeholder(tf.float32, shape=[None, 3])

        # the weight matrix and bias vector
        W = tf.Variable(tf.zeros([self.vector_len, 3]))
        b = tf.Variable(tf.zeros([3]))

        with tf.Session() as sess:
            # initialize variables
            sess.run(tf.global_variables_initializer())

            # softmax regression to predict y; cross entropy used as error function
            y = tf.nn.softmax(tf.matmul(x, W) + b)
            cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y, y_))

            # train using gradient descent
            train_step = tf.train.GradientDescentOptimizer(self.learning_rate).minimize(cross_entropy)

            # run gradient descent number of times specified, using different randomly sampled
            # subset of boards each time
            for training_iteration in range(self.num_training_iterations):
                training_boards = random.sample(all_training_boards, self.num_sample_positions)
                x_train = [t[0] for t in training_boards]
                y_train = np.array([t[1] for t in training_boards]).reshape(self.num_sample_positions, 3)
                train_step.run(feed_dict={x: x_train, y_: y_train})

                if print_accuracy:
                    # evaluate accuracy on whole training set (not reliable because train set = test set)
                    correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
                    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
                    x_all = [t[0] for t in all_training_boards]
                    y_all = np.array([t[1] for t in all_training_boards]).reshape(num_boards, 3)
                    print(sess.run(accuracy, feed_dict={x: x_all, y_: y_all}))

            # convert evaluated tensors to np arrays
            self.W = W.eval()
            self.b = b.eval()

    def eval(self, board_vector):
        # check that model has been trained
        if self.W is None or self.b is None:
            raise Exception('Train softmax first.')

        # tensor for board_vector
        x = tf.placeholder(tf.float32, [1, len(board_vector)])

        # the weight matrix and bias vector
        W = tf.constant(self.W, dtype=tf.float32)
        b = tf.constant(self.b, dtype=tf.float32)

        with tf.Session() as sess:
            # initialize variables
            sess.run(tf.global_variables_initializer())

            # define model with weights and biases calculated
            y = tf.nn.softmax(tf.matmul(x, W) + b)

            # predict new board
            predict = tf.argmax(y,1)
            x_np = np.array(board_vector).reshape(1,len(board_vector))
            pred = sess.run(predict, feed_dict={x: x_np})[0]
            return pred

