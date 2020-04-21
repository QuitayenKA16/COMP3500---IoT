from influxdb import InfluxDBClient

dbclient = InfluxDBClient('0.0.0.0', 8086, 'root', 'root', 'mydb')

json_body = [{
    "measurement": 'uri',
    "tags": {
        "user": "default"
        },
    "fields" : {
        "anger" : "7L08IETH8EQmm7k4r8rivb",
        "contempt" : "7L08IETH8EQmm7k4r8rivb",
        "disgust" : "7L08IETH8EQmm7k4r8rivb",
        "fear" : "1IQD1FC4LQa2fa59HytPGV",
        "happiness" : "6M4ZbVjkSE6P3IhbeYbnhc",
        "neutral" : "37i9dQZF1DXc8kgYqQLMfH",
        "sadness" : "0N2pTjZX98Piir6i1VUTzZ",
        "surprise" : "37i9dQZF1DXc8kgYqQLMfH"
    }
}]
dbclient.write_points(json_body)
