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

7. Please summarize the papers below, using the following format. (4 * 5 pts)

**Motivation**: Why did the authors want to do the work?
**Novelty**: How is their method different from the previous works?
**Intuition**: Why would their method work and be better than the previous methods intuitively?
**Implementation**: The link to the code.

Papers:
- *Efficient Estimation of Word Representations in Vector Space*
- *Attention Is All You Need*
- *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*
- *MSA Transformer*