# pysweep

# USAGE:  pysweep [optional ipAddress, cidr]

Running this command will generate a ping sweep of all ip addresses starting with 10.0.2.0 unless one provides the ip from which to start and a cidr from /24 to /32.

It will iterate through the included set of ip addresses looking for online hosts and will show five latency ping times, then will print out a summary report listing all the online hosts.

