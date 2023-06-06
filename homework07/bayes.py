from math import log


class NaiveBayesClassifier:
    def __init__(self, alpha=1):
        self.alpha = alpha
        self.class_probs = []
        self.classes = []
        self.vocab = dict()
        self.classes_count = dict()
        self.class_word_probs = dict()

    def fit(self, X, y):
        """Fit Naive Bayes classifier according to X, y."""
        self.classes = sorted(set(y))
        self.class_probs = {w: (y.count(w) / len(y)) for w in self.classes}
        self.classes_count = {c: 0 for c in self.classes}

        uniq = []
        for x in X:
            uniq += x.split()
        uniq = sorted(set(uniq))

        self.vocab = {token: [0] * len(self.classes) for token in uniq}

        for i, x in enumerate(X):
            for token in x.split():
                self.vocab[token][self.classes.index(y[i])] += 1
                self.classes_count[y[i]] += 1

        d = len(uniq)
        self.class_word_probs = {
            c: [
                (self.vocab[token][self.classes.index(c)] + self.alpha) / (self.classes_count[c] + self.alpha * d)
                for token in self.vocab
            ]
            for c in self.classes
        }

    def predict(self, X):
        """Perform classification on an array of test vectors X."""
        Y = [None] * len(X)
        for i, x in enumerate(X):
            class_predictions = []
            for c in self.classes:
                predict = log(self.class_probs[c])
                for token in x.split():
                    if token in self.vocab:
                        P = self.class_word_probs[c][list(self.vocab.keys()).index(token)]
                        predict += log(P)
                class_predictions.append(predict)
            Y[i] = self.classes[class_predictions.index(max(class_predictions))]
        return Y

    def score(self, X_test, y_test):
        """Returns the mean accuracy on the given test data and labels."""
        Y_pred = self.predict(X_test)
        correct = sum([1 for i in range(len(y_test)) if Y_pred[i] == y_test[i]])
        total = len(y_test)
        return correct / total
