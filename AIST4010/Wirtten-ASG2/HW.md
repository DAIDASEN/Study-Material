# Questions

1. What is gradient vanishing and gradient explosion? How do we solve the two problems? (Please provide at least THREE valid methods) (10 pts)

2. What are the differences and similarities between 2D convolution and 3D convolution? (5 pts)

3. Suppose you are training a neural network, and you find the training loss doesn't decrease in the first several epochs. What are possible reasons? (Please provide at least THREE reasons) (10 pts)

4. How would imbalanced datasets affect the training and prediction results of deep learning methods? (*e.g.*, a certain class has many more samples than the other classes) Please suggest at least THREE possible ways to alleviate the issue. (10 pts)

5. Please implement LeNet using the PyTorch library and train it on the Fashion-MNIST dataset. Record its performance on the test set, and take the results as the baseline. Then try the following experiments to see how the test accuracy varies compared to the baseline. For every experiment, please try at least TWO settings and record the results. Then please report the best result and the corresponding settings. (35 pts)
   - a. Add or remove several CONV layers.
   - b. Add or remove several FC layers.
   - c. Add some other layers like 'dropout'.
   - d. Adjust the setting of the Pooling layer (e.g., Avg or Max, kernel size)
   - e. Adjust the convolution window size.
   - f. Adjust the number of output channels for several layers.
   - g. Use a different activation function (e.g., ReLU).

6. In A1, we implemented SGD using NumPy. Now, please implement the Adam optimizer using NumPy and apply it to the program (logistic regression) from A1. Please compare the convergence speed (plot the loss function of the training data) of Adam and SGD (learning rate=10⁻⁴) with the default hyperparameters discussed during class. (10 pts)

补充信息:
以下是刚刚提到的A1中的有关的题目描述，有关的py文件是tex文件夹下的A1_Q4_sample.py
Let’s implement logistic regression using different methods. Before we use PyTorch, let
us build everything from scratch. That is, you are only allowed to use NumPy to perform
basic calculations and optimization.
We provide a sample Python code file including the assignment pipeline. Please follow the
instructions and write the functions to finish this assignment. Remember to keep the seed
unchanged to make sure the result can be the same.
a. Data generation: Please generate a dataset of two classes, each having 1000 points and
100 features. The two classes should be generally linearly separable, but please add
some Gaussian noise to the data to create some overlap (i.e., not perfectly separable).
Please also generate a testing dataset with a total of 100 points (approx. 50 per class).
(4 pts)
b. Please implement logistic regression only using NumPy and run gradient descent (GD)
to find your function to separate the data. Please record the training and testing loss
history, the parameters W and b, and calculate the accuracy. (5 pts)
c. Please run SGD to learn the decision function that separates the data. Please record the
training/testing loss history, the parameters W and b, and calculate the accuracy. (3 pts)
d. Please plot the training and testing loss curves during training using the loss history.
Save the figures and insert them into your report. (3 pts)
e. Please use the PyTorch framework to implement logistic regression. In your
implementation, please make full use of PyTorch's tensor operations and avoid using
an explicit for loop to iterate over individual samples within a data batch. Also, record
the training/testing loss history and the parameters W and b, calculate the accuracy, and
plot the training/testing loss curves. (5 pts)

课程中我们提到的default hyperparameter:
ADAM 优化器默认超参数

| 参数 | 符号 | 默认值 |
|------|------|--------|
| 学习率 | $\alpha$ | 0.001 |
| 一阶矩衰减率 | $\delta$ | 0.9 |
| 二阶矩衰减率 | $\gamma$ | 0.999 |
| 数值稳定项 | $\epsilon$ | $10^{-7}$ |

SGD超参数
α 0.001
β 0.9

1. Please summarize the papers below, using the following format. (4 * 5 pts)

**Motivation**: Why did the authors want to do the work?
**Novelty**: How is their method different from the previous works?
**Intuition**: Why would their method work and be better than the previous methods intuitively?
**Implementation**: The link to the code.

Papers:
- *Efficient Estimation of Word Representations in Vector Space*
- *Attention Is All You Need*
- *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*
- *MSA Transformer*