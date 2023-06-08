import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

bearer_token = os.getenv('NOTION_SECRET')
headers = {
        "Authorization": "Bearer " + bearer_token,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

# Getting a specific Notion page that will be used to write blocks to.
def get_page():
    page_id = 'c6a7075059f9406fafcca99eb3ebd622'
    url = "https://api.notion.com/v1/pages/{}".format(page_id)
    response = requests.get(url, headers=headers)
    print(response.text)

# Getting a specific notion block from a page.
def get_block():
    block_id = '8ac44d123340434d8ae82efc0d71703e'
    child_url = "https://api.notion.com/v1/blocks/{}/children?page_size=100".format(block_id)
    child_response = requests.get(child_url, headers=headers)
    print(child_response.text)

# Perform a search in Notion for a page.
def search_page():
    url = "https://api.notion.com/v1/search"
    # payload = {"filter": {"object": 'page', 'property': 'page'}}
    payload = {"query": 'Test 2'}
    response = requests.post(url, json=payload, headers=headers)
    print(response.text)

# Create a Notion page for playlist items.
def create_playlist_page():
    url = "https://api.notion.com/v1/pages"
    new_pages_added = []

    payload = {
        "parent": {
            "type": "page_id", 
            "page_id": 'ef12820b3e26484faf5ecf1e44c8bc7c'
        },
        "properties": {
            "title": [
                {
                    "text": {
                        "content": "Test 2"
                    }
                }
            ]
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    clean_json = response.json()
    new_page_id = clean_json['id']
    print(response.text)
    print("New Page ID:", new_page_id)

# Adding blocks to a Notion page.
def add_blocks_to_page():
    page_id = 'c6a7075059f9406fafcca99eb3ebd622'
    url = 'https://api.notion.com/v1/blocks/{}/children'.format(page_id)
    print(url)
    with open('n_payload.json', 'r') as payl:
        third_payload = json.load(payl)
    response = requests.patch(url, json=third_payload, headers=headers)
    print(response.text)

def enter_details_to_block():
    video_list = []
    with open('n_payload.json', 'r'):
        for v in video_list:
            video_name = v.snippet.title
            channel_id = v.snippet.channelId
            thumbnail_image = v.snippet.thumbnails.medium.url
            description = v.snippet.description

# Get response from Youtube API and add to Notion block
def get_yt_response_values():
    print("hi")
    block_id = 'f053669b068a47799041ad0d7f6b437e'
    url = 'https://api.notion.com/v1/blocks/{}/children'.format(block_id)

    with open('single_response_yt.json', 'r') as vid:
        video_details = json.load(vid)
        # notion_template = json.load('n_payload.json')
        for i in video_details['items']:
            print("Getting metadata from Youtube response for " + i['etag'])
            video_name = i['snippet']['title']
            channel_name =  i['snippet']['videoOwnerChannelTitle']
            thumbnail_image = i['snippet']['thumbnails']['medium']['url']
            description = i['snippet']['description']
            published_at = i['snippet']['publishedAt']
            video_id = i['contentDetails']['videoId']
            print('Success: ' + i['etag'])
            print('Sending to Notion...')
            update_new_block = {
                "children": [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": "videoOwnerChannelTitle = " + channel_name,
                                    },
                                    "annotations": {
                                        "code": True,
                                    },
                                    "plain_text": "videoOwnerChannelTitle = " + channel_name,
                                    "href": None,
                                }
                            ]
                        }
                    }
                ]
            }
            # yield(video_name, channel_id, thumbnail_image, description, published_at, video_id)
            response = requests.patch(url, json=update_new_block, headers=headers)
            print(response.text)
            print('Successfully added to Notion block: ' + i['etag'])
        vid.close()

    # instance_channel_id = 'f053669b'
    # channel_id = 'ChannelID = ' + instance_channel_id
    # published_at = 'Test Published At'
    # video_id = 'Test Video ID'
    # video_owner_channel_title = 'Test Video Owner Channel Title'

def get_yt_response_values_two():
    with open('single_response_yt.json', 'r') as vid:
        video_details = json.load(vid)
        print("Name: " + video_details['snippet']['title'])
        print("Channel Name: " + video_details['snippet']['videoOwnerChannelTitle'])
        print("Thumbnail URL: " + video_details['snippet']['thumbnails']['medium']['url'])


if __name__ == '__main__':
    get_yt_response_values()