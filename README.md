naivebayes.py\
Description\
This program takes 3 command line arguments:name of training data file, name of input data file, and name of output data file. It would train a Naive Bayes classifier from the training file, use it to predict the input, and write the result on the output file\
This program would only take arff format with sets of attributes. It could not handle numeric or special type of attributes

evaluate.py\
Description\
This program takes 1 command line argument:name of the data file. It would perform leave-one-out cross-validation and use Naive Bayes classifier for prediction. It would generate a file called result.txt, which store the result from each training and validation dataset. The confusion matrix would be show on the screen
