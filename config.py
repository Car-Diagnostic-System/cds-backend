import os

SECRET_KEY = os.urandom(32)

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'mysql://root:password@127.0.0.1:3366/cds'

# Turn off the Flask-SQLAlchemy event system and warning
SQLALCHEMY_TRACK_MODIFICATIONS = False
JSON_SORT_KEYS = False

CORS_HEADERS = 'Content-Type'

# brands = tuple(set(map(lambda s: (s['brand'], s['brand_th']), cars)))
# result = []
# for car in brands:
#     obj = {'brand': car[0], 'brand_th':car[1], 'model': list(filter(lambda s: s['brand'] == car[0], cars))}
#     obj['model']
#     result.append(obj)
#
# import pandas as pd
#
# df = pd.DataFrame(cars)
# gdf = df.groupby('model')
# gdf = gdf['nickname'].apply(set)