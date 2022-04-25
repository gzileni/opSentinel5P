import logging
import os
import datetime

from flask import Flask, request, json
from products import config, product_config
from core import postgis, copernicus

from werkzeug.exceptions import HTTPException

app = Flask(__name__)

rootpath = os.path.abspath(os.getcwd()) + '/logs'
if (not os.path.isdir(rootpath)):
    os.mkdir(rootpath)

logging.basicConfig(filename=rootpath + '/sentinel5P.log',
                    encoding='utf-8', level=logging.DEBUG)

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

# ----------------------------------------------------------------
# get geojson from intersect geometry
# GET /sentinel5p/<string:product>/<int:code>/<float:lat>/<float:lng>
@app.route('/s5p/<string:product>/<lat>/<lng>/<start>/<end>/<meters>', methods=['GET'])
def sentinel5P_geojson(product, lat, lng, start, end, meters):

    product, cfg =  product_config(product)
    
    params = {
        "product": product,
        "config": cfg,
        "crs": 4326,
        "lat": lat,
        "lng": lng,
        "start": start,
        "end": end,
        "meters": int(meters)
    }

    if None not in (product, lat, lng, start, end, meters):
        return postgis.get_json(params)
    else:
        return {
            "error": "Can't parameters [product, lat, lng, start, end, meters] are None "
        }

# ----------------------------------------------------------------
# POST /sentinel5P 
@app.route('/s5p/job', methods=['POST'])
def sentinel5P():

    print('hello')
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        
        body = request.json
        
        if None not in (body["product"], 
                        body["bbox"]):
            start = 0
            end = False

            response = {
                "status": [],
                "error": [],
                "links": []
            }

            cfg = config()
            
            product, pconfig =  product_config(body["product"])
            print(pconfig)
            bbox = (float(body["bbox"][1]), float(body["bbox"][0]),
                    float(body["bbox"][3]), float(body["bbox"][2]))
            range = copernicus.range(cfg["days"])

            while end==False:
                
                url = 'https://' + cfg["url"] + \
                    '/dhus/search?start=' + str(start) + '&rows=100&q=' + range + \
                    ' AND platformname:Sentinel-5 Precursor' + \
                    ' AND producttype:' + product + \
                    ' AND ' + copernicus.footprint(bbox)

                logging.info(str(datetime.datetime.now()) + ' - get datasets from ' + url)

                params = {
                    "url": url,
                    "username": cfg["username"],
                    "password": cfg["password"],
                    "bbox": bbox,
                    "product": product,
                    "platform": cfg["platform"],
                    "description": pconfig["description"],
                    "crs": cfg["crs"]
                }

                print(params)

                # get url datasets
                result = copernicus.datasets(params)

                response["status"].append(result["status"])
                response["error"].append(result["error"])
                response["links"].append(result["datasets"])

                if (len(result["datasets"]) > 0):
                    start += 101
                else:
                    end = True
            
            return response
        else:
            return {
                "error": "parameters [product, bbox] are not None "
            }
    else:
        return {
            "error" : 'Content-Type not supported!'
        }


    