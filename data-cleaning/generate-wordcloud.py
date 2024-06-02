import os

from matplotlib import pyplot as plt
from wordcloud import WordCloud, STOPWORDS

os.environ['NUMEXPR_MAX_THREADS'] = '12'


from services.influencers_service import InfluencersService
from shared.mongo import MongoConnection
mongo_connection = MongoConnection()
influencers_service = InfluencersService(mongo_connection)
posts = influencers_service.get_posts()

mongo_connection=MongoConnection()
influencers_service = InfluencersService(mongo_connection)
bios=[]

influencers=influencers_service.get_influencers()
info_string = ""
# for influencer in influencers:
#     if influencer['Bio']!= 'NULL':
#         info_string+=influencer['Bio']
#     if influencer['Category']!= 'NULL':
#         info_string+=influencer['Category']
info_string+=influencers[8]['Bio']+influencers[0]['Category']
custom_stopwords = set(STOPWORDS)
custom_stopwords.update(['away','might','look','every','never','new','null',
                         'like','com','www','gmail','hotmail','creator','celebritie','creators',
                        'celebrities','contact','make','follow',
                         'DM','e','de','Content','collab','hello','thing','next','com','Creators','S','info','comCreators','General','email','NYC','LA','Bmogger','blogger','Good'
                         ])
wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=100, stopwords=custom_stopwords, colormap='viridis').generate(info_string)

# Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
wordcloud.to_file('wordcloud.png')
