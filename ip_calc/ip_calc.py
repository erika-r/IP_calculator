
#run gui to get results or change return statements to print

from textwrap import wrap

#PART 1 - IP ADDRESS CALC
def convert2bin(ip_addr):
	tmp_list = [bin(int(num)).replace("0b","") for num in ip_addr.split(".")]
	ip_list = ["0"*(8-len(num))+num for num in tmp_list]	#add remaining 0s
	return ip_list	

def convert2dec(binary_num):
	tmp_list = binary_num.split(".")	#list of 1s and 0s
	dec_list = [str(int(num,2)) for num in tmp_list]
	return dec_list

#first or last address for a given class
def get_address(clss,pos,prefix):
	if pos == "first":
		full_prefix = prefix + "0"*(8 -len(prefix))
		addr = "{}.{}.{}.{}".format(full_prefix,"0"*8,"0"*8,"0"*8)
	else:
		full_prefix = prefix + "1"*(8 -len(prefix))
		addr = "{}.{}.{}.{}".format(full_prefix,"1"*8,"1"*8,"1"*8)

	return ".".join(convert2dec(addr))

def get_class_stats(ip_addr):
	
	ip_list = convert2bin(ip_addr)

	ip_classes = ["A","B","C","D","E"] 
	class_definer = ip_list[0]	#first 8 bits

	#index of first 0 == index in ip_classes
	try:
		indx = class_definer.index("0")
		ip_class = ip_classes[indx]
	except:								#if not found, class is E
		ip_class = "E"

	#class : [networks, hosts,prefixes]
	class_info = {"A": {"networks":"127","hosts":"16777216","prefix":"0"},
			"B": {"networks":"16384","hosts":"65536","prefix":"10"},
			"C": {"networks":"2097152","hosts":"256","prefix":"110"},
			"D": {"networks":"N/A","hosts":"N/A","prefix":"1110"},
			"E": {"networks":"N/A","hosts":"N/A","prefix":"1111"}}

	av_nets = class_info[ip_class]["networks"]
	av_hosts = class_info[ip_class]["hosts"]

	first_addr = get_address(ip_class,"first",class_info[ip_class]["prefix"]) 
	last_addr = get_address(ip_class,"last",class_info[ip_class]["prefix"])

	return ("Class: {}\nNetwork: {}\nHost: {}\nFirst address: {}\nLast address: {}\n".format(ip_class,av_nets,av_hosts,first_addr,last_addr))


#PART 2 & 3 - SUBNET CLASS C & B CALC
def get_cidr(subnet_mask):
	submask_bin = convert2bin(subnet_mask)	#list of 1s & 0s
	return "".join(submask_bin).count("1")

#Class functions
def classB(subnet_mask,iplist,cidr):

	submask_bin = convert2bin(subnet_mask)

	octet = "".join([num for num in submask_bin[2:] if num != "11111111"][0])	#number to calculate block size
	block_size = 256 - int(convert2dec(octet)[0])
	av_nets = 2**(octet.count("1"))

	#add 8 0s if in 3rd octet
	av_hosts = (2**(octet.count("0")))	# num of 0s in binary notation, - broadcast & network later
	if submask_bin.index(octet) == 2:
		av_hosts = (2**(octet.count("0") + 8))

	subnets,broadcast_addr,first_addr,last_addr = [],[],[],[]
	subnets += ["{}.{}.0".format(".".join((iplist[0:2])),(block_size*i)) for i in range(av_nets)]
	broadcast_addr += ["{}.{}.255".format(".".join((iplist[0:2])),(block_size*i)-1) for i in range(1,av_nets+1)]
	first_addr += ["{}.{}.1".format(".".join((iplist[0:2])),(block_size*i)) for i in range(av_nets)]
	last_addr += ["{}.{}.254".format(".".join((iplist[0:2])),(block_size*i)-1) for i in range(1,av_nets+1)]

	return [av_nets,subnets,broadcast_addr,first_addr,last_addr,av_hosts]

def classC(subnet_mask,iplist,cidr):

	zeroes_len = convert2bin(subnet_mask)[-1].count("0")
	av_hosts = 2**(zeroes_len)
	av_nets = 2**(8-zeroes_len)
	block_size = av_hosts	#to get next subnet, this == (256 - av_nets) == av_hosts

	subnets = ["{}.{}".format((".").join(iplist[:-1]),str((block_size*i))) for i in range(av_nets)]
	broadcast_addr = ["{}.{}".format((".").join(iplist[:-1]),str((block_size*i) - 1)) for i in range(1,av_nets+1)]
	first_addr = ["{}.{}".format((".").join(iplist[:-1]),str((block_size*i) + 1)) for i in range(av_nets)]
	last_addr = ["{}.{}".format((".").join(iplist[:-1]),str((block_size*i) - 2)) for i in range(1,av_nets+1)]
	
	return [av_nets,subnets,broadcast_addr,first_addr,last_addr,av_hosts]

def get_subnet_stats(ip_addr,subnet_mask):

	iplist = ip_addr.split(".")
	ip_bin = convert2bin(ip_addr)
	cidr = get_cidr(subnet_mask)

	identifier = int(ip_addr[:3])	#class b or c ?
	if identifier < 192:
		info = classB(subnet_mask,iplist,cidr)
	else:
		info = classC(subnet_mask,iplist,cidr)

	return ("Address: {}\nSubnets: {}\nAdressable hosts per subnet: {}\nValid subnets: {}\nBroadcast addresses: {}\nFirst addresses: {}\nLast addresses: {}\n".format((ip_addr + "/" + str(cidr)), info[0],info[-1]-2,info[1],info[2],info[3],info[4]))

#PART 4 - SUPERNETTING
def get_supernet_stats(classC_addr):
	#common prefix + 0s = network id
	#common prefix turned into 1s + 0s = network mask
	#assume difference is in 3rd bit
	#since addresses are contiguous,only first and last needed to compare 

	third_bit = [convert2bin(classC_addr[0])[2]] + [convert2bin(classC_addr[-1])[2]]

	for i in range(8):
		if third_bit[0][i] == third_bit[1][i]:
			prefix = third_bit[0][:i+1]			#best match for prefix

	full_prefix = prefix + "0"*(8-len(prefix))
	
	#net ID
	base = classC_addr[0].split(".")
	net_id = "{}.{}.{}.0".format(base[0],base[1],str(convert2dec(full_prefix)[0]))
	
	#net mask
	tmp = "1"*(16 + len(prefix)) + "0"*(32 -(16 + len(prefix)))
	bin_net_mask = ".".join(wrap(tmp,8))
	net_mask = ".".join(([str(num) for num in convert2dec(bin_net_mask)]))

	cidr = get_cidr(net_mask)
	return ("Address: {}/{}\nNetwork Mask: {}\n".format(net_id,cidr,net_mask))
