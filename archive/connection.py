import yaml
import geopandas as gpd
from sqlalchemy import create_engine 
from enc_password import decryptPassword

def read_yaml(filePath):
    with open(filePath, 'r') as path:
        data = yaml.load(path, yaml.FullLoader)
        return data

my_yaml = read_yaml('bi.yaml')


pgis_con = my_yaml['Contexts']['pg_geodb']


def get_postgis(sql, geom_col):

    dbname = pgis_con['dbname']
    host = pgis_con['host']
    user = pgis_con['user']
    port = pgis_con['port']
    passwordfile = decryptPassword('~/.tdpasswordkey', '~/.geodbpw')


    db_connection_url = f"postgresql://{user}:{passwordfile}@{host}:{port}/{dbname}"
   

    con = create_engine(db_connection_url) 
    df = gpd.GeoDataFrame.from_postgis(sql, con,  geom_col=geom_col, coerce_float=False)
    return df

# print(pgis_con)

# sql = f"""SELECT pt, leadbichtrobnm FROM work_schema.hhp_pt WHERE pt && ST_MakeEnvelope(-96.65498971939088, 32.787229428984595, -96.64783895015718, 32.79004800822172, 4326)"""
# hhp_pt = get_postgis(sql, geom_col='pt')
# hhp_pt