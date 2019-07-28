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
  #print('\n-->Running process_ip_list: ')
  duration_ms = 0
  time_start = time.time()
  for ip in list_ips:
    #print_ip_address(ip)
    process_fping_gso(ip)
  duration_ms = (time.time() - time_start) * 1000
  return duration_ms

# Print out one ip address (for testing)
def print_ip_address(ip):
  print("Checking {}...".format(ip))

def print_report_line(ip, data):
  print("Host: {0} is detected online. Reponse time(s) were: {1}".format(ip,data))

def process_fping_call(ip):
  print('\n-->Running process_fping_call: ')
  rtnCode = subprocess.check_call(['fping', '-a','-C 5', ip], 
    shell=True,
    stdout=subprocess.PIPE,)
  print('return code: ',rtnCode.returncode)
  result = rtnCode.stdout.decode('utf-8')
  print("result: {}".format(result))
  
def process_fping_run(ip):
  print('\n-->Running process_fping_run: ')
  results = subprocess.run(
    ['fping', '-a','-C 5', ip],capture_output=True)
  print('return code: ',results.returncode)
  print('stdout: {}'.format(results.stdout.decode('utf-8')))
  
def process_fping_gso(ip):
  #print('\n-->Running process_fping_gso: ')
  global list_ips_online
  cmd = 'fping -a -C 5 {}'.format(ip) 
  results = subprocess.getstatusoutput(cmd)
  #print('return code: {}'.format(results[0]))
  data = results[1].split(':')[1]
  #print('return: ', data)
  if(results[0]==0):
    print_report_line(ip,data)
    #print('Host: {} is detected online. Response time(s) were: {}'.format(ip,data))
    list_ips_online.append(ip)
  #print(results.stdout.decode('utf-8'))
  #return list_ips_online
  

def example_ls():
  print('\n-->Running example_ls: ')
  completed = subprocess.run(
    ['ls','-l'],
    stdout=subprocess.PIPE,
  )
  print('return code: ', completed.returncode)
  print('Have {} bytes in stdout:\n{}'.format(
    len(completed.stdout),
    completed.stdout.decode('utf-8'))
  )

def print_summary(list_ips_online, duration_ms):
  #print('\n-->Running print_summary: ')
  print('\nThe following hosts were found to be online and responding to ping requests:\n\nDetected Hosts: {}\n==============='.format(len(list_ips_online)))
  for ip in list_ips_online:
    print(ip)
  print('Total time to scan took: {}ms\n'.format(duration_ms))

def calc_range_from_cidr(cidr):
  # first check to make sure that cidr is between 24 and 32
  #arrToStrip = []
  #cidr = cidr.strip(['/',' ','\'])
  #print('cidr (before): {}'.format(cidr))
  cidr = re.sub("[^0-9]",'',cidr)
  #print('cidr: {}'.format(cidr))
  #pass
  global range_ip
  range_cidr_max = 256
  factor = int(cidr)-23
  #print('factor: {}'.format(factor))
  range_ip = int(range_cidr_max / factor)
  #print('range: {}'.format(range_ip))
  return range_ip

# remove non-numeric char from target ip and allow on three octals
def scrub_ip(ip):
  arr_ip = ip.split('.')
  while(len(arr_ip)>3):
    arr_ip.pop()
  ip_clean = '.'.join(arr_ip)
  return ip_clean

def main():
  ip_target = '10.0.2'    # default target ip if none provided
  range_ip = 5            # default range of ips to process if none provided
  if(len(sys.argv)>1):
    ip_target = sys.argv[1]
    ip_target = scrub_ip(ip_target) # only use the first three octals
    #print(ip_target)
    cidr = sys.argv[2]
    range_ip = calc_range_from_cidr(cidr) # get the # of ip addresses to process

  list_ip = generate_ip_list(ip_target, range_ip)
  duration_ms = process_ip_list(list_ip)
  print_summary(list_ips_online, duration_ms)
    
if __name__ == "__main__":
  main()
  #example_ls()
  #process_fping_run('127.0.0.1')
  #process_fping_call('127.0.0.1')
  #process_fping_gso('127.0.0.1')
  #process_fping_gso('127.0.0.0')
  #print_summary()
