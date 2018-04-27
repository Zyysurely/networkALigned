import networkx as nx
import datetime
import requests
from collectData import SocialNetwork


def get_city(location):    # 对每种ip地址进行计算
    r = requests.get(url='http://api.map.baidu.com/geocoder/v2/', params={'location':location,'ak':'9ob1YaUCIxuQkxGEP5qjRwlutG554AYE','output':'json'})
    result = r.json()
    try:
        city = result['result']['addressComponent']['city']
        return city
    except:
        return None

# 将时间规范化
def get_format_time(line):
    vec = line.split('_')
    if len(vec) >= 2:
        if ('AM' not in vec[1] and 'PM' not in vec[1]):
            return ' '
        # slot = time.strptime(vec[0].strip('#'), '%H:%M',)
        # 10:09_AM_-_14_Jul_06
        if (vec[1] == 'PM'):
            return str(int(vec[0].strip('#').split(':')[0]) + 12) + ':' + vec[0].strip('#').split(':')[1]
        else:
            return vec[0].strip('#')
    else:
        return ' '


network = SocialNetwork(250)
tw_G = network.tw_G
four_G = network.four_G
all_location = dict()
location_file = open('location.txt', 'a+')
# foursqaure 的time和location，text进行整理
f = open('E:/graduate/twitter_foursquare/foursquare/locations/location', encoding='UTF-8', errors='ignore')
location_G = nx.Graph()
for line in f:
    lis = line.split('\n')[0].split('\t')
    if len(lis)>10:
        latitude = lis[9]
        longitude = lis[10]
        locationid = lis[0]
        location_G.add_node(locationid, latitude=latitude, longitude=longitude)

f = open('E:/graduate/twitter_foursquare/foursquare/tips/tip', encoding='UTF-8',errors='ignore')
tip_G = nx.Graph()
for line in f:
    lis = line.strip('\n').split('\t')
    tip_G.add_node(lis[0], location='')
    st = datetime.datetime.utcfromtimestamp(int(lis[1])) + datetime.timedelta(hours=-5)
    tip_G.node[lis[0]]["time"] = st.strftime('%Y-%m-%d %H:%M').split(' ')[1] # 时间
    tip_G.node[lis[0]]["word"] = lis[2].replace('_', ' ')    # word

f = open('E:/graduate/twitter_foursquare/foursquare/tips/tip_loc', encoding='UTF-8',errors='ignore')
for line in f:
    lis = line.strip('\n').split('\t')
    if(tip_G.has_node(lis[0]) and location_G.has_node(lis[1])):
        tip_G.node[lis[0]]["location"] = location_G.node[lis[1]]["latitude"] + '_' + location_G.node[lis[1]]["longitude"]

f = open('foursquare/tips/user_tip', encoding='UTF-8', errors='ignore')
for line in f:
    lis = line.strip('\n').split('\t')
    if (four_G.has_node(lis[0]) and tip_G.has_node(lis[1])):
        if len(tip_G.node[lis[1]]["time"]) > 1:
            four_G.node[lis[0]]["time"] = four_G.node[lis[0]]["time"] + tip_G.node[lis[1]]["time"] + ','
        if len(tip_G.node[lis[1]]["location"]) > 1:
            if tip_G.node[lis[1]]["location"] not in all_location.keys():
                temp_location = get_city(tip_G.node[lis[1]]["location"].replace('_', ','))
                all_location[tip_G.node[lis[1]]["location"]] = temp_location
                location_file.write(tip_G.node[lis[1]]["location"] + ' ' + temp_location + '\n')
            else:
                temp_location = all_location[tip_G.node[lis[1]]["location"]]
            four_G.node[lis[0]]["location"] = four_G.node[lis[0]]["location"] + temp_location + ','
#             four_G.node[lis[0]]["location"] = four_G.node[lis[0]]["location"] + get_city(tip_G.node[lis[1]]["location"].replace('_',',')) + ',
#         if(len(tip_G.node[lis[1]]["word"])>1):
#             four_G.node[lis[0]]["word"] = four_G.node[lis[0]]["word"] + tip_G.node[lis[1]]["word"] + ' '
tip_G.clear()
location_G.clear()

# 对twitter用户的活动地点以及时间进行整理结果
f_tweet = open('twitter/tweet', encoding='utf-8', errors='ignore')
tweet_G = nx.Graph()
for line in f_tweet:
    lis = line.strip('\n').split('\t')
    if (len(lis) >= 3):
        tweetid = lis[0]
        tweet_G.add_node(tweetid)
        tweet_G.node[tweetid]["tweet"] = lis[1]  # word
        if ('?' in lis[2]):
            location = lis[2].split('?')[1]
            f_time = lis[2].split('?')[0]
        else:
            f_time = lis[2]
            location = None
    tweet_G.node[tweetid]["location"] = location
    tweet_G.node[tweetid]["time"] = f_time


f_user_tweet = open('twitter/userTweet', encoding='utf-8', errors='ignore')
for line in f_user_tweet:
    lis = line.split('\n')[0].split('\t')
    userid = lis[0]
    if (tw_G.has_node(userid) and tweet_G.has_node(lis[1])):
        # 生成location的list
        if (tweet_G.node[lis[1]]["location"] is not None and len(tweet_G.node[lis[1]]["location"]) > 1):
            if tweet_G.node[lis[1]]["location"] not in all_location.keys():
                temp_location = get_city(tweet_G.node[lis[1]]["location"].replace('_', ','))
                all_location[tweet_G.node[lis[1]]["location"]] = temp_location
                location_file.write(tweet_G.node[lis[1]]["location"] + ' ' + temp_location + '\n')
            else:
                temp_location = all_location[tip_G.node[lis[1]]["location"]]
            tw_G.node[lis[0]]["location"] = four_G.node[lis[0]]["location"] + temp_location + ','
        if (tweet_G.node[lis[1]]["time"] is not None and len(tweet_G.node[lis[1]]["time"]) > 1):
            formattime = get_format_time(tweet_G.node[lis[1]]["time"])
            tw_G.node[userid]["time"] = tw_G.node[userid]["time"] + formattime + ','
#       tw_G.node[userid]["location"] = tw_G.node[userid]["location"] + get_city(tweet_G.node[lis[1]]["location"].replace('_',','))+ ','
#         # 生成word的list
#         if(tweet_G.node[lis[1]]["tweet"] is not None and len(tweet_G.node[lis[1]]["tweet"])>1):
#             tw_G.node[userid]["word"] = tw_G.node[userid]["word"] + tweet_G.node[lis[1]]["tweet"] + ' '
tweet_G.clear()

