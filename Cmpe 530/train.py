'''
Created on Nov 7, 2016

@author: miracgoksuozturk
'''

import numpy
import tensorflow as tf
from random import shuffle


# Dataset is open and available at https://archive.ics.uci.edu/ml/datasets/ISOLET 
train_file = 'isolet1+2+3+4.data'
test_file = 'isolet5.data'
train_size = 5200
dev_size = 1000
test_size = 1500
lr = 0.005
layer_size = 200
in_dim = 617
out_dim = 26
dropout = 1.0
batch_size = 200
momnt = 0.3

sess = tf.InteractiveSession()
x = tf.placeholder("float", shape=[None, in_dim])
y_ = tf.placeholder("float", shape=[None, out_dim])

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)
    

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def variable_summaries(var):
    """Attach a lot of summaries to a Tensor (for TensorBoard visualization)."""
    with tf.name_scope('summaries'):
        mean = tf.reduce_mean(var)
        tf.summary.scalar('mean', mean)
        with tf.name_scope('stddev'):
            stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
            tf.summary.scalar('stddev', stddev)
            tf.summary.scalar('max', tf.reduce_max(var))
            tf.summary.scalar('min', tf.reduce_min(var))
            tf.summary.histogram('histogram', var)

def nn_layer(input_tensor, input_dim, output_dim, layer_name, keep_prob, act=tf.nn.relu):
    """Reusable code for making a simple neural net layer.

      It does a matrix multiply, bias add, and then uses relu to nonlinearize.
      It also sets up name scoping so that the resultant graph is easy to read,
      and adds a number of summary ops.
      """
    # Adding a name scope ensures logical grouping of the layers in the graph.
    with tf.name_scope(layer_name):
        # This Variable will hold the state of the weights for the layer
        with tf.name_scope('weights'):
            weights = weight_variable([input_dim, output_dim])
            variable_summaries(weights)
        with tf.name_scope('biases'):
            biases = bias_variable([output_dim])
            variable_summaries(biases)
        with tf.name_scope('Wx_plus_b'):
            preactivate = tf.matmul(input_tensor, weights) + biases
            tf.nn.dropout(preactivate, keep_prob)
            tf.summary.histogram('pre_activations', preactivate)
            activations = act(preactivate, name='activation')
            tf.summary.histogram('activations', activations)
    return activations


keep_prob = tf.placeholder(tf.float32)
activation1 = nn_layer(x, in_dim, layer_size, 'layer1', keep_prob, act=tf.nn.relu)
activation2 = nn_layer(activation1, layer_size, layer_size, 'layer2', keep_prob, act=tf.nn.relu)
activation3 = nn_layer(activation2, layer_size, layer_size, 'layer3', keep_prob, act=tf.nn.relu)
y = nn_layer(activation3, layer_size, out_dim, 'layer4', keep_prob, act=tf.nn.relu)


with tf.name_scope('cross_entropy'):
    # The raw formulation of cross-entropy,
    #
    # tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(tf.softmax(y)),
    #                               reduction_indices=[1]))
    #
    # can be numerically unstable.
    #
    # So here we use tf.nn.softmax_cross_entropy_with_logits on the
    # raw outputs of the nn_layer above, and then average across
    # the batch.
    diff = tf.nn.softmax_cross_entropy_with_logits(y, y_)
    with tf.name_scope('total'):
        cross_entropy = tf.reduce_mean(diff)
tf.summary.scalar('cross_entropy', cross_entropy)

with tf.name_scope('train'):
    train_step = tf.train.RMSPropOptimizer(learning_rate=lr, momentum=momnt).minimize(cross_entropy)

with tf.name_scope('accuracy'):
    with tf.name_scope('correct_prediction'):
        correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    with tf.name_scope('accuracy'):
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
tf.summary.scalar('accuracy', accuracy)

# Merge all the summaries and write them out to /tmp/mnist_logs (by default)
merged = tf.summary.merge_all()
train_writer = tf.summary.FileWriter('summary' + '/train',
                                      sess.graph)
test_writer = tf.summary.FileWriter('summary' + '/test')
tf.global_variables_initializer().run()




X = []
Y = []

with open(train_file) as f:
    for line in f:
        tokens = line.split(', ')
        vec = numpy.array(tokens[:-1]).astype(numpy.float)
        lab = numpy.zeros((out_dim,))
        lab_ind = tokens[-1].rsplit('.')[0]
        lab[int(lab_ind)-1] = 1
        X.append(vec)
        Y.append(lab)
        
        
valX = numpy.array(X[-dev_size:])
valY = numpy.array(Y[-dev_size:])       
X = numpy.array(X[:train_size])
Y = numpy.array(Y[:train_size])

testX = []
testY = []

with open(test_file) as f:
    for line in f:
        tokens = line.split(', ')
        vec = numpy.array(tokens[:-1]).astype(numpy.float)
        lab = numpy.zeros((out_dim,))
        lab_ind = tokens[-1].rsplit('.')[0]
        lab[int(lab_ind)-1] = 1
        testX.append(vec)
        testY.append(lab)
        
testX = numpy.array(testX[:test_size])
testY = numpy.array(testY[:test_size])

  
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))

accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# sess.graph_def is the graph definition; that enables the Graph Visualizer.
summary_writer = tf.summary.FileWriter('logs', sess.graph)


for e in range(100):
    XY = list(zip(X,Y))
    shuffle(XY)
    trainX, trainY = zip(*XY)
    for i in xrange(len(trainX)/batch_size):
        summary, _ = sess.run([merged, train_step], feed_dict={x: trainX[batch_size*i:batch_size*i+batch_size], y_: trainY[batch_size*i:batch_size*i+batch_size], keep_prob: dropout})
        train_writer.add_summary(summary, e)
        
    print 'epoch: %d' %e
    
    summary, acc = sess.run([merged, accuracy], {x: valX, y_:valY, keep_prob: 1.0})
    test_writer.add_summary(summary, i)
    print 'Acc : %f' %acc

acc = accuracy.eval(feed_dict={x: testX, y_:testY, keep_prob: 1.0})
print 'Test Acc : %f' %acc

 

