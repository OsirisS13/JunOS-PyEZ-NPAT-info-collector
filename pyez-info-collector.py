from jnpr.junos import Device
import jnpr.junos
#for user prompt to enter passwords 
from getpass import getpass
#used to parse the xml???
from lxml import etree
import sys

#function to write data to text file
def writefile(name,contents):
	#open file in append mode, will create if file doesnt exist
	file = open(name,'a')
	#check to see if the contents is a string, if it is then write directly to file, if not then parse it from xml to string, and strip the output tags
	if isinstance(contents, basestring) == False:
		contents = etree.tostring(contents)
		contents = contents.replace('<output>', '')
		contents = contents.replace("</output>", "")
		contents = contents.replace("<configuration-text>", "")
		contents = contents.replace("</configuration-text>", "")
		#print contents
		file.write(contents)
	else:
		print ('%s file written' %name)
		file.write(contents)
	return

#function to convert xml to string and strip some tags to make it emulate cli output
def convert_etree_to_string(etree_input):
	if isinstance(etree_input, basestring) == False:
		etree_input = etree.tostring(etree_input)
		etree_input = etree_input.replace('<output>', '')
		etree_input = etree_input.replace("</output>", "")
		etree_input = etree_input.replace("<configuration-text>", "")
		etree_input = etree_input.replace("</configuration-text>", "")
		#print contents
		return etree_input
	else:
		return etree_input		
	
def get_data(ipaddress, username, passwd):
	#check to see if netconf is reachable, otherwise timeout after
	Device.auto_probe = 1
	#create device object
	dev = Device(host=ipaddress, user=username, password=passwd, port = "22" )
	#connet to device
	try:
		dev.open()
		print("\nNETCONF connection to %s opened!" %ipaddress)
		print("Beginning data collection...")
		#collect all data
		#store facts
		devicefacts = dev.facts
		#get hostname
		hostname = devicefacts['hostname'].replace("'","")
		#get config
		config = convert_etree_to_string(dev.rpc.get_config(options={'format':'text'}))
		config = hostname + "> show config|display inheritance|no-more \n" + config
		#get hardware ("show chassis hardware ")
		hw = convert_etree_to_string(dev.rpc.get_chassis_inventory({'format':'text'}))
		hw = hostname + "> show chassis hardware|no-more\n " + hw  
		#get hw models
		hwmodel = convert_etree_to_string(dev.rpc.get_chassis_inventory({'format':'text'}, models=True))
		hwmodel = hostname + "> show chassis hardware models|no-more \n" + hwmodel
		#get software (show version)
		sw = convert_etree_to_string(dev.rpc.get_software_information({'format':'text'}))
		sw = hostname + "> show version|no-more \n" + sw
		#get fpc info
		fpc = convert_etree_to_string(dev.rpc.get_fpc_information({'format':'text'}))
		fpc = hostname + "> show chssis fpc|no-more \n" + fpc
		#get interface info
		interface = convert_etree_to_string(dev.rpc.get_interface_information({'format':'text'}))
		interface = hostname + "> show interfaces|no-more \n" + interface
		#get ted data base info (show ted database extensive)
		ted = convert_etree_to_string(dev.rpc.get_ted_database_information({'format':'text'}, extensive=True))
		ted = hostname + "> show ted database extensive|no-more \n" + ted
		#get rsvp ingress (show rsvp session ingress detail logical-router all|no-more)
		rsvp_ingress = convert_etree_to_string(dev.rpc.get_rsvp_session_information({'format':'text'}, ingress=True))
		rsvp_ingress = hostname + "> show rsvp session ingress detail | no-more \n" + rsvp_ingress
		rsvp_transit = convert_etree_to_string(dev.rpc.get_rsvp_session_information({'format':'text'}, transit=True))
		rsvp_transit = hostname + "> show rsvp session transit detail | no-more \n" + rsvp_transit
		lsp_stats = convert_etree_to_string(dev.rpc.get_mpls_lsp_information({'format':'text'}, extensive=True, statistics = True ,ingress=True))
		lsp_stats = hostname + "> show mpls lsp statistics ingress extensive | no-more \n" + lsp_stats

		#write data to files
		#config file
		writefile(hostname + "_Config.txt", config)
		#equipment file
		writefile(hostname + "_Equipment.txt", hostname + " show configuration system hostname \n host-name " + hostname + "\n \n")
		writefile(hostname + "_Equipment.txt", sw)
		writefile(hostname + "_Equipment.txt", hw)
		writefile(hostname + "_Equipment.txt", fpc)
		writefile(hostname + "_Equipment.txt", hwmodel)
		#Interface file
		writefile(hostname + "_Interface.txt", hostname + " show configuration system hostname \n host-name " + hostname + "\n \n")
		writefile(hostname + "_Interface.txt", interface)
		#topology file
		writefile(hostname + "_Topology.txt", ted)
		#transit tunnel file
		writefile(hostname + "_TransitTunnel.txt", hostname + " show configuration system hostname \n host-name " + hostname + "\n \n")
		writefile(hostname + "_TransitTunnel.txt", rsvp_ingress)
		writefile(hostname + "_TransitTunnel.txt", rsvp_transit)
		#tunnel path file
		writefile(hostname + "_TunnelPath.txt", hostname + " show configuration system hostname \n host-name " + hostname + "\n \n")
		writefile(hostname + "_TunnelPath.txt", lsp_stats)
		print("Operation Complete.")
		dev.close()
		print("NETCONF connection to %s is now closed.\n" %ipaddress)
	#if probe times out and raises a probe error
	except jnpr.junos.exception.ProbeError as e: 
		print("NETCONF connection to %s is not reachable, moving on.." %ipaddress)
	#any other error
	except Exception as e:
		print (e)

#user inputs
user = raw_input("Username: ")	
passwd = getpass("Device password: ")
startip = input("Enter start third octect number: ")
endip = input("Enter end third octect number: ")
#generate and loop through data collection for ip addresses from 10.189.x.10 where x begins at intial "i" value and ends at the while < value.
i = startip
while i < endip:
        val = str(i)
        currentip = ( "10.189.%s.10" %val)
        i = i + 1
	get_data(currentip,user, passwd)
