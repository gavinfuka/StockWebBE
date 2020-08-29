
from app import app as Backend
if __name__ ==  "__main__":
    Backend.run( host="0.0.0.0", port="4000",debug=True)
    Backend.config['JSON_AS_ASCII'] = False

