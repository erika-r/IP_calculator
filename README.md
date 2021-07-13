# IP_calculator#
This is a calculator which classifies, subnets, and supernets IP addresses.

This project was created in 5 parts
- implementing a "get_class_stats" function which takes in an IP address and outputs
  - The class of the address
  - The number of networks for the class of the address
  - The number of hosts for the class of the address
  - The first IP address for the class
  -The last IP address for the class
- implementing a "get_subnet_stats" function which takes in a Class C IP address and a subnet mask. It then outputs
  - The ip address in CIDR notation e.g. 192.168.10.0/26
  - The number of subnets on the network
  - The number of addressable hosts per subnet
  - The valid subnets
  - The broadcast address of each subnet
  - The valid hosts on each subnet
- extending the "get_subnet_stats" function to include Class B addresses
- implementing a "get_supernet_stats" which takes in a list of contiguous Class C addresses. It then outputs
  - The network using CIDR notation e.g. 205.100.0.0/22 (the format is the first network number, followed
    by a / followed by the number of network bits).
  - The network mask
- creating a GUI using Tkinter
