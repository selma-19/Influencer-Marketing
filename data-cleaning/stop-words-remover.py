import nltk
from nltk.corpus import stopwords

import services.influencers_sevice as influencers_service

nltk.download('stopwords')

stopwords_en = stopwords.words('english')
influencers = influencers_service.get_influencers()


# Fonction pour supprimer les stopwords d'un texte
def remove_stopwords(text, stopwords_list):
    words = text.split()
    words = [word for word in words if word not in stopwords_list]
    return ' '.join(words)


def remove_captions_stopwords(influencer, post_type):
    posts = influencer.get(post_type, [])
    updated_posts = []
    for post in posts:
        captions = post.get('captions', [])
        no_stopwords_captions = []
        for caption in captions:
            try:
                no_stopwords_caption = remove_stopwords(caption, stopwords_en)
            except Exception as e:
                print(f"An exception occurred: {e}. Skipping this caption.")
                continue
            print(no_stopwords_caption)
            no_stopwords_captions.append(no_stopwords_caption)
            post['captions'] = no_stopwords_captions
            updated_posts.append(post)
        influencers_service.update_influencer(influencer, post_type, updated_posts)


def remove_title_stopwords(influencer, post_type):
    posts = influencer.get(post_type, [])
    updated_posts = []
    for post in posts:
        title = post.get('title')
        try:
            no_stopwords_title = remove_stopwords(title, stopwords_en)
        except Exception as e:
            print(f"An exception occurred: {e}. Skipping this caption.")
            continue
        print(no_stopwords_title)
        post['title'] = no_stopwords_title
        updated_posts.append(post)
        influencers_service.update_influencer(influencer, post_type, updated_posts)


for influencer in influencers:
    # remove from bio bio
    bio = influencer.get('bio')
    no_stopwords_bio = remove_stopwords(bio, stopwords_en)
    influencers_service.update_influencer(influencer, 'bio', no_stopwords_bio)
    # Supprimer les stopwords des profils
    remove_title_stopwords(influencer, 'videos')
    remove_title_stopwords(influencer, 'images')
    remove_captions_stopwords(influencer, 'images')
    remove_captions_stopwords(influencer, 'images')
