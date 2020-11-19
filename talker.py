


import sys
import time
import datetime
import copy
import random
import numpy as np



#===========================================================================================================
# my packages
import my_nlp
import search
import utils




# ====================================================================================================
RECENT_DAYS = 30        # Twitter 최근정보 조회시
END_POINTS = ['.', '!', '?', '\n', '...']



class Talker:
    def __init__(self, interval=1, story_list=[]):
        print('\nTalker.__init__')
        # threading.Thread.__init__(self)       # for thread
        #
        self.interval = interval
        self.stories = story_list
    #
    # -------------------------------------------------------------------------------
    #def run(self):             # for thread
    def talking(self, start_keyword='BTS', n_stories=1000):
        cnt_total_stories = 0
        cnt_keyword_stories = 0
        #
        story_keyword = start_keyword
        while_cnt = 0
        while cnt_total_stories < n_stories:
            while_cnt += 1
            if while_cnt >= n_stories:
                break
            # ---------------------------------------------------------
            # Search Interesting Story
            selected_stories = []
            try:
                stories = []
                # -----------------------------------------------------
                wiki_dic = search.search_wiki(story_keyword)
                # print('wiki_dic:', wiki_dic)
                summary = wiki_dic.get('summary')
                if summary is not None:
                    sents = my_nlp.get_nlp()(summary).sents
                    for sent in sents:
                        try:
                            sent_text = sent.text.strip()
                            if sent_text[-1] in END_POINTS and sent_text not in stories:
                                stories.append(sent_text)
                        except Exception as ex:
                            print(str(ex))
                #
                # -----------------------------------------------------
                twit_list = search.search_twit(story_keyword)
                # print('twit_list:', twit_list)
                for twit in twit_list:
                    twit_text = twit.get('text')
                    sents = my_nlp.get_nlp()(twit_text).sents
                    for sent in sents:
                        try:
                            sent_text = sent.text
                            if 'RT @' in sent_text:
                                continue
                            if sent_text[-1] in END_POINTS and sent_text not in stories:
                                stories.append(sent_text)
                        except Exception as ex:
                            print(str(ex))
                # ----------------------------------------------------------------------------
                for i in range(np.min([5, len(stories)])):
                    selected_story = utils.randomChoice(stories).strip()
                    print('\t', cnt_total_stories, selected_story)
                    selected_stories.append(selected_story)
                    self.stories.append([story_keyword, selected_story])
                    cnt_keyword_stories += 1
                    cnt_total_stories += 1
                #
            except Exception as ex:
                print(str(ex))
            finally:
                # -------------------------------------------------------
                # Change story_keyword ? : 마지막 story에서 entity를 뽑아서 랜덤주제 변경
                print(selected_stories)
                if selected_stories is not None and len(selected_stories) > 0:
                    last_story = selected_stories[-1]
                    entities, _, _, _ = my_nlp.get_entities(last_story)
                    if len(entities) != 0:
                        new_keyword = utils.randomChoice(entities)
                        if new_keyword != story_keyword:
                            story_keyword = new_keyword
                            cnt_keyword_stories = 0
                # -------------------------------------------------------
            #
            time.sleep(self.interval)   # CPU 먹통방지



# ================================================================================================
TOO_MUCH_STORIES = []       # 스토리 저장


interval = 1
num_of_stories = 100                                           # n개 스토리
now = datetime.datetime.now()
today = now.strftime('%Y%m%d')




# start_key = 'Donald Trump'
start_key = 'Covid19'
talker = Talker(interval, TOO_MUCH_STORIES)
talker.talking(start_key, num_of_stories)                       # thread로 만들수도




import pandas as pd
pd_stories = pd.DataFrame(TOO_MUCH_STORIES)
pd_stories.to_csv('too_much_stories_{}.csv'.format(today), index=None, header=None, encoding='utf-8-sig')




