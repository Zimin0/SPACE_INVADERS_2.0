import vk_api

login = 'nik.zimenkov.00@inbox.ru'
password = '62050897And'
session = vk_api.VkApi(token = 'f2d1b5321ef9d8f1e0d3a4fb437f864de65a0a101715c3f7669698bd3015e117eaa854f4e6c3d8b7d0140' ) # put your token here login=login, password=password
vk = session.get_api()

TARGET_ID = 150619294 # user id 
ALBUM_ID = 3 # needed album
PUBLIC_ALL_ID = -2 # id of album, where your videos are currently in 
HOW_MANY_VIDEOS = 20 # not more than 200

search = session.method('video.get', {'album_id': PUBLIC_ALL_ID, 'count': HOW_MANY_VIDEOS + 1 }) # finds all your videos and returns 

def replace_loc_video(TARGET_ID, ALBUM_ID, video_id, owner_id):
    stat1 = session.method('video.addToAlbum', {'target_id':TARGET_ID, 'video_id': video_id, 'album_id': ALBUM_ID , 'owner_id': owner_id}) # add to album
    stat2 = session.method("video.removeFromAlbum", {'video_id': video_id, 'owner_id': owner_id, 'target_id': TARGET_ID, 'album_id': PUBLIC_ALL_ID}) # delete from album
    return stat1, stat2

for i in range(0, HOW_MANY_VIDEOS-1):
    video_id = search['items'][i]['id']
    owner_id = search['items'][i]['owner_id']
    try:
        res = replace_loc_video(TARGET_ID, ALBUM_ID, video_id, owner_id)
    except vk_api.exceptions.ApiError:
        continue
    if res != (1,1): # check for issues and errors 
        print("Some kind of a error, check this")
        break
