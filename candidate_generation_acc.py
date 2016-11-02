import os
import sys
import unicodedata
import shelve

class CandidateRecall():
  def __init__(self, shelve_dict_file):
    self.shelve_dict_file = shelve_dict_file


  def open_shelve(self):
    self.map = shelve.open(filename=self.shelve_dict_file,
                           writeback=False)

  def close_shelve(self):
    self.map.close()

  def _getLnrm(self, arg):
    """Normalizes the given arg by stripping it of diacritics, lowercasing, and
    removing all non-alphanumeric characters.
    """
    arg = ''.join([
      c for c in unicodedata.normalize('NFD', arg)
      if unicodedata.category(c) != 'Mn'
    ])
    arg = arg.lower()
    arg = ''.join([
      c for c in arg
      if c in set('abcdefghijklmnopqrstuvwxyz0123456789')
    ])
    return arg

  def getCandidates(self, arg, threshold=None):
    mention = self._getLnrm(arg)
    if mention in self.map:
      candidates = self.map[mention]
    else:
      candidates = ()
    if threshold != None and threshold > 0:
      return candidates[0:threshold]
    else:
      return candidates

  def getMentionAndGoldWids(self, mentions_file):
    assert os.path.exists(mentions_file), "Mentions file does not exist"
    f = open(mentions_file, 'r')
    wids = []
    mentions = []
    mention_lines = f.readlines()
    for mention in mention_lines:
      m_split = mention.split("\t")
      wid = m_split[1].strip()
      surface = m_split[2].strip()
      mentions.append(surface)
      wids.append(wid)
    #endfor
    return wids, mentions

  def getCandidateRecall(self, mentions_file, threshold=None):
    wids, mentions = self.getMentionAndGoldWids(mentions_file)
    recall = 0
    for i in range(0, len(mentions)):
      candidates = self.getCandidates(mentions[i], threshold)
      candidate_wids = [c[0] for c in candidates]
      if wids[i] in candidate_wids:
        recall += 1
      else:
        print(mentions[i] + " " + wids[i])
    #endfor
    recall = float(recall)/len(mentions)
    if threshold == None:
      threshold = sys.maxsize
    print("Recall at threshold %d is %2.4f" % (threshold, recall))

if __name__ == "__main__":
  cwikis = CandidateRecall(shelve_dict_file="/save/ngupta19/crosswikis/crosswikis.dict")
  cwikis.open_shelve()

  cwikis.getCandidateRecall(mentions_file="/save/ngupta19/datasets/ACE/mentions.txt",
                            threshold=30)

  cwikis.close_shelve()






