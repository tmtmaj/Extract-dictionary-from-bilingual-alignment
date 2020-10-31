from collections import defaultdict, Counter

class ExtractDict:
  def __init__(self, src_list, tgt_list, align_list, N, n_best = 1):

    if type(align_list) is not list:

      align_f = open(align_list, "r", encoding="utf*")
      align_list = align_f.readlines()
      align_f.close()

      src_f = open(src_list, "r", encoding="utf*")
      src_list = src_f.readlines()
      src_f.close()

      tgt_f= open(tgt_list, "r", encoding="utf*")
      tgt_list = tgt_f.readlines()
      tgt_f.close()

    # src_list: source sentence list (i.e. ['올해 87 차 를 맞은 sc@@ e 수련 회 는 매년 전국 교회 에서 다음 세대 성도 들 이 한자리 에 모이는 여름철 대표 신앙 축제 다 .\n', ..., ])
    # tgt_list: target sentence list (i.e. ['the s@@ ce retreat , which marks its 8@@ 7th anniversary this year , is a major summer religious festival where the next generation of believers gather in churches across the country every year .\n', ..., ])
    # align_list: alignment list (i.e ['23-16 0-12 4-10 22-17 4-6 14-22 11-29 15-23 24-18 5-1 1-9 5-2 1-8 11-31 12-28 10-33 10-32 27-34 4-5 21-20 0-11 16-25 13-27 25-19 7-3 4-7 21-26\n', ..., ])
    # N: the number of words that appear frequently in the source dictionary
    # n_best: the number of corresponding target words of each source word in the dictionary

    self.preproAlign = self.prepro_align(align_list)
    self.tokenSrc = self.tokenizer(src_list)
    self.tokenTgt = self.tokenizer(tgt_list)
    self.lineDict = self.line_dict(self.preproAlign, self.tokenSrc, self.tokenTgt)
    self.aggrCountDict = self.aggregate_count_dict(self.lineDict)
    self.sortDict = self.sort_dict(self.tokenSrc)
    self.topNdict = self.create_top_n_dict(self.sortDict, self.aggrCountDict, N, n_best)


  def prepro_align(self, align_list):
    # input: Pharaoh format bilingual alignment from GIZA++ or fastalign (i.e. ['23-16 0-12 4-10 22-17 4-6 14-22 11-29 15-23 24-1 ...', ...])
    # output: list of tuple (i.e. [[(23, 16), (0, 12), (4, 10), (22, 17), ..., (1, 9), (5, 2)], ..., [(5, 1), (1, 9), (5, 2), ..., (3,4), (32, 3)]])
    output = []
    
    for align in align_list:
        try:
            output.append([tuple(map(int, unit.split("-"))) for unit in align.strip().split(" ")])
        except:
            output.append([(-1000, -1000)]) 
            
    return output  

  def tokenizer(self, input_list): 
    #tokenizer by space
    return [sen.strip().split(' ') for sen in input_list]

  def line_dict(self, prepro_align, src_token, tgt_token):
    # input: 
    # 1. prepro_alignment list (i.e. [[(23, 16), (0, 12), (4, 10), (22, 17), ..., (1, 9), (5, 2)], ..., [(5, 1), (1, 9), (5, 2), ..., (3,4), (32, 3)]])
    # 2. tokenized source sentence list (i.e. [['올해', '87', '차', '를', '맞은', 'sc@@', 'e', '수련', '회', '는', '매년', '전국', '교회', '에서', '다음', '세대', '성도', '들', '이', '한자리', '에', '모이는', '여름철', '대표', '신앙', '축제', '다', '.'], ...] )
    # 3. tokenized target sentence list (i.e. ['the', 's@@', 'ce', 'retreat', ',', 'which', 'marks', 'its', '8@@', '7th', 'anniversary', 'this', 'year', ',', 'is', 'a', 'major', 'summer', 'religious', 'festival', 'where', 'the', 'next', 'generation', 'of', 'believers', 'gather', 'in', 'churches', 'across', 'the', 'country', 'every', 'year', '.'], ...] )
    # output: list of per-line dictionary (i.e. [defaultdict(list, {'.': ['.'], '87': ['7th', '8@@'], 'sc@@': ['s@@', 'ce'], ...}), ..., defaultdict...] )
    line_dict = []

    for a, s, t in zip(prepro_align, src_token, tgt_token):
      align_list = [(s[a_[0]], t[a_[1]]) for a_ in a if a_[0] != -1000] #만약 set이나 list를 바로 dict으로 바꿔버리면 한 key에 대한 여러개의 values 중 하나만 뺴고 다 사라짐 
      temp_dict = defaultdict(list)
      for (key, val) in align_list:
        if val not in temp_dict[key]:
          temp_dict[key].append(val) 
      line_dict.append(temp_dict)

    return line_dict

  def aggregate_count_dict(self, line_dict):

    aggregate_dict = defaultdict(list)
    count_dict = defaultdict(dict)

    for line in line_dict:
      for word in line.items():
        if word[0] not in aggregate_dict:
          aggregate_dict[word[0]] = word[1]
        else:
          aggregate_dict[word[0]] += word[1]

    for elem in aggregate_dict.items():
      count_dict[elem[0]] = [i[0] for i in Counter(elem[1]).most_common()]

    return count_dict


  def sort_dict(self, token_list):
    sort_dict = defaultdict(int)

    for line in token_list:
      for word in line:
        if word in sort_dict:
          sort_dict[word] += 1
        else:
          sort_dict[word] = 1

    return {k:v for k,v in sorted(sort_dict.items(), key = lambda v:v[1], reverse=True)}



  def create_top_n_dict(self, sort_dict, sort_count_dict, N, n_best = 1):

    top_n_dict = defaultdict()

    N_top_list = list(sort_dict.keys())[:N]

    for n in N_top_list:
      try:
        top_n_dict[n] = sort_count_dict[n][:n_best]
      except:
        pass

    return top_n_dict

