#!/usr/bin/python3

import subprocess # for running processes
import time       # to measure process duration
import sys        # to access args
import re         # for regex

# Global var    # note to self: try to limit use of globals
list_ips_online = []

# Create a list of ip addresses to process
def generate_ip_list(ip_target, range_ip):
  #print('\n-->Running generate_ip_list: ')
  list_ips = []
  for i in range(range_ip):
    ip = ip_target + '.' + str(i)
    list_ips.append(ip)
  return list_ips
    

# Loop over that list of IP addresses
def process_ip_list(list_ips):
  print('\nPing-ing ips from {} to {}.'.format(list_ips[0], list_ips[len(list_ips)-1]))
  print('# of ips: {}'.format(len(list_ips)))
  
  duration_ms = 0
  time_start = time.time()
  for ip in list_ips:
    #print_ip_address(ip)   # use this line if want to watch each iteration
    #process_fping_gso(ip)  # legacy way to run fping
    process_fping_run(ip)
  duration_ms = (time.time() - time_start) * 1000
  return duration_ms

# Print out one ip address (for testing)
def print_ip_address(ip):
  print("Checking {}...".format(ip))

def print_report_line(ip, data):
  data = data.replace('\n','')  # remove the carriage return
  print("Host: {0} is detected online. Reponse time(s) were: {1}".format(ip,data))

  
def process_fping_run(ip):
  global list_ips_online
  results = subprocess.run(
    ['fping', '-a','-C 5', ip],capture_output=True, text=True)
  #print('stdout: {}'.format(results.stderr)) # stdout is captured in stderr.
  
  # for successful return code, print results and add to summary list
  if(results.returncode==0):
    data = results.stderr.split(':')[1] # save the timings as data
    print_report_line(ip,data)
    list_ips_online.append(ip)

# ping an ip address, report online ips, and add them to the summary ip list
def process_fping_gso(ip):
  global list_ips_online
  cmd = 'fping -a -C 5 {}'.format(ip) 
  results = subprocess.getstatusoutput(cmd)

  # for successful return code, print results and add to summary list
  if(results[0]==0):
    data = results[1].split(':')[1] # save the timings as data
    print_report_line(ip,data)
    list_ips_online.append(ip)
  
# print summary report
def print_summary(list_ips_online, duration_ms):
  print('\nThe following hosts were found to be online and responding to ping requests:\n\nDetected Hosts: {}\n==============='.format(len(list_ips_online)))
  for ip in list_ips_online:
    print(ip)
  print('Total time to scan took: {:,.0f} ms or {:,.2f} seconds\n'.format(duration_ms, duration_ms/1000))

def calc_range_from_cidr(cidr):
  # remove all non-numeric chars
  cidr = re.sub("[^0-9]",'',cidr)
  cidr = int(cidr)

  # then make sure that cidr is between 24 and 32, inclusive
  if not (cidr >= 24 and cidr <= 36):
    print('\n   ***Bad cidr /{} value; using /24 instead.***'.format(cidr))
    cidr = 24 # default for bad cidr

  # calculate the range  
  range_cidr_max = 256
  factor = cidr - 24
  range_ip = int(range_cidr_max / (2**factor))
  #print('range: {}'.format(range_ip))
  return range_ip

# remove non-numeric char from target ip and allow on three octals
def scrub_ip(ip):
  arr_ip = ip.split('.')
  while len(arr_ip)>3:
    arr_ip.pop()
  ip_3octals = '.'.join(arr_ip)
  return ip_3octals

def main():
  ip_target = '10.0.2'    # default target ip if none provided
  range_ip = 5            # default range of ips to process if none provided
  if len(sys.argv)>1:
    ip_target = sys.argv[1]
    ip_target = scrub_ip(ip_target) # only use the first three octals

    # get the CIDR and calc the range from it
    cidr = sys.argv[2]
    range_ip = calc_range_from_cidr(cidr) # get the # of ip addresses to process

  # make the ip test list, process it, getting the process time, & print out the final report
  list_ip = generate_ip_list(ip_target, range_ip)
  duration_ms = process_ip_list(list_ip)
  print_summary(list_ips_online, duration_ms)
    
if __name__ == "__main__":
  main()
  #process_fping_run('127.0.0.1')
  #process_fping_gso('127.0.0.1')
