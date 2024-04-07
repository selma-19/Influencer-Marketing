from deep_translator import GoogleTranslator
import services.influencers_sevice as influencers_service

translator = GoogleTranslator(source='auto', target='en')
influencers=influencers_service.get_influencers()

def translate_captions(influencer,post_type):
	posts = influencer.get(post_type, [])
	updated_posts = []
	for post in posts:
		captions = post.get('captions', [])
		translated_captions = []
		for caption in captions:
			try:
				translated_caption = translator.translate(caption)
			except Exception as e:
				print(f"An exception occurred: {e}. Skipping this caption.")
				continue
			print(translated_caption)
			translated_captions.append(translated_caption)
			post['captions'] = translated_captions
			updated_posts.append(post)
		influencers_service.update_influencer(influencer, post_type, updated_posts)

#translate bio and captions
for influencer in influencers:
	#translate bio
	#bio=influencer.get('bio')
	#translated_bio=translator.translate(bio)
	#influencers_service.update_influencer(influencer,'bio',translated_bio)
	#translate post captions
	translate_captions(influencer,'videos')
	translate_captions(influencer,'images')





