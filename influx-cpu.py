#!/usr/bin/python
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-Q", "--query", help="Realizar consulta", action="store_true")
parser.add_argument("-v", "--version", help="Consulta la version del servidor Influx", action="store_true")
parser.add_argument("-S", "--secure", help="Usar https en lugar de http", const="https", default="http", action="store_const")
parser.add_argument("-i", "--ip", help="Indica la ip de influx")
parser.add_argument("-d", "--database", help="Indica la base de datos para la consulta")
parser.add_argument("-H", "--host", help="Indica el host para la consulta")
parser.add_argument("-V", "--value", help="Valor del que se realiza la consulta")
parser.add_argument("-t", "--time", help="Tiempo desde el que se obtienen los datos. Ns, Nm, Nh")
args = parser.parse_args()

if args.query:
	query = os.system("curl -G "+ args.secure +"://"+ args.ip +":8086/query --data-urlencode db="+ args.database +" --data-urlencode epoch=s --data-urlencode \"q=SELECT mean("+ args.value +") FROM cpu WHERE host='"+ args.host +"' AND time > now() - "+args.time+" GROUP BY time(10m)\"")

if args.version:
	version = os.system("curl -sl -I "+ args.secure +"://"+ args.ip +":8086/ping")
