from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import re
import string
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import pandas as pd
from translation import bing
from translation.exception import TranslateError

tknzrwhu = TweetTokenizer(preserve_case=False, reduce_len=True, strip_handles = False)
tknzr = TweetTokenizer(preserve_case=False, reduce_len=True, strip_handles = True)



def preProcessAllText(serie):
    alltext = ""
    for line in serie:
        frase = ""
        l = ""
        emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
        line = str(emoji_pattern.sub(r'', str(line))) # no emoji
        #try:
        #    line = bing(line, dst='en')
        #except TranslateError:
        #	line = line
        l = line
        pal = tknzrwhu.tokenize(str(l))
        urls = re.compile(r'.http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        line = urls.sub('', str(line))
        pr = ["rt","@","http","https","'s",'...', 'english', 'translation','):', '. .', '..',
         'à', '؟', 'و', 'ं', 'क', 'ग', 'ज', 'ड', 'त', 'थ', 'द', 'न', 'प', 'ब', 'भ', 'म', '…',
          'य', 'र', 'ल', 'व', 'श', 'स', 'ह', 'ा', 'ि', 'ी', 'ु', 'ू', 'े', 'ै', 'ो',
          '्', 'ാ', 'ി', '്', 'ท', 'พ', 'ั', 'ิ', 'ี', 'ื', 'ู', '็', '่', '้', '์', '–', '—', '‘',
          '’', '“', '”', '、', '。', '「', '」', '【', '】', 'ﷺ', '️', '！', '（', '）', '🏻', '📰', '',
          '📷', '🔥', '🔴', '😂']
        ht = re.compile(r'http.')
        bar = re.compile(r'//*')
        punctuation = set(string.punctuation)
        stoplist = stopwords.words('english')
        #d = enchant.Dict("en_GB")
        pal = [str(i) for i in pal if i not in pr 
            if i not in stoplist if i not in punctuation
            if not bar.search(i) if not ht.search(i)
            if not i.isdigit()]
        #Dentro tenia tb if d.check(str(i))
        for p in pal:
            frase = frase + " " + p
        line = lemmaSentence(frase)
        alltext = alltext + " " + line
    return alltext

def preProcessSerie(serie):
    listatweets = []
    for line in serie:
        frase = ""
        l = ""
        emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
        line = str(emoji_pattern.sub(r'', str(line))) # no emoji
        #try:
        #    line = bing(line, dst='en')
        #except TranslateError:
        #	line = line
        l = line
        pal = tknzr.tokenize(str(l))
        
        urls = re.compile(r'.http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        line = urls.sub('', str(line))
        pr = ["rt","@","http","https","'s",'...', 'english', 'translation','):', '. .', '..',
         'à', '؟', 'و', 'ं', 'क', 'ग', 'ज', 'ड', 'त', 'थ', 'द', 'न', 'प', 'ब', 'भ', 'म', '…',
          'य', 'र', 'ल', 'व', 'श', 'स', 'ह', 'ा', 'ि', 'ी', 'ु', 'ू', 'े', 'ै', 'ो',
          '्', 'ാ', 'ി', '്', 'ท', 'พ', 'ั', 'ิ', 'ี', 'ื', 'ู', '็', '่', '้', '์', '–', '—', '‘',
          '’', '“', '”', '、', '。', '「', '」', '【', '】', 'ﷺ', '️', '！', '（', '）', '🏻', '📰', '',
          '📷', '🔥', '🔴', '😂']
        ht = re.compile(r'http.')
        bar = re.compile(r'//*')
        punctuation = set(string.punctuation)
        stoplist = stopwords.words('english')
        #d = enchant.Dict("en_GB")
        pal = [str(i) for i in pal if i not in pr 
            if i not in stoplist if i not in punctuation
            if not bar.search(i) if not ht.search(i)
            if not i.isdigit()]
        #Dentro tenia tb if d.check(str(i))
        for p in pal:
            frase = frase + " " + p
        line = lemmaSentence(frase)
        listatweets.append(line)
    return pd.Series(listatweets)



def lemmaSentence(sentence):
    result = ""
    wnl = WordNetLemmatizer()
    poscategory = pos_tag(tknzrwhu.tokenize(sentence))
    for word, tag in poscategory:
        wntag = tag[0].lower()
        wntag = wntag if wntag in ['a','r','n','v'] else None
        if not wntag:
            lemma = word
        else:
            lemma = wnl.lemmatize(word, wntag)
        result = result + " " + lemma
#    print(result)
    return result