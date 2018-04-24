import networkx as nx
import random
from logconfig import logger


class SocialNetwork(object):
    def __init__(self, random_num):
        self.four_G = nx.Graph()       # Foursquare无向图
        self.tw_G = nx.Graph()         # Twitter无向图
        self.f_anchor_known_list = []  # 设定的事先知道的anchor link foursquare
        self.t_anchor_known_list = []  # 设定的事先知道的anchor link twitter
        self.f_all_anchor_list = []
        self.t_all_anchor_list = []
        self.random_num = random_num   # 控制已知数量
        self.random_list = []  # 随机生成提前知道的anchor user数
        self.set_network()
        self.set_follow(random_num)

    # 存入所有的节点和节点属性
    def set_network(self):
        logger.debug("save node")
        f = open('E:/graduate/twitter_foursquare/foursquare/users/user', encoding='utf-8')
        twitter_file = open('E:/graduate/twitter_foursquare/twitter/user', encoding='utf-8')
        for line in twitter_file:
            tw_list = line.split('\t')
            user_name = tw_list[0]
            if len(user_name) > 1 and len(tw_list) >= 5:
                self.tw_G.add_node(user_name, time='', location='', word='', fourID=None)

        # foursquare 目前只将对应的twitterid存了进去，其它的属性未存,
        # location=tw_list[4],  realname=tw_list[2], bio=tw_list[3], home=tw_list[4]
        num = 0
        for line in f:
            lis = line.split('\t')
            userFourID = lis[0]
            if 'com' in lis[7]:
                userTwitterID = lis[7].split('twitter.com/')[1]
                if self.tw_G.has_node(userTwitterID):
                    num = num + 1
                    self.four_G.add_node(userFourID, twitterID=userTwitterID, location='', time='', word='', in_test=0)
                    self.tw_G.node[userTwitterID]["fourID"] = userFourID  # 标明 tw对应的four ID
                    self.f_all_anchor_list.append(userFourID)
                    self.t_all_anchor_list.append(userTwitterID)
                else:
                    self.four_G.add_node(userFourID, twitterID=None, location='', time='', word='', in_test=0)
        f.close()
        twitter_file.close()

    # 存入用户的follow关系
    def set_follow(self, random_num):
        logger.debug("save follow")
        tw_f = open('E:/graduate/twitter_foursquare/twitter/following')
        for line in tw_f:
            user1 = line.split('\t')[0]
            user2 = line.split('\t')[1].split('\n')[0]
            if self.tw_G.has_node(user1) and self.tw_G.has_node(user2):
                if self.tw_G.has_edge(user2, user1):
                    self.tw_G.edges[user2, user1]["weight"] = 2
                    if user1 in self.t_anchor_known_list and user2 in self.f_anchor_known_list:
                        f_user1 = self.tw_G.node[user1]["fourID"]
                        f_user2 = self.tw_G.node[user2]["fourID"]
                        self.four_G.add_edge(f_user1, f_user2, weight=2)
                else:
                    self.tw_G.add_edge(user1, user2, weight=1)
                    if user1 in self.t_anchor_known_list and user2 in self.f_anchor_known_list:
                        f_user1 = self.tw_G.node[user1]["fourID"]
                        f_user2 = self.tw_G.node[user2]["fourID"]
                        self.four_G.add_edge(f_user1, f_user2, weight=1)
        tw_f.close()

        f = open('E:/graduate/twitter_foursquare/foursquare/users/user_following')
        for line in f:
            user1 = line.split('\t')[0]
            user2 = line.split('\t')[1].split('\n')[0]
            if self.four_G.has_node(user1) and self.four_G.has_node(user2):
                if self.four_G.has_edge(user2, user1):
                    self.four_G.edges[user2, user1]["weight"] = 2
                    if user1 in self.f_anchor_known_list and user2 in self.f_anchor_known_list:
                        t_user1 = self.four_G.node[user1]["twitterID"]
                        t_user2 = self.four_G.node[user2]["twitterID"]
                        if self.tw_G.has_edge(t_user1, t_user2):
                            self.tw_G.edges[t_user2, t_user1]["weight"] = 2
                else:
                    self.four_G.add_edge(user1, user2, weight=1)
                    if user1 in self.f_anchor_known_list and user2 in self.f_anchor_known_list:
                        t_user1 = self.four_G.node[user1]["twitterID"]
                        t_user2 = self.four_G.node[user2]["twitterID"]
                        self.tw_G.add_edge(t_user1, t_user2, weight=1)

        # 删除twitter中的单向关系
        self.tw_G.remove_edges_from([e for e in self.tw_G.edges() if self.tw_G.edges[e]["weight"] == 1])

        # 删除边缘节点
        vdict = self.four_G.degree()
        r_node = [v for v in self.four_G if vdict[v] < 1]
        for v in r_node:
            if v in self.f_all_anchor_list:
                self.f_all_anchor_list.remove(v)
                self.t_all_anchor_list.remove(self.four_G.node[v]['twitterID'])
        self.four_G.remove_nodes_from(r_node)

        vdict = self.tw_G.degree()
        r_node = [v for v in self.tw_G if vdict[v] < 1]
        for v in r_node:
            if v in self.t_all_anchor_list:
                self.t_all_anchor_list.remove(v)
                self.f_all_anchor_list.remove(self.tw_G.node[v]['fourID'])
        self.tw_G.remove_nodes_from(r_node)

        # 生成事先知道的锚用户
        self.random_list = [168, 350, 1286, 120, 803, 1093, 736, 130, 1187, 1210, 50, 579, 604, 1135, 1278, 1326, 330, 875, 1390, 95, 173, 698, 1067, 665, 1457, 458, 1281, 1197, 789, 147, 641, 1085, 1239, 13, 512, 343, 808, 539, 1402, 575, 829, 88, 1219, 346, 1221, 911, 1103, 1002, 426, 1414, 772, 373, 104, 162, 666, 809, 307, 1391, 887, 1463, 1060, 448, 1238, 1438, 1164, 419, 85, 949, 756, 7, 896, 954, 1481, 1399, 1468, 1251, 847, 398, 286, 1044, 595, 1176, 622, 1009, 1173, 530, 1094, 107, 1188, 1101, 1070, 793, 450, 1016, 746, 706, 1134, 719, 625, 909, 974, 1317, 890, 1019, 823, 962, 639, 587, 918, 1181, 294, 748, 425, 280, 1150, 1376, 226, 475, 661, 877, 599, 714, 917, 786, 124, 101, 160, 1350, 237, 205, 317, 920, 204, 1227, 105, 1448, 77, 649, 1245, 873, 15, 1088, 966, 672, 366, 1436, 1405, 1112, 175, 251, 108, 969, 1100, 674, 906, 1379, 1035, 891, 1108, 57, 1306, 263, 364, 1119, 1299, 463, 1032, 729, 281, 971, 610, 732, 731, 460, 1471, 945, 761, 525, 78, 150, 468, 1358, 38, 245, 1147, 1024, 788, 1124, 157, 831, 1470, 720, 2, 952, 1480, 279, 109, 1183, 424, 1268, 523, 276, 1036, 28, 930, 380, 540, 1454, 934, 1437, 912, 106, 1460, 697, 899, 801, 296, 686, 1171, 305, 895, 946, 103, 1000, 704, 807, 191, 755, 1250, 1406, 321, 987, 943, 1450, 1469, 1143, 1395, 1479, 135, 1021, 769, 1247, 1426, 614, 1374, 1318, 148, 1081, 678, 922, 423, 898, 629, 96, 230, 859, 222, 27, 312, 1010, 481, 269, 1079, 991, 1389, 832, 358, 90, 394, 257, 411, 667, 1475, 495, 500, 692, 711, 1242, 445, 754, 329, 1284, 180, 1220, 693, 618, 747, 1089, 1215, 1413, 229, 781, 1082, 368, 75, 267, 241, 370, 270, 824]
        # self.random_list = random.sample(range(0, len(self.f_all_anchor_list)), random_num)  # 随机生成提前知道的anchor user数
        for i in self.random_list:
            self.f_anchor_known_list.append(self.f_all_anchor_list[i])
            self.four_G.node[self.f_all_anchor_list[i]]["in_test"] = 1
            self.t_anchor_known_list.append(self.t_all_anchor_list[i])
        logger.info(self.random_list)
        logger.info(nx.info(self.tw_G))
        logger.info(nx.info(self.four_G))
        print("length of already known anchor list:", len(self.f_anchor_known_list), len(self.t_anchor_known_list))
        print("length of all anchor list:", len(self.f_all_anchor_list), len(self.t_all_anchor_list))

    def fresh_anchor_known(self, engage):
        s = len(engage.keys())
        random_anchor_list = random.sample(engage.keys(), int(0.8 * s))
        for item in engage.keys():
            if item in random_anchor_list:
                self.four_G.node[item]['in_test'] = 1
                self.four_G.node[item]['twitterID'] = engage[item]
                self.tw_G.node[engage[item]]['fourID'] = item
                self.f_anchor_known_list.append(item)
                self.t_anchor_known_list.append(engage[item])
        # 根据已知的将网络进行扩展
        for item in self.four_G.edges():
            if item[0] in self.f_anchor_known_list and item[1] in self.f_anchor_known_list:
                tw1 = self.four_G.node[item[0]]["twitterID"]
                tw2 = self.four_G.node[item[1]]["twitterID"]
                self.tw_G.add_edge(tw1, tw2)
        for item in self.tw_G.edges():
            if item[0] in self.t_anchor_known_list and item[1] in self.t_anchor_known_list:
                four1 = self.tw_G.node[item[0]]["fourID"]
                four2 = self.tw_G.node[item[1]]["fourID"]
                self.four_G.add_edge(four1, four2)
