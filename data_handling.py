from peewee import *
import datetime
from playhouse.migrate import *
from notion import get_page

db = SqliteDatabase('ytnotion.db')

class BaseModel(Model):
    class Meta:
        database = db

class PlaylistItem(BaseModel):
    title = CharField()
    date_added = DateTimeField()
    etag = CharField()
    youtube_id = CharField()
    channel_id = CharField()
    description = TextField()
    thumbnail = CharField()
    playlistId = CharField()
    videoPublishedAt = CharField()
    videoOwnerChannelTitle = CharField()
    videoOwnerChannelId = CharField()
    added_to_notion = BooleanField(default=False)

# Function to add Youtube API responses to SQLite database.
def responses_to_db(response):
    for i in response['items']:
        if i['snippet']['title'] == 'Private video':
            print('Private video, skipping...')
            break
        elif i['snippet']['title'] == 'Deleted video':
            print('Deleted video, skipping...')
            break
        else:
            print(i['id'])
            try:
                PlaylistItem.get_or_create(
                    title = i['snippet']['title'],
                    etag = i['etag'],
                    youtube_id = i['id'],
                    channel_id = i['snippet']['channelId'],
                    description = i['snippet']['description'],
                    thumbnail = i['snippet']['thumbnails']['medium']['url'],
                    playlistId = i['snippet']['playlistId'],
                    videoPublishedAt = i['snippet']['publishedAt'],
                    videoOwnerChannelTitle = i['snippet']['videoOwnerChannelTitle'],
                    videoOwnerChannelId = i['snippet']['videoOwnerChannelId'],
                    defaults={'date_added': datetime.datetime.now(), 'added_to_notion': False}
                )
                print('Success adding playlist item to database!')
                return
            except Exception as e:
                print('Error adding playlist item to database... ' + str(e))
                break

# Helper function used to create SQLite database table.
def create_tables():
    with db:
        db.create_tables([PlaylistItem])

# Helper function used to add a column to the database.
def add_column_to_db():
    db = SqliteDatabase('ytnotion.db')
    migrator = SqliteMigrator(db)
    date_added = DateTimeField(default=datetime.datetime.now())
    added_to_notion = BooleanField(default=False)

    migrate(
        migrator.add_column('playlistItem', 'added_to_notion', added_to_notion),
    )

def close_db():
    return db.close()

if __name__ == '__main__':
    responses_to_db()