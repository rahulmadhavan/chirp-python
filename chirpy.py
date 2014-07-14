from flask import Flask
from chirp_manager import ChirpManager
import sys
import json

app = Flask("Chirpy")


cm = ChirpManager(sys.argv[1],sys.argv[2],'http','chirp.org')

@app.route('/')
def index():
    return "Chirp !!!"

@app.route('/chirper')
def chirper():
    return json.dumps(cm.details())

@app.route('/chirpers')
def chirpers():
    return json.dumps(cm.chirpers)

@app.route('/chirper/names')
def chirper_names():
    return json.dumps(cm.list_chirpers())

@app.route('/chirper/<chirper_name>')
def fetch_chirper(chirper_name):
    chirper = cm.fetch(chirper_name)
    if chirper != False:
        return json.dumps(chirper)
    else:
        return "chirper not found", 404




if __name__ == '__main__':
    cm.start_chirping()
    app.run(port=int(sys.argv[2]))



