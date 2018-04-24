from collectData import SocialNetwork
from extractFeature import SimplifiedFeature
from classifier import Classifier
from strictMatching import StrictStableMatching


if __name__ == "__main__":
    networksPair = SocialNetwork(300)
    for itera in range(0, 10):
        feature = SimplifiedFeature(networksPair)
        classifier = Classifier(networksPair, feature)
        matching = StrictStableMatching(networksPair, classifier.result)
        if itera == 0:
            k_list = [None, 3, 1]
        else:
            k_list = [1]
        for k in k_list:
            matching.cut_k_list(k)
            matching.matching()
        networksPair.fresh_anchor_known(matching.engage)
        # 250  1037/1041
