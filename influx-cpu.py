#!/usr/bin/python
import os
import sys
import subprocess
import argparse

#Es bastante cutrecillo, pero hace lo que se necesita (espero xD).
#Disponible tambien en https://github.com/Loenberg123/influx-telegraf-cpu

parser = argparse.ArgumentParser()
parser.add_argument("-Q", "--query", help="Realizar consulta", action="store_true")
parser.add_argument("-v", "--version", help="Consulta la version del servidor Influx", action="store_true")
parser.add_argument("-S", "--secure", help="Usar https en lugar de http", const="https", default="http", action="store_const")
parser.add_argument("-i", "--ip", help="Indica la ip de influx")
parser.add_argument("-w", "--warn", help="Indica el nivel de warning")
parser.add_argument("-c", "--crit", help="Indica el nivel de critical")
parser.add_argument("-d", "--database", help="Indica la base de datos para la consulta")
parser.add_argument("-H", "--host", help="Indica el host para la consulta")
parser.add_argument("-V", "--value", help="Valor del que se realiza la consulta")
parser.add_argument("-t", "--time", help="Tiempo desde el que se obtienen los datos. Ns, Nm, Nh")
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()

warning = args.warn
critical = args.crit

if args.query:
	q = "curl -s -G "+ args.secure +"://"+ args.ip +":8086/query --data-urlencode db="+ args.database +" --data-urlencode \"q=SELECT mean("+ args.value +") FROM cpu WHERE host='"+ args.host +"' AND time > now() - "+args.time+"\" | awk -F',' '{print $6}'| awk -F] '{printf(\"%.2f\",  $1)}'"
	result = subprocess.check_output(q, shell=True)
	if result is None:
		print "UNKNOWN - Could not retrieve data?"
		sys.exit(3)
	if result >= warning:
		print "WARNING - Host: "+args.host+" "+args.value+" mean: "+result+" - from: "+args.time
                sys.exit(1)
	if result >= critical:
		print "CRITICAL - Host: "+args.host+" "+args.value+" mean: "+result+" - from: "+args.time
                sys.exit(2)
	else:
		print "OK - Host: "+args.host+" "+args.value+" mean: "+result+" - from: "+args.time
		sys.exit(0)


if args.version:
	version = "curl -sl -I "+ args.secure +"://"+ args.ip +":8086/ping | awk 'NR==4{print}'"
	result = subprocess.check_output(version, shell=True)
	if result is not None:
		print result
		sys.exit(0)
	else:
		print "CRITICAL - Could not get version"
		sys.exit(2)
