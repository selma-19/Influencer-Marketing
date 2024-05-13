import services.influencers_service as influencers_service
from unidecode import unidecode

influencers = influencers_service.get_influencers()


def remove_emojis(text):
    return unidecode(text)


def remove_caption_emojis(influencer, post_type):
    posts = influencer.get(post_type, [])
    updated_posts = []
    for post in posts:
        captions = post.get('captions', [])
        no_emoji_captions = []
        for caption in captions:
            try:
                no_emoji_caption = remove_emojis(caption)
            except Exception as e:
                print(f"An exception occurred: {e}. Skipping this caption.")
                continue
            print(no_emoji_caption)
            no_emoji_captions.append(no_emoji_caption)
            post['captions'] = no_emoji_captions
            updated_posts.append(post)
            influencers_service.update_influencer(influencer, post_type, updated_posts)


def remove_title_emojis(influencer, post_type):
    posts = influencer.get(post_type, [])
    updated_posts = []
    for post in posts:
        title = post.get('title')
        try:
            no_emojis_title = remove_emojis(title)
        except Exception as e:
            print(f"An exception occurred: {e}. Skipping this caption.")
            continue
        print(no_emojis_title)
        post['title'] = no_emojis_title
        updated_posts.append(post)
        influencers_service.update_influencer(influencer, post_type, updated_posts)


def remove_bio_emojis(influencer):
    bio = influencer.get('Bio')
    no_emoji_bios = remove_emojis(bio)
    influencers_service.update_influencer(influencer, 'Bio', no_emoji_bios)

def remove_name_emojis(influencer):
    name = influencer.get('Name')
    no_emoji_bios = remove_emojis(name)
    influencers_service.update_influencer(influencer, 'Name', no_emoji_bios)


# remove emojis for influencer profiles

for influencer in influencers:
    remove_name_emojis(influencer)
    remove_bio_emojis(influencer)
    # remove_title_emojis(influencer, 'videos')
    # remove_title_emojis(influencer, 'images')
    # remove_caption_emojis(influencer, 'videos')
    # remove_caption_emojis(influencer, 'images')
