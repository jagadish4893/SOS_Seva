import pandas as pd
import os
from sent2vec.vectorizer import Vectorizer
import re
import numpy as np
from scipy import spatial
from informer.models import tweet
import pandas as pd
from nltk.tokenize import wordpunct_tokenize
from searchtweets import ResultStream, gen_rule_payload, load_credentials, collect_results
vectorizer = Vectorizer()
os.environ['SEARCHTWEETS_CONSUMER_KEY'] = "****************************"
os.environ['SEARCHTWEETS_CONSUMER_SECRET'] = "********************************"
os.environ['SEARCHTWEETS_ENDPOINT'] = "https://api.twitter.com/1.1/tweets/search/30day/stage.json"
#os.environ['SEARCHTWEETS_ENDPOINT'] = "https://api.twitter.com/1.1/tweets/search/fullarchive/dev.json"
os.environ['SEARCHTWEETS_BEARER_TOKEN'] = "AAAAAAAAAAAAAAAAAAAAALM%2F8gAAAAAA*********************MEeMK"
premium_search_args = load_credentials(account_type="premium",
                env_overwrite=False)
city_list_data = pd.read_csv("informer/CityList.csv")
data_city_list = list(city_list_data['cities'])

def tweet_df(searchString):
    tweet_text, place, date_tweet, label = [], [], [], []
    rule = gen_rule_payload(searchString, results_per_call=100)
    rs = ResultStream(rule_payload=rule,
                  max_results=100,
                  **premium_search_args)
    tweets = list(rs.stream())
    pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    for tweet in tweets:
        try:
            location = tweet['user']['location'].lower()
            location = location.split(",")[0].strip()
            if location in data_city_list:
                tweet_text_val = tweet.all_text
                print(tweet_text_val)
                clean_text = pattern.sub(' ', tweet_text_val)
                vectorizer.bert(clean_text)
                vectors = vectorizer.vectors
                tweet_text.append(tweet_text_val)
                place.append(location)
                date_tweet.append(tweet.created_at_datetime)
        #            label_val = classifier(tweet_text_val)
                label.append(np.mean(vectors,axis=0))
        except Exception as e:
            print("Error {}".format(str(e)))
    df = pd.DataFrame({"tweet":tweet_text,"place":place,"date":date_tweet, "Vectors":label})
    return df


def final_data():
    searches = ['remdesivir','oxygen','beds']
    data = pd.DataFrame()
    for i in searches:
        df = tweet_df(i)
        data = data.append(df,ignore_index=True)
    return data


def ques_vect(ques):
    pattern = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    clean_text = re.sub(pattern,'', ques)
    vectorizer.bert(ques)
    vectors = vectorizer.vectors
    return np.asarray(np.mean(vectors,axis=0),dtype=float)


def similarity(ques,data):
    ques_vec = ques_vect(ques)
    similarity = []
    for i in range(len(data)):
        data_labels = [float(x.replace("[","").replace("]","")) for x in data[i]['label'].split()]
        similarity.append([i,spatial.distance.cosine(np.array(data_labels,dtype=float), ques_vec)])
    val = sorted(similarity,key = lambda x:x[1], reverse=True)
    #print(val)
    #tweet_text = [data[val[i][0]]['text'] for i in range(5)]
    tweet_text = []
    for i in range(20):
        text = wordpunct_tokenize(data[val[i][0]]['text'])
        for j in range(len(text)):
            word = text[j].lower().strip()
            if word in data_city_list:
                text[j] = "<b><mark>" + text[j] + "</mark></b>"
        tweet_text.append(' '.join(text))
    return tweet_text
