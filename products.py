import json
import os

def config():
    directory = os.getcwd()
    f = open(directory + "/sentinel5P.json")
    config = json.load(f)
    f.close()

    return config

# get product to select dataset
def product_config(product):

    result = None
    pc = None

    if (product == 'CO'):
        result = 'L2__CO____'
    elif (product == 'NO2'):
        result = 'L2__NO2___'
    elif (product == 'SO2'):
        result = 'L2__SO2___'
    elif (product == 'CH4'):
        result = 'L2__CH4___'
    elif (product == 'HCHO'):
        result = 'L2__HCHO__'
    elif (product == 'AER_340_388'):
        result = 'L2__AER_AI'
    elif (product == 'AER_354_388'):
        result = 'L2__AER_AI'

    if (product is not None):
        pc = config()["products"][result]

    return result, pc