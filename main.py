import json
import sys
import sqlite3

sql_conn = sqlite3.connect('navroutes.sqlite')

with open('schema.sql', 'r', encoding='utf-8') as schema_file:
    sql_conn.executescript(''.join(schema_file.readlines()))


for line in sys.stdin:  # open('example.txt', 'r').readlines():
    event = json.loads(line)

    if event['$schemaRef'] != 'https://eddn.edcd.io/schemas/navroute/1':
        continue

    software_name = event['header']['softwareName']
    software_version = event['header']['softwareVersion']

    timestamp = event['message']['timestamp']

    route = event['message']['Route']

    route_for_insert = list()
    point_id = 0
    route_id = sql_conn.execute('select route_id from routes order by route_id desc limit 1;').fetchone()

    if route_id is None:
        route_id = 0

    else:
        route_id = route_id[0] + 1

    for route_point in route:
        StarSystem = route_point['StarSystem']
        StarSystemID = route_point['SystemAddress']
        StarClass = route_point['StarClass']
        x = route_point['StarPos'][0]
        y = route_point['StarPos'][1]
        z = route_point['StarPos'][2]

        sql_r = sql_conn.execute('select count(*) from systems where system_id = ?', [StarSystemID])

        route_for_insert.append([route_id, point_id, StarSystemID, timestamp])
        point_id = point_id + 1

        if sql_r.fetchone()[0] > 0:
            with sql_conn:
                sql_conn.execute('update systems set '
                                 'system_name = ?,'
                                 'star_class = ?,'
                                 'x = ?,'
                                 'y = ?,'
                                 'z = ?,'
                                 'updated_timestamp = ?,'
                                 'software_name = ?,'
                                 'software_version = ? '
                                 'where system_id = ?',
                                 [StarSystem, StarClass, x, y, z, timestamp,
                                  software_name, software_version, StarSystemID])

        else:
            with sql_conn:
                sql_conn.execute('insert into systems ('
                                 'system_name,'
                                 'star_class,'
                                 'system_id,'
                                 'x,'
                                 'y,'
                                 'z,'
                                 'updated_timestamp,'
                                 'software_name,'
                                 'software_version'
                                 ') values (?, ?, ?, ?, ?, ?, ?, ?, ?);',
                                 [StarSystem, StarClass, StarSystemID, x, y, z,
                                  timestamp, software_name, software_version])

    with sql_conn:
        sql_conn.executemany('insert into routes (route_id, point_id, system_id, timestamp) values (?, ?, ?, ?)'
                             , route_for_insert)


sql_conn.close()
