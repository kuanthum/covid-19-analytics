!pip install sodapy
from sodapy import Socrata

client = Socrata("data.cityofnewyork.us",
                 app_token="L67KNyC9J4wO007XLxv0oJlDZ", #o sus udatos
                 username="agustin.ojeda.90@gmail.com",
                 password="Henrydata1600!")
results = client.get("2j8u-wtju", limit=2000000)#primer parametro poner la parte final de los links

#---------------------------------------------------------

#Pueden traerse menos data usando SoQL:
#Ejemplo
results = client.get("g62h-syeh",
                    select="state as estado, date as fecha, inpatient_beds_used_covid as pacientes_covid",
                    where="date between '2020-01-01T00:00:00' and '2020-07-01T00:00:00' and pacientes_covid IS NOT NULL",
                    order="pacientes_covid desc",
                    limit = 100)



endpoints_list = {'data.cityofnewyork.us':'2j8u-wtju'
                'motor_vehicle_collisionscrashes':'h9gi-nx95',
                'new_york_city_truck_routes':       'jjja-shxy',
                'motor_vehicle_collisions_person':  'f55k-p6yu',
                'motor_vehicle_collisions_vehicles':'bm4k-52h4',
                'nypd_motor_vehicle_collisions':    'nypd-motor-vehicle-collisions',
                'bicycle_counts':                   'uczf-rk3c',
                'traffic_volume_counts':            'csv btm5-ppia'
                }


endpoints_list = {'data.cityofnewyork.us':{'2j8u-wtju','None'},
                'data.world':{'h9gi-nx95','motor_vehicle_collisionscrashes'}
                }

'''
que hacemos con esto
https://www1.nyc.gov/site/nypd/stats/traffic-data/traffic-data-collision.page
https://www.kaggle.com/datasets/nycopendata/new-york?datasetId=22531&sortBy=voteCount
https://api.openweathermap.org/data/2.5/onecall/timemachine
'''

