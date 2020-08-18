import pickle
import os
import collections
import sys
import random

sys.path.append('./pycocoevalcap')
from pycocoevalcap.bleu.bleu import Bleu
from pycocoevalcap.rouge.rouge import Rouge
from pycocoevalcap.meteor.meteor import Meteor
#from pycocoevalcap.cider.cider import Cider

class Evaluate(object):
    def __init__(self):
        self.scorers = [
            (Bleu(4), ["Bleu_1", "Bleu_2", "Bleu_3", "Bleu_4"]),
            # (Meteor(), "METEOR"),
            (Rouge(), "ROUGE_L")
        ]#,        (Cider(), "CIDEr")

    def convert(self, data):
        if isinstance(data, basestring):
            return data.encode('utf-8')
        elif isinstance(data, collections.Mapping):
            return dict(map(convert, data.items()))
        elif isinstance(data, collections.Iterable):
            return type(data)(map(convert, data))
        else:
            return data

    def score(self, ref, hypo):
        final_scores = {}
        for scorer, method in self.scorers:
            score, scores = scorer.compute_score(ref, hypo)
            if type(score) == list:
                for m, s in zip(method, score):
                    final_scores[m] = s
            else:
                final_scores[method] = score

        return final_scores

    def evaluate(self, get_scores=True, live=False, **kwargs):
        if live:
            temp_ref = kwargs.pop('ref', {})
            cand = kwargs.pop('cand', {})
        else:
            reference_path = kwargs.pop('ref', '')
            candidate_path = kwargs.pop('cand', '')

            # load caption data
            with open(reference_path, 'rb') as f:
                temp_ref = pickle.load(f)
            with open(candidate_path, 'rb') as f:
                cand = pickle.load(f)

        # make dictionary
        hypo = {}
        ref = {}
        i = 0
        for vid, caption in cand.items():
            hypo[i] = [caption]
            ref[i] = temp_ref[vid]
            i += 1

        # compute scores
        final_scores = self.score(ref, hypo)
        #"""
        # print out scores
        # print ('Bleu_1:\t', final_scores['Bleu_1'])
        # print ('Bleu_2:\t', final_scores['Bleu_2'])
        # print ('Bleu_3:\t', final_scores['Bleu_3'])
        # print ('Bleu_4:\t', final_scores['Bleu_4'])
        # # print ('METEOR:\t', final_scores['METEOR'])
        # print ('ROUGE_L:', final_scores['ROUGE_L'])
        # #print ('CIDEr:\t', final_scores['CIDEr'])
        # """

        if get_scores:
            return final_scores['Bleu_4']


if __name__ == '__main__':
    '''
    cands = {'generated_description1': 'how are you', 'generated_description2': 'Hello how are you'}
    refs = {'generated_description1': ['what are you', 'where are you'],
           'generated_description2': ['Hello how are you', 'Hello how is your day']}
    '''
    # with open(sys.argv[1]) as f:
    #   cands = {'generated_description'+str(i):x.strip() for i,x in enumerate(f.readlines())}
    # with open(sys.argv[2]) as f:
    #   refs = {'generated_description'+str(i):[x.strip()] for i,x in enumerate(f.readlines())}
    # x = Evaluate()
    # x.evaluate(live=True, cand=cands, ref=refs)

    with open(sys.argv[1]) as f:
      cands = {'generated_description'+str(i):x.strip() for i,x in enumerate(f.readlines())}
    with open(sys.argv[2]) as f:
      refs = {'generated_description'+str(i):[x.strip()] for i,x in enumerate(f.readlines())}
    x = Evaluate()
    bleu_scores = []
    bleu_id = []
    stack_num = 50
    cands_num = len(cands.keys())  # 1000
    for i in range(stack_num):
        key = 'generated_description{}'.format(i)
        score = x.evaluate(live=True, cand={key: cands[key]}, ref={key: refs[key]})
        bleu_id.append(i)
        bleu_scores.append(score)
    min_score = min(bleu_scores)
    min_id = bleu_scores.index(min_score)
    for i in range(stack_num, cands_num, 1):
        key = 'generated_description{}'.format(i)
        score = x.evaluate(live=True, cand={key: cands[key]}, ref={key: refs[key]})
        if score>min_score:
            bleu_scores.pop(min_id)
            bleu_id.pop(min_id)
            bleu_scores.append(score)
            bleu_id.append(i)
            min_score = min(bleu_scores)
            min_id = bleu_scores.index(min_score)
    print(bleu_id, bleu_scores)
    for ids in bleu_id:
        key = 'generated_description{}'.format(ids)
        with open('./results/single_top_{}.txt'.format(stack_num), 'a+') as f:
            f.writelines(cands[key])
            f.writelines('\n')
    random_ids = random.sample(range(0,cands_num), stack_num)
    for ids in random_ids:
        key = 'generated_description{}'.format(ids)
        with open('./results/single_random_gt_{}.txt'.format(stack_num), 'a+') as f:
            f.writelines(refs[key])
            f.writelines('\n')