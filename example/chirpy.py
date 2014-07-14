###############################################
#
#   example uses flask web framework
#
#   setup flask to run the example,
#
#   pip install flask OR easy_install flask
#
##############################################

import sys
import json
import logging

from flask import Flask

from chirp.chirp_manager import ChirpManager


app = Flask("Chirpy")


## initialising the chirp manager
cm = ChirpManager(sys.argv[1],sys.argv[2],'http','chirp.org')


@app.route('/')
def index():
    return "Chirp !!!"

## retrieve details of the current chirper

@app.route('/chirper')
def chirper():
    return json.dumps(cm.details())

## retrieve details of all the chirpers on the network


@app.route('/chirpers')
def chirpers():
    return json.dumps(cm.chirpers)

## retrieve names of all the chirpers on the network

@app.route('/chirper/names')
def chirper_names():
    return json.dumps(cm.list_chirpers())

## retrieve detail of the chirpers specified

@app.route('/chirper/<chirper_name>')
def fetch_chirper(chirper_name):
    chirper = cm.fetch(chirper_name)
    if chirper != False:
        return json.dumps(chirper)
    else:
        return "chirper not found", 404




if __name__ == '__main__':
    logging.basicConfig(filename = sys.argv[1]+'.log',level=logging.DEBUG)

    ## start the chirp manager
    cm.start_chirping()


    app.run(port=int(sys.argv[2]))



