from logconfig import logger


class StrictStableMatching(object):
    def __init__(self, socialnetwork, result):
        self.four_result = dict()
        self.tw_result = dict()
        self.right = 0
        self.all = 0
        self.f_anchor_known_list = socialnetwork.f_anchor_known_list
        self.t_anchor_known_list = socialnetwork.t_anchor_known_list
        self.engage = dict()
        self.f = result

    def cut_k_list(self, k):
        logger.debug("k is %s" % (str(k)))
        # 产生配对的dict，设置k为3 four,tw 1,0，这里设置k
        four_result_list = dict()
        tw_result_list = dict()
        logger.info(len(self.f_anchor_known_list))
        for line in self.f:
            x_list = line.split(';')
            if len(x_list) == 3:
                rate = eval(x_list[2])[0]
                if x_list[0] in four_result_list:
                    four_result_list[x_list[0]][0].append(rate)
                    four_result_list[x_list[0]][1].append(x_list[1])  # 对应的twitter名
                else:
                    four_result_list[x_list[0]] = [[rate], [x_list[1]]]
                if x_list[1] in tw_result_list:
                    tw_result_list[x_list[1]][0].append(rate)
                    tw_result_list[x_list[1]][1].append(x_list[0])    # 对应的twitter名
                else:
                    tw_result_list[x_list[1]] = [[rate], [x_list[0]]]

        for item in four_result_list.keys():
            s = dict()
            for i in range(0, len(four_result_list[item][1])):
                s[four_result_list[item][1][i]] = four_result_list[item][0][i]
            s = sorted(s.items(), key=lambda j: j[1], reverse=True)
            s = map(lambda x: x[0], s)
            four_result_list[item] = list(s)
            if k is not None:
                if len(four_result_list[item]) > k-1:
                    four_result_list[item] = four_result_list[item][0:k]

        for item in tw_result_list.keys():
            s = dict()
            for i in range(0, len(tw_result_list[item][1])):
                s[tw_result_list[item][1][i]] = tw_result_list[item][0][i]
            s = sorted(s.items(), key=lambda j: j[1], reverse=True)
            s = map(lambda x: x[0], s)
            tw_result_list[item] = list(s)
            if k is not None:
                if len(tw_result_list[item]) > k-1:
                    tw_result_list[item] = tw_result_list[item][0:k]
        self.four_result = four_result_list
        self.tw_result = tw_result_list

    def match(self):
        logger.debug("matching")
        manprefers = self.tw_result          # dict形式，方便找人
        womanprefers = self.four_result
        women = sorted(womanprefers.keys())  # list形式
        men = sorted(manprefers.keys())
        manfree = men[:]  # twitter user who is free (not engaged)
        engaged = dict()  # map woman:man的格式, 也就是anchor的配对
        while manfree:    # still some man is free而且还没达到k的标准，是在list处就处理好的
            man = manfree.pop(0)
            if man not in self.t_anchor_known_list:
                manlist = manprefers[man]  # twitter用户对应的fourlist
                woman = manlist.pop(0)  # 弹出最想要配对的对象
                flag = 1
                while woman in self.f_anchor_known_list:
                    if len(manlist) == 0:
                        flag = 0
                        break
                    else:
                        woman = manlist.pop(0)
                if flag == 1:
                    fiance = engaged.get(woman)  # 目前的four对象
                    womanlist = womanprefers[woman]  # 最想要配对的four用户的twlist
                    if not fiance and man in womanlist:
                        # the woman is free
                        engaged[woman] = man
                    else:
                        if man in womanlist:
                            if womanlist.index(fiance) > womanlist.index(man):
                                # the woman is not free but she prefers this man rather than her old fiance
                                engaged[woman] = man
                                if manprefers[fiance]:
                                    manfree.append(fiance)
                            else:
                                # she is faithful to her old fiance
                                if manlist:  # 他还要想要配对的人选，否则对应单身
                                    manfree.append(man)
        return engaged

    def matching(self):
        self.engage = self.match()
        num = 0        # 正确判断的anchor links
        sums = 0       # 所有判断的anchor links
        for item in self.engage.keys():
            if item == self.engage[item]:
                if item not in self.f_anchor_known_list:
                    num = num + 1
            sums = sums + 1
        self.right = num
        self.all = sums
        logger.info(str(self.right) + ',' + str(self.all))
