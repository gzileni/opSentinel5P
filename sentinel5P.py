from flask import Flask

from products import get_config
from core import postgis

app = Flask(__name__)

# ----------------------------------------------------------------
# get geojson from intersect geometry
# GET /sentinel5p/<string:product>/<int:code>/<float:lat>/<float:lng>
@app.route('/s5p/<string:product>/<lat>/<lng>/<start>/<end>/<meters>', methods=['GET'])
def sentinel5P_geojson(product, lat, lng, start, end, meters):

    product, config =  get_config(product)
    
    params = {
        "product": product,
        "config": config,
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
