from sklearn.ensemble import RandomForestClassifier
from logconfig import logger


class Classifier(object):
    def __init__(self, socialnetwork, feature):
        self.socialnetwork = socialnetwork
        self.feature = feature
        self.result = self.run_classifier()

    def run_classifier(self):
        logger.debug("random forest")
        # 随机森林训练
        clf = RandomForestClassifier(n_estimators=100, max_depth=None, min_samples_split=2)
        clf = clf.fit(self.feature.x, self.feature.y)
        print(clf.feature_importances_)  # 每个特征的重要性
        s = clf.predict_proba(self.feature.xt)
        print(len(self.feature.xt))
        classify_result = []
        for i in range(0, len(s)):
            classify_result.append(self.feature.name[i] + ';' + str([s[i][0], s[i][1]]))
        return classify_result
