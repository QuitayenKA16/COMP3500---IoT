from influxdb import InfluxDBClient

dbclient = InfluxDBClient('0.0.0.0', 8086, 'root', 'root', 'mydb')

#query = 'select * from "uri"'
query = "DROP SERIES FROM /.*/"
result = dbclient.query(query)
