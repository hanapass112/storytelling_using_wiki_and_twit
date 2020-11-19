

import copy
import spacy


# load nlp components
spacy_nlp = spacy.load('en_core_web_sm')



def get_nlp():
    return spacy_nlp


# ============================================================================================
def merge_compound(spacy_docs, DEBUG=False):
    try:
        # Compound word Check : Auto
        span_start = -1
        index = 0
        for i in range(len(spacy_docs)):
            t = spacy_docs[index]
            index += 1
            if t.dep_ == 'punct':
                continue
            if t.dep_ == 'compound':
                if span_start == -1:
                    span_start = index - 1
                if DEBUG:
                    print('\t', span_start, index)
                continue
            if span_start > -1:
                span = spacy_docs[span_start: index]
                span.merge()
                if DEBUG:
                    print(spacy_docs[span_start])
                # 초기화
                index = span_start + 1
                span_start = -1
                if DEBUG:
                    print('\t', span_start, index)
    except Exception as ex:
        print(str(ex))
    return spacy_docs




# ---------------------------------------------------------------------------------------------------
# Find PRORP and check Wikipedia
def get_entities(content, compounds=[]):
    entities = []
    keywords_noun = []
    keywords_verb = []
    spacy_docs = spacy_nlp(content)
    # ------------------------------------------------
    # Manual Compound
    for compound in compounds:
        doc_comp = spacy_nlp(compound)
        if compound.lower() in content.lower():
            start = -1
            end = -1
            for i in range(len(spacy_docs)):
                if i >= len(spacy_docs) - 1:
                    break
                if doc_comp[0].text in spacy_docs[i].text and start == -1:
                    start = i
                if doc_comp[-1].text in spacy_docs[i].text and start != -1 and end == -1:
                    end = i
                    span = spacy_docs[start: end + 1]
                    span.merge()
                    start = -1
                    end = -1
    spacy_docs = merge_compound(spacy_docs)
    # ------------------------------------------------
    # Entities
    for t in spacy_docs:
        if t.pos_ in ['PROPN']:
            ent_text = t.text
            # ======================
            # Hardcoding
            if ent_text.lower() in ['year', 'month', 'week', 'day']:
                continue
            # ======================
            if ent_text not in entities:
                entities.append(ent_text)
            # ------------------------------------------------
            # Merge again: Rookie of the Year
            t_rights = list(t.rights)
            while t_rights != []:
                for right in t_rights:
                    t_lefts = list(right.lefts)
                    for left in t_lefts:
                        ent_text = ent_text + ' ' + left.text
                    ent_text = ent_text + ' ' + right.text
                    t_rights = list(right.rights)
            #before_entity = ent_text
            if ent_text not in entities:
                entities.append(ent_text)
    # ------------------------------------------------
    # Keywords_noun
    for t in spacy_docs:
        t_text = t.lemma_.strip()
        if t.pos_ == 'NOUN' and t.tag_ == 'NN'\
                and 'http://' not in t_text:
            keywords_noun.append(t_text.lower())
    # ------------------------------------------------
    # Keywords_verb
    for t in spacy_docs:
        t_text = t.lemma_.strip()
        if t.pos_ == 'VERB' and t.dep_ == 'ROOT' \
                and t_text not in ['be', 'say']:
            keywords_verb.append(t_text.lower())
    # ------------------------------------------------
    return entities, keywords_noun, keywords_verb, spacy_docs

