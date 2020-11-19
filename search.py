


import json
import urllib.request
import urllib.parse


import my_nlp
import wikipedia as wiki
import twitter



# ================================================================================
# 개인키 발급 필요
CONSUMER_KEY = 'lIceOgkpCIWcXjGFzkBRrPXdO'
CONSUMER_SECRET = 'lu11FJOaZJ7WJv8PdA5kBZ3qnhfAGxthF2ofUp1WzCo8bZVnwJ'
ACCESS_TOKEN = '1128592494294228994-Nw81ifgYkDD7JMSW8tbng3w7lkP1yN'
ACCESS_SECRET = '7nQx21ZxpGBM4Y4Ri0Zp1rcB9TyvD1luvqU0a64qchngQ'
twit_api = twitter.Api(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token_key=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)
# ================================================================================





# =====================================================================================================
# Wikipedia
wiki_api = 'https://en.wikipedia.org/w/api.php?action=query&prop=pageprops|pageterms&meta=wikibase&redirects&titles={}&format=json'


def search_wiki(key):
    print('search_wiki: key={}'.format(key))
    wiki_result = {}
    try:
        summary = wiki.summary(key)
        # ------------------------------------------------------------------------------
        # More Info from wiki_api
        wiki_id = ''
        label = ''
        aliases = []
        desc = ''
        url_content = urllib.request.urlopen(wiki_api.format(key.replace(' ', '_'))).read() # space는 '_' 로 변경
        data = json.loads(url_content)
        page_id = list(data['query']['pages'].keys())[0]
        page_dic = data['query']['pages'].get(page_id)
        if page_dic is not None and page_dic.get('terms') is not None:
            wiki_id = page_dic.get('pageprops').get('wikibase_item')
            label = page_dic.get('terms').get('label')[0]
            aliases = page_dic.get('terms').get('alias')
            desc = page_dic.get('terms').get('description')[0]
        # ------------------------------------------------------------------------------
        wiki_result.update({'wiki_id': wiki_id, 'label': label, 'aliases': aliases, 'desc': desc, 'summary': summary})
    except wiki.exceptions.DisambiguationError as err:
        wiki_result.update({'options': err.options})
    except Exception as ex:
        print(str(ex))
    return wiki_result



# =====================================================================================================
# Twitter
def search_twit(key, MAX_TWITS=20):
    print('search_twit: key=', key)
    #statuses = twit_api.GetSearch(raw_query="q={}&result_type=mixed&since=2019-01-01&count=100".format(key))
    statuses = twit_api.GetSearch(raw_query="q={}&result_type=mixed&count=100".format(key))
    twit_list = []
    count = 1
    for status in statuses:
        if status.user.verified == True:            # 공식 계정에 대해서만 조회
            twit_list.append(json.loads(str(status)))
            count += 1
            if count >= MAX_TWITS:
                break
    return twit_list




# ========================================================================================================
'''
key = 'Donalt Trump'
res_wiki = search_wiki(key)
summary = res_wiki.get('summary')

sents = my_nlp.get_nlp()(summary).sents
res_str = []
for sent in sents:
    res_str.append(sent.text)


key = 'Trump'
res_twit = search_twit(key)


for twit in res_twit:
    print()
    twit_text = twit.get('text')
    sents = my_nlp.get_nlp()(twit_text).sents
    for sent in sents:
        res_str.append(sent.text)


'''


