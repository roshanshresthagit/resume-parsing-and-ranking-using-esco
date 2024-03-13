from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pickle
from skillenrichment import enrich
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


class jd_profile_comparison:
    def __init__(self):
        self.setofStopWords = set(stopwords.words('english') + ['``', "''"])


    def __cleanResume(self, resumeText):
        resumeText = re.sub('http\S+\s*', ' ', resumeText)  # remove URLs
        resumeText = re.sub('RT|cc', ' ', resumeText)  # remove RT and cc
        resumeText = re.sub('#\S+', '', resumeText)  # remove hashtags
        resumeText = re.sub('@\S+', '  ', resumeText)  # remove mentions
        resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ',
                            resumeText)  # remove punctuations
        resumeText = re.sub(r'[^\x00-\x7f]', r' ', resumeText)
        resumeText = re.sub('\s+', ' ', resumeText)  # remove extra whitespace
        resumeText = resumeText.lower()  # convert to lowercase
        resumeTextTokens = word_tokenize(resumeText)  # tokenize
        filteredText = [w for w in resumeTextTokens if not w in self.setofStopWords]  # remove stopwords
        return ' '.join(filteredText)

    def __matcher(self, job_desc, resume_text):
        cjobdesc= self.__cleanResume(job_desc)
        print(cjobdesc)
        jskill=set(cjobdesc.split())
        ljskill = list(jskill)
        print("============= jd skillset===========")
        print(ljskill)
        enriched_jskills = enrich(ljskill)
        print('=============enriched jd==========')
        print(enriched_jskills)
        en_jskills =' '.join(enriched_jskills)
        #for resume text
        cresume = self.__cleanResume(resume_text)
        print(cresume)
        rskill = set(cresume.split())
        rjskill = list(rskill)
        print("============= resume skillset===========")
        print(rjskill)
        enriched_rskills = enrich(rjskill)
        print('=============enriched resume==========')
        print(enriched_rskills)
        en_rskills =' '.join(enriched_rskills)

        text = [en_rskills, en_jskills]
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(text)
        matchper = cosine_similarity(count_matrix)[0][1] * 100
        return round(matchper, 2)

    def match(self, jd, resumetext):
        return self.__matcher(jd, resumetext)


obj_jd_profile_comparison = jd_profile_comparison()
pickle.dump(obj_jd_profile_comparison, open("jd_profile_comparison.pkl", "wb"))