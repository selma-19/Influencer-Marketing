import json
import httpx
import jmespath
from bs4 import BeautifulSoup
import requests
import mongo

client = httpx.Client(
    headers={
        # this is internal ID of an instegram backend app. It doesn't change often.
        "x-ig-app-id": "936619743392459",
        # use browser-like features
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "*/*",
    }
)

def parse_user(data) :
    """Parse instagram user's hidden web dataset for user's data"""
    result = jmespath.search(
        """{
        name: full_name,
        username: username,
        id: id,
        category: category_name,
        business_category: business_category_name,
        phone: business_phone_number,
        email: business_email,
        bio: biography,
        bio_links: bio_links[].url,
        homepage: external_url,        
        followers: edge_followed_by.count,
        follows: edge_follow.count,
        facebook_id: fbid,
        is_private: is_private,
        is_verified: is_verified,
        profile_image: profile_pic_url_hd,
        video_count: edge_felix_video_timeline.count,
        videos: edge_felix_video_timeline.edges[].node.{
            id: id, 
            title: title,
            shortcode: shortcode,
            thumb: display_url,
            url: video_url,
            views: video_view_count,
            tagged: edge_media_to_tagged_user.edges[].node.user.username,
            captions: edge_media_to_caption.edges[].node.text,
            comments_count: edge_media_to_comment.count,
            comments_disabled: comments_disabled,
            taken_at: taken_at_timestamp,
            likes: edge_liked_by.count,
            location: location.name,
            duration: video_duration
        },
        image_count: edge_owner_to_timeline_media.count,
        images: edge_felix_video_timeline.edges[].node.{
            id: id, 
            title: title,
            shortcode: shortcode,
            src: display_url,
            url: video_url,
            views: video_view_count,
            tagged: edge_media_to_tagged_user.edges[].node.user.username,
            captions: edge_media_to_caption.edges[].node.text,
            comments_count: edge_media_to_comment.count,
            comments_disabled: comments_disabled,
            taken_at: taken_at_timestamp,
            likes: edge_liked_by.count,
            location: location.name,
            accesibility_caption: accessibility_caption,
            duration: video_duration
        },
        saved_count: edge_saved_media.count,
        collections_count: edge_saved_media.count,
        related_profiles: edge_related_profiles.edges[].node.username
    }""",
        data,
    )
    return result

def scrape_user(username: str):
    """Scrape Instagram user's data"""
    result = client.get(
        f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}",
    )
    print(result)
    data = json.loads(result.content)
    return data["data"]["user"]

def scrape_for_influencers():
    influencers=[]
    for nb_pages in range(15):
        url="https://www.influenceurs.tn/?page="+str(nb_pages+1)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        div_tags = soup.find_all('div', class_='isotope-item')
        for div_tag in div_tags:
            a_tag = div_tag.find('a')
            href=a_tag["href"]
            uri=href[0:44]
            length_url=len(href)
            username=href[44:length_url]
            influencers.append(username)
    print(influencers)

def write_data(file,data):
    with open(file,"a",encoding="utf-8") as f:
        json.dump(data,f,indent=4)

def load_data(file):
    with open(file,"r",encoding="utf-8") as f:
        data=json.load(f)
    return data

influencers=load_data("influencers.json")['influencers_list']
for i in range(536,536+30):
    influencer_info=parse_user(scrape_user(influencers[i]))
    write_data("scraped-data.txt",influencer_info)

if __name__ == '__main__':
    user=input()
    print(scrape_user(user))

