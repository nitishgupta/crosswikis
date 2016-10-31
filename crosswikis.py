import os
import sys
import unicodedata
import shelve

class CrossWikis():
  def __init__(self, shelve_dict_file):
    self.shelve_dict_file = shelve_dict_file

  def load_widWikiTitle(self):
    print("[#] Making WikiTitle -> Wid map ... ")
    wikiTitle_WID = {}
    f = open(widWikiTitle_fname, 'r')
    line = f.readline()
    while line != "":
      split = line.split("\t")
      wid = split[0].strip()
      wTitle = split[1].strip()
      wikiTitle_WID[wTitle] = wid
      line = f.readline()
    #enddef
    print(" [#] Number of wTitles read : %d" % len(wikiTitle_WID))
    return wikiTitle_WID


  def open_shelve(self, writeback):
    self.map = shelve.open(filename=self.shelve_dict_file,
                           writeback=writeback)

  def close_shelve(self):
    self.map.close()


  def makeShelveMap(self, crosswikisfile, widWikiTitle_fname):
    self.wikiTitle_WID = self.load_widWikiTitle()
    print("[#] Making CrossWikis Shelve file")
    assert not os.path.exists(self.shelve_dict_file), "Dict already exists"
    d = shelve.open(filename=self.shelve_dict_file, writeback=True)
    f = open(crosswikisfile, 'r', encoding='utf-8')
    line = f.readline()
    lines_written = 0
    mentions_written = 0
    titles_found = 0
    failed_lines = 0
    leg_line = True

    while line != "":
      split = line.split("\t")
      if len(split) >= 2:
        mention = split[0].strip()
        cprob_title = split[1].strip().split(" ")
        cprob = cprob_title[0].strip()
        title = cprob_title[1].strip()
        if title in self.wikiTitle_WID:
          titles_found += 1
          if mention not in d:
            mentions_written += 1
            d[mention] = []
          d[mention].append((self.wikiTitle_WID[title], cprob))
        lines_written += 1
      leg_line = False
      while not leg_line:
        try:
          line = f.readline()
          leg_line = True
        except UnicodeDecodeError:
          failed_lines += 1
      if lines_written % 100000 == 0:
        d.sync()
        print(str(lines_written) + " ... ", end="", flush=True)
    #endwhile
    print("Number of mentions written : %d" % mentions_written)
    print("Number of titles written / value entries : %d" % titles_found)
    d.close()

  def print_shelve(self):
    d = shelve.open(filename=self.shelve_dict_file, writeback=False)
    for key in d:
      print(key)
      print(d[key])
    d.close()


  def getCandidates(self, arg):
    mention = self.getLnrm(arg)
    if mention in self.map:
      candidates = self.map[mention]
    else:
      candidates = ()
    return candidates





  def getLnrm(self, arg):
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

if __name__ == "__main__":
  cwikis = CrossWikis(shelve_dict_file="/save/ngupta19/crosswikis/crosswikis.dict")
  #cwikis.makeShelveMap(crosswikisfile="/save/ngupta19/crosswikis/data/lnrm.dict",
  #                     widWikiTitle_fname="/save/ngupta19/freebase/types_pruned/wid.WikiTitle")
  cwikis.open_shelve(writeback=False)

  candidates = cwikis.getCandidates("Taiwan")
  print(candidates[0:30])
  cwikis.close_shelve()






