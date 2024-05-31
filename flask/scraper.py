import json

import httpx

client = httpx.Client(headers={  # this is internal ID of an instegram backend app. It doesn't change often.
    "x-ig-app-id": "936619743392459",  # use browser-like features
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,ru;q=0.8", "Accept-Encoding": "gzip, deflate, br", "Accept": "*/*", })


def scrape_user(username: str):
    """Scrape Instagram user's data"""
    try:
        result = client.get(f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}", )
        result.raise_for_status()  # Raise an error for bad responses
    except httpx.RequestError as e:
        return f"An error occurred while making the request: {e}"
    except httpx.HTTPStatusError as e:
        return f"An error occurred due to the response status: {e}"

    try:
        data = json.loads(result.content)
    except (json.JSONDecodeError, KeyError) as e:
        return f"Error parsing JSON: {e}"

    return data
