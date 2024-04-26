#!/usr/bin/python3

import sys
import scapy.all as scapy

dump_file_A = "A.dump"
dump_file_B = "B.dump"

ip_A='10.249.249.1'
ip_B='10.249.249.242'

if len(sys.argv) == 3: 
    dump_file_A = sys.argv[1]
    dump_file_B = sys.argv[2]

#print (dump_file_A)
#print (dump_file_B)

dump_A = scapy.rdpcap(dump_file_A)
dump_B = scapy.rdpcap(dump_file_B)

list_A_to_B = []
list_B_to_A = []

#print ("A -> B")
#for i in range(0, len(dump_A)-1):
#    #отфильтровываем только icmp трафик и пакеты, осносящиеся к взаимодействию исследуемой пары хостов
#    if  dump_A[i]['IP'].src == ip_A and dump_A[i]['IP'].dst == ip_B and dump_A[i]['IP'].proto == 1:
#        for j in range(0, len(dump_B)-1):
#            #отфильтровываем только icmp трафик и пакеты, осносящиеся к взаимодействию исследуемой пары хостов
#            if  dump_B[j]['IP'].src == ip_A and dump_B[j]['IP'].dst == ip_B and dump_B[j]['IP'].proto == 1:
#                if dump_A[i]['ICMP'].chksum == dump_B[j]['ICMP'].chksum:
#                    #print(str(round(abs(dump_A[i].time - dump_B[j].time)*1000)) + 'ms')
#                    list_A_to_B.append(round(abs(dump_A[i].time - dump_B[j].time)*1000))


def one_direction_time(dump1, dump2, src, dst):

    result = []

    for i in range(0, len(dump1)-1):
        #отфильтровываем только icmp трафик и пакеты, осносящиеся к взаимодействию исследуемой пары хостов
        if  dump1[i]['IP'].src == src and dump1[i]['IP'].dst == dst and dump1[i]['IP'].proto == 1:
            for j in range(0, len(dump2)-1):
                #отфильтровываем только icmp трафик и пакеты, осносящиеся к взаимодействию исследуемой пары хостов
                if  dump2[j]['IP'].src == src and dump2[j]['IP'].dst == dst and dump2[j]['IP'].proto == 1:
                    if dump1[i]['ICMP'].chksum == dump2[j]['ICMP'].chksum:
                        result.append(round(abs(dump_A[i].time - dump_B[j].time)*1000))
    
    return result

list_A_to_B = one_direction_time(dump_A, dump_B, ip_A, ip_B)
list_B_to_A = one_direction_time(dump_B, dump_A, ip_B, ip_A)


print ("A -> B  A -> B")
for i in range(0, min(len(list_A_to_B), len(list_B_to_A)) - 1):
    print (str(list_A_to_B[i]) + 'ms    ' + str(list_B_to_A[i]) + 'ms')