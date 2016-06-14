import tensorflow as tf
import os

class CriticNN():
    
    def __init__(self, input_size=274, hidden_size=100, alpha=0.1, discount=0.9, learn_rate=0.1, step=100, model_dir='model/', model_name='model'):
        self._alpha = alpha
        self._discount = discount
        self._learn_rate = learn_rate
        self._input_size = input_size
        self._hidden_size = hidden_size
        self._step = step
        self._model_path = model_dir + model_name + '.ckpt'
        if not os.path.isdir(model_dir):
            os.system('mkdir ' + model_dir)

    # build one hidden layer graph
    def inference(self, input_layer):
        with tf.name_scope('hidden'):
            weights = tf.Variable(tf.zeros([self._input_size, self._hidden_size]), name='weights')
            hidden = tf.sigmoid(tf.matmul(input_layer, weights))

        with tf.name_scope('output'):
            weights = tf.Variable(tf.zeros([self._hidden_size, 1]), name='weights')
            logits = tf.sigmoid(tf.matmul(hidden, weights))

        return logits

    def loss(self, reward_next, v_current, v_next):
        # e = alpha*(r(t+1) + gamma*v(t+1) - v(t))
        e = tf.mul(self._alpha, tf.sub(tf.add(reward_next, tf.mul(self._discount, v_next)), v_current))
        # E = 1/2 * e^2
        E = tf.mul(0.5, tf.pow(e, 2))
        return E

    # should be put after variables are defined
    def session(self):
        saver = tf.train.Saver()
        sess = tf.Session()
        
        if os.path.exists(self._model_path):
            saver.restore(sess, self._model_path)
        else:
            init = tf.initialize_all_variables()
            sess.run(init)

        return sess

    def placeholders(self):
        input_placeholder = tf.placeholder(tf.float32, shape=[None, self._input_size])
        reward_next_placeholder = tf.placeholder(tf.float32, shape=[None, 1])
        v_next_placeholder = tf.placeholder(tf.float32, shape=[None, 1])

        return input_placeholder, reward_next_placeholder, v_next_placeholder

    def train_op(self, input_placeholder, reward_next_placeholder, v_next_placeholder):
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=self._learn_rate)
        logits = self.inference(input_placeholder)
        loss = self.loss(reward_next_placeholder, logits, v_next_placeholder)
        train_op = optimizer.minimize(loss)

        return train_op

    def run_value(self, x):
        with tf.Graph().as_default():
            input_placeholder =  tf.placeholder(tf.float32, shape=[None, self._input_size])
            logits = self.inference(input_placeholder)
            sess = self.session()
            feed_dict = {input_placeholder: x}
            value = sess.run(logits, feed_dict=feed_dict)

        return value

    def run_learning(self, reward_next, x_current, x_next):
        v_current = self.run_value(x_current)
        v_next = self.run_value(x_next)

        with tf.Graph().as_default():
            input_placeholder, reward_next_placeholder, v_next_placeholder = self.placeholders()
            train_op = self.train_op(input_placeholder, reward_next_placeholder, v_next_placeholder)
            
            feed_dict = {reward_next_placeholder: reward_next,
                        v_next_placeholder: v_next, 
                        input_placeholder: x_current}

            sess = self.session()
            for _ in range(self._step):
                sess.run(train_op, feed_dict=feed_dict)

            saver = tf.train.Saver()
            saver.save(sess, self._model_path)

        return v_current, v_next

def test():
    CNN = CriticNN(3)
    print(CNN.run_value([[1., 0., 0.], [0., 0., 1.], [1., 1., 0.], [2., 1., 0.]]))
    print("----------------")
    print(CNN.run_learning([[1.]], [[1., 0., 0.]], [[0., 0., 1.]]))
    print(CNN.run_value([[1., 0., 0.], [0., 0., 1.], [1., 1., 0.], [2., 1., 0.]]))
    print("----------------")
    print(CNN.run_learning([[0.]], [[1., 0., 0.]], [[1., 1., 0.]]))
    print(CNN.run_value([[1., 0., 0.], [0., 0., 1.], [1., 1., 0.], [2., 1., 0.]]))
    print("----------------")
    print(CNN.run_learning([[0.]], [[1., 1., 0.]], [[2., 1., 0.]]))
    print(CNN.run_value([[1., 0., 0.], [0., 0., 1.], [1., 1., 0.], [2., 1., 0.]]))
    print("----------------")
    print(CNN.run_learning([[0.]], [[1., 0., 0.]], [[1., 1., 0.]]))
    print(CNN.run_value([[1., 0., 0.], [0., 0., 1.], [1., 1., 0.], [2., 1., 0.]]))
    print("----------------")
    print(CNN.run_learning([[0.]], [[2., 1., 0.]], [[1., 1., 0.]]))
    print(CNN.run_value([[1., 0., 0.], [0., 0., 1.], [1., 1., 0.], [2., 1., 0.]]))
    print("----------------")
    print(CNN.run_learning([[0.]], [[1., 0., 0.]], [[1., 1., 0.]]))
    print(CNN.run_value([[1., 0., 0.], [0., 0., 1.], [1., 1., 0.], [2., 1., 0.]]))
    print("----------------")
    print(CNN.run_learning([[0.]], [[1., 1., 0.]], [[2., 1., 0.]]))
    print(CNN.run_value([[1., 0., 0.], [0., 0., 1.], [1., 1., 0.], [2., 1., 0.]]))
    print("----------------")
    print(CNN.run_learning([[0.]], [[1., 0., 0.]], [[1., 1., 0.]]))
    print(CNN.run_value([[1., 0., 0.], [0., 0., 1.], [1., 1., 0.], [2., 1., 0.]]))
    print("----------------")
    print(CNN.run_learning([[0.]], [[2., 1., 0.]], [[1., 1., 0.]]))
    print(CNN.run_value([[1., 0., 0.], [0., 0., 1.], [1., 1., 0.], [2., 1., 0.]]))
    print("----------------")
    print(CNN.run_learning([[0.]], [[1., 0., 0.]], [[1., 1., 0.]]))
    print(CNN.run_value([[1., 0., 0.], [0., 0., 1.], [1., 1., 0.], [2., 1., 0.]]))
    print("----------------")
    print(CNN.run_learning([[0.]], [[1., 1., 0.]], [[2., 1., 0.]]))
    print(CNN.run_value([[1., 0., 0.], [0., 0., 1.], [1., 1., 0.], [2., 1., 0.]]))
    print("----------------")
    print(CNN.run_learning([[0.]], [[1., 0., 0.]], [[1., 1., 0.]]))
    print(CNN.run_value([[1., 0., 0.], [0., 0., 1.], [1., 1., 0.], [2., 1., 0.]]))
    print("----------------")
    print(CNN.run_learning([[0.]], [[2., 1., 0.]], [[1., 1., 0.]]))
    print(CNN.run_value([[1., 0., 0.], [0., 0., 1.], [1., 1., 0.], [2., 1., 0.]]))

