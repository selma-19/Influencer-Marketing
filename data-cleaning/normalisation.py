# from unidecode import unidecode
# import services.influencers_sevice as influencers_service
#
# def normalize_text(text):
#     # Convert text to lowercase
#     text_lower = text.lower()
#     # Remove accents using unidecode
#     text_normalized = unidecode(text_lower)
#     return text_normalized
#
# influencers = influencers_service.get_influencers()
#
#
# def normalize_captions(influencer, post_type):
#     posts = influencer.get(post_type, [])
#     updated_posts = []
#     for post in posts:
#         captions = post.get('captions', [])
#         normalized_captions = []
#         for caption in captions:
#             normalized_caption = normalize_text(caption)
#             print(normalized_caption)
#             normalized_captions.append(normalized_caption)
#             post['captions'] = normalized_captions
#             updated_posts.append(post)
#             influencers_service.update_influencer(influencer, post_type, updated_posts)
#
#
# def normalize_titles(influencer, post_type, ):
#     posts = influencer.get(post_type, [])
#     updated_posts = []
#     for post in posts:
#         title = post.get('title')
#         normalized_title = normalize_text(title)
#         print(normalized_title)
#         post['title'] = normalized_title
#         updated_posts.append(post)
#         influencers_service.update_influencer(influencer, post_type, updated_posts)
#
#
# def normalize_bio(influencer):
#     bio = influencer.get('bio')
#     if bio is not None:
#         normalized_bio = normalize_text(bio)
#         print(normalized_bio)
#         influencers_service.update_influencer(influencer, 'bio', normalized_bio)
#
#
# for influencer in influencers:
#     normalize_bio(influencer)
#     normalize_titles(influencer, 'images')
#     normalize_titles(influencer, 'videos')
#     normalize_captions(influencer, 'images')
#     normalize_captions(influencer, 'videos')
