import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import re
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

consumer_key = "3II162EiHwgcNCSV17YW0Ykof"
consumer_secret = "CZonbTz3tao9tZkQVVCvQscf5Yml0ohV3H2n16JYktg4bY73z4"
access_token = "1349083645-NoM2NjgwsSqPPrT3DN8PgKMa4VFV8VGpV7qVX1H"
access_token_secret = "wI0pzHELnIIMzTZPLm4Pn7Gj01SVL5zniJaDPM2ZcW6SG"


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

dict_hashtags = {}

class MyListener(StreamListener):
    def on_data(self, data):
        try:
            regex_str = [
                r'<[^>]+>',
                r'(?:@[\w_]+)',
                r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",
                r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',
                r'(?:(?:\d+,?)+(?:\.?\d+)?)',
                r"(?:[a-z][a-z'\-_]+[a-z])",
                r'(?:[\w_]+)',
                r'(?:\S)'
                ]
            tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
            def tokenize(s):
                return tokens_re.findall(s)
            hashtags = [hashtag.lower() for hashtag in tokenize(data) if len(hashtag)>1 and hashtag[0]=="#"]
            for i in hashtags:
                if i not in dict_hashtags:
                    dict_hashtags[i] = [i, 1]
                else:
                    dict_hashtags[i][1] += 1

            df_hashtags =  pd.DataFrame.from_dict(dict_hashtags, orient='index', columns=['hashtag', 'count'])
            df_hashtags = df_hashtags.sort_values(by='count', ascending=False)
            results = df_hashtags.head(5)
            df = results.values.tolist()
            with open('Hashtags.txt', 'w', encoding='utf8') as f:
                f.write(str(df))
                f.close()
            style.use('fivethirtyeight')
            
            fig = plt.figure()
            ax1 = fig.add_subplot(1, 1, 1)

            #print(results)
            def animate(i):
                graph_data = open('Hashtags.txt', 'r').read()
                xs = []
                ys = []
                """for i in list(graph_data):
                    print(i)
                    xs.append(i[0])
                    ys.append(i[1])"""
                ax1.clear()
                ax1.plot(xs, ys)

            ani = animation.FuncAnimation(fig, animate, interval=1000)
                
            plt.show()
                
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
    def on_error(self, status):
        print(status)


if __name__ == "__main__":
    stream = Stream(auth, MyListener())
    stream.filter(track=["#bnk48"])
            
