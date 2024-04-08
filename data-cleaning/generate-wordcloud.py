import uuid
from wordcloud import WordCloud
import services.influencers_sevice as influencers_service
import os

influencers = influencers_service.get_influencers()

def generate_wordcloud(text,username,foldername):
    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    #create folder structure
    folder_path = os.path.join('wordclouds', username, foldername)
    os.makedirs(folder_path, exist_ok=True)

    unique_id = str(uuid.uuid4())[:8]  # Take the first 8 characters of the UUID
    filename = f'{foldername}_wordcloud_{unique_id}.png'
    #save wordcloud
    wordcloud.to_file(os.path.join(folder_path, filename))


def generate_wordcloud_bio(influencer):
    bio=influencer.get('bio')
    username = influencer.get('username')
    generate_wordcloud(bio,username,'bio')

def generate_wordcloud_captions(influencer, post_type):
    posts = influencer.get(post_type, [])
    captions = []
    for post in posts:
        captions += post.get('captions', [])
        captions_text = ' '.join(captions)

    username = influencer.get('username')
    generate_wordcloud(captions_text,username,'captions')



for influencer in influencers:
    generate_wordcloud_bio(influencer)
    generate_wordcloud_captions(influencer, 'images')
    generate_wordcloud_captions(influencer, 'videos')