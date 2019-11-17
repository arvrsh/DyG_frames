#!/root/dyg/fenv/bin/python
import facebook
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv(verbose=True)
access_token = os.getenv('FB_TOKEN')
page_id = os.getenv('FB_PAGE_ID')
folder = os.getenv('VID_FOLDER')
graph = facebook.GraphAPI(access_token, version="4.0")
data = None

def load_data():
    with open('data.json','r') as jsonfile:
        data = json.load(jsonfile)
    return data

def check_disponibilidad(data):
    return data['disponible']

def update_disponibilidad(data):
    if data['save_data']['season'] > len(data['seasons']):
        return False
    else:
        print(data)
        return True
    pass 

def next_frame(data):
    ndata = data
    if data['save_data']['frame'] + 1 > get_frame_count(data['save_data']):
        # hay que inicicar el siguiente cap y reiniciar los frames
        ndata['save_data']['episode'] += 1
        if ndata['save_data']['episode'] > get_episode_count(data):
            ndata['save_data']['season'] += 1
            ndata['save_data']['episode'] = 1
            ndata['disponible'] = update_disponibilidad(ndata)
        ndata['save_data']['frame'] = 1
    else:
        # seguir como si nada lol 
        ndata['save_data']['frame'] += 1
    save_data(ndata)
    pass

def save_data(data):
    with open('data.json','w') as f:
        json.dump(data, f)
    pass

def get_episode_frame(data):
    string = "vid/"+str(data['season'])+"/"+str(data['episode'])+"/"+str(data['frame']).rjust(4,'0')+".jpg"
    # string = "vid/"+str(data['season'])+"/"+str(data['episode'])+"/0505.jpg"
    return string

def get_episode_count(data):
    season = data['seasons'][data['save_data']['season']-1]['episodes']
    return season

def get_frame_count(data):
    files = os.listdir("vid/"+str(data['season'])+"/"+str(data['episode']))
    return len(files)

def post_frame(data):
    # do something 
    ndata = data['save_data']
    message = "Temporada: " + str(ndata['season'])
    message += " - Episodio: " + data['seasons'][ndata['season']-1]['episode'][ndata['episode']-1]
    message += " - Frame " + str(ndata['frame']) + "/"+ str(get_frame_count(ndata))
    try:
        frame = get_episode_frame(ndata)
        # graph.put_photo(image = open(frame,'rb'), message = message)
        print("[!] " + message)
        # recibe la data original...!! 
        next_frame(data)
    except Exception as ex:
        print("[X]", ex)

if __name__ == "__main__":
    data = load_data()
    if(check_disponibilidad(data)):
        print("[D] ", datetime.now())
        post_frame(data)
    else:
        print("[!] No hay más temporadas - episodios :(")
    pass


