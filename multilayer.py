import parse
import vectorize
import random
import numpy as np
import tensorflow as tf
import os.path

class Multilayer:
    """
    Defines the multilayer evaluation function by constructing and training a multilayer
    neural network.
    """
    def __init__(self, num_training_iterations, num_sample_positions, num_data_sets, learning_rate, vectorize_method):
        # parameters of training
        self.num_training_iterations = num_training_iterations
        self.num_sample_positions = num_sample_positions
        self.num_data_sets = num_data_sets
        self.learning_rate = learning_rate
        self.vectorize_method = vectorize_method

        # parameters of the network
        self.n_input = vectorize.get_vector_len(vectorize_method) # length of feature vector
        self.n_hidden_1 = 256 # 1st layer number of features
        self.n_hidden_2 = 256 # 2nd layer number of features
        self.n_classes = 3 # win, lose, draw

        # the weights and biases to be calculated
        self.W = {
            'h1': tf.Variable(tf.random_normal([self.n_input, self.n_hidden_1])),
            'h2': tf.Variable(tf.random_normal([self.n_hidden_1, self.n_hidden_2])),
            'out': tf.Variable(tf.random_normal([self.n_hidden_1, self.n_classes]))
        }
        self.b = {
            'b1': tf.Variable(tf.random_normal([self.n_hidden_1])),
            'b2': tf.Variable(tf.random_normal([self.n_hidden_2])),
            'out': tf.Variable(tf.random_normal([self.n_classes]))
        }

        self.model_path = './pickles/model_2_layer.ckpt'

    def multilayer_perceptron(self, x, weights, biases):
        """
        Constructs a multilayer neural network using TensorFlow
        """
        # Hidden layer with RELU activation
        layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
        layer_1 = tf.nn.relu(layer_1)
        # Hidden layer with RELU activation
        # layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
        # layer_2 = tf.nn.relu(layer_2)
        # Output layer with softmax activation
        out_layer = tf.nn.softmax(tf.matmul(layer_2, weights['out']) + biases['out'])
        return out_layer

    def train(self):
        """
        Trains a neural network using labelled training data and gradient descent.
        The output layer is three values corresponding to the likelihoods of
        losing, drawing, or winning.
        """
        if not os.path.isfile(self.model_path + '.index'):
            # get vectorized, labeled training data
            all_training_boards = parse.pgn_to_boards(self.num_data_sets, labels=True, vectorize_method=self.vectorize_method)

            # confirm feature length
            assert self.n_input == len(all_training_boards[0][0])

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
            x = tf.placeholder(tf.float32, [None, self.n_input])
            y_ = tf.placeholder(tf.float32, shape=[None, self.n_classes])

            # Construct model
            pred = self.multilayer_perceptron(x, self.W, self.b)

            # Define loss and optimizer
            cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(pred, y_))
            train_step = tf.train.GradientDescentOptimizer(learning_rate=self.learning_rate).minimize(cross_entropy)

        saver = tf.train.Saver()

        with tf.Session() as sess:
            if os.path.isfile(self.model_path + '.index'):
                saver.restore(sess, self.model_path)
                print 'Model restored'
            else:
                print 'Training model - this could take a while...'
                # initialize variables
                sess.run(tf.global_variables_initializer())

                # run gradient descent number of times specified, using different randomly sampled
                # subset of boards each time
                for training_iteration in range(self.num_training_iterations):
                    training_boards = random.sample(all_training_boards, self.num_sample_positions)
                    x_train = [t[0] for t in training_boards]
                    y_train = np.array([t[1] for t in training_boards]).reshape(self.num_sample_positions, 3)
                    train_step.run(feed_dict={x: x_train, y_: y_train})

                save_path = saver.save(sess, self.model_path)
                print 'Model saved in file ' + save_path
