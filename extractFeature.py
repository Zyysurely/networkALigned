import math
from logconfig import logger
import networkx as nx


class SimplifiedFeature(object):
    def __init__(self, socialnetwork):
        self.four_G = socialnetwork.four_G
        self.tw_G = socialnetwork.tw_G
        self.socialnetwork = socialnetwork
        self.y = []
        self.x = []
        self.yt = []
        self.xt = []
        self.name = []
        self.positive = []
        self.negative = []
        self.set_feature()

    def set_feature(self):
        logger.debug("set_feature of node pairs")
        for item in self.four_G.nodes(data=True):
            for item1 in self.tw_G.nodes(data=True):
                f_real_nei = list(self.four_G.neighbors(item[0]))
                f_nei = []
                com_nei = []
                for i in f_real_nei:
                    if self.four_G.node[i]["in_test"] == 1:     # foursquare中哪些是已知的
                        f_nei.append(self.four_G.node[i]["twitterID"])
                        com_nei.append(i)
                t_nei = list(self.tw_G.neighbors(item1[0]))
                result = [v for v in t_nei if v in f_nei]      # 共同的已知的neighbor的多少
                length = len(com_nei)
                res_four = []
                for i in range(0, length):
                    if f_nei[i] in result:
                        res_four.append(com_nei[i])
                CN = len(result)
                if (len(f_real_nei) + len(t_nei) - CN) > 0:
                    JC = CN / (len(f_real_nei) + len(t_nei) - CN)
                else:
                    JC = 0
                AA = 0
                for i in res_four:
                    jh = len(list(self.four_G.neighbors(i))) + len(list(self.tw_G.neighbors(self.four_G.node[i]["twitterID"])))
                    if jh != 2:
                        AA = AA + 1 / math.log(jh / 2)
                social_feature = (CN + JC + AA) / 3
                label = 0
                if item1[0] == item[1]["twitterID"]:
                    label = 1
                # s = item[0] + ',' + item1[0] + ',' + str(social_feature) + ',' + str(label) + '\n'
                # if label == 1:
                # #     self.positive.append(s)
                # # else:
                # #     self.negative.append(s)

                if label == 1:
                    if item[0] in self.socialnetwork.f_anchor_known_list:
                        self.y.append(1)
                        self.x.append([social_feature])
                    else:
                        self.xt.append([social_feature])
                        self.name.append(item[0] + ';' + item1[0])
                else:
                    if item[0] in self.socialnetwork.f_anchor_known_list or item1[0] in self.socialnetwork.t_anchor_known_list:
                        self.y.append(0)
                        self.x.append([social_feature])
                    else:
                        self.xt.append([social_feature])
                        self.name.append(item[0] + ';' + item1[0])
