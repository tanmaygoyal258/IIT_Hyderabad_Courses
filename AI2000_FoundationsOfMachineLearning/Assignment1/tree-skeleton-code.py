# FoML Assign 1 Code Skeleton
# Please use this outline to implement your decision tree. You can add any code around this.

from DecisionNode import DecisionNode
import csv

# Enter You Name Here
myname = "Amar-Akbar-Antony" # or "Amar-Akbar-Antony"

# Implement your decision tree below
class DecisionTree():
    tree = {}

    def learn(self, training_set):
        # implement this function
        rootNode = DecisionNode(0)
        #split into train_x and train_y 
        rootNode.train(train_x,train_y)
        self.tree = {} 

    # implement this function
    def classify(self, test_instance):
        result = 0 # baseline: always classifies as 0
        return result

def run_decision_tree():

    # Load data set
    with open("wine-dataset.csv") as f:
        next(f, None)
        data = [tuple(line) for line in csv.reader(f, delimiter=",")]
    print "Number of records: %d" % len(data)

    # Split training/test sets
    # You need to modify the following code for cross validation.
    K = 10
    training_set = [x for i, x in enumerate(data) if i % K != 9]
    test_set = [x for i, x in enumerate(data) if i % K == 9]
    
    tree = DecisionTree()
    # Construct a tree using training set
    tree.learn( training_set )

    # Classify the test set using the tree we just constructed
    results = []
    for instance in test_set:
        result = tree.classify( instance[:-1] )
        results.append( result == instance[-1])

    # Accuracy
    accuracy = float(results.count(True))/float(len(results))
    print "accuracy: %.4f" % accuracy       
    

    # Writing results to a file (DO NOT CHANGE)
    f = open(myname+"result.txt", "w")
    f.write("accuracy: %.4f" % accuracy)
    f.close()


if __name__ == "__main__":
    run_decision_tree()
