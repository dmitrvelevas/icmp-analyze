#!/usr/bin/python3

#----Настраиваемые параметры----

ip_A='10.249.249.1'
ip_B='10.249.249.242'

dump_file_A = "A.dump"
dump_file_B = "B.dump"

#------------------------------

import scapy.all as scapy

dump_A = scapy.rdpcap(dump_file_A)
dump_B = scapy.rdpcap(dump_file_B)

list_A_to_B = []
list_B_to_A = []

def one_direction_time(dump1, dump2, src, dst):

    result = []

    for i in range(0, len(dump1)-1):
    
        #отбрасываем не ip пакеты
        if "IP" not in dump1[i]:
            continue
        
        #оставляем только icmp пакеты, осносящиеся к взаимодействию исследуемой пары хостов
        if  dump1[i]['IP'].src == src and dump1[i]['IP'].dst == dst and dump1[i]['IP'].proto == 1:
            for j in range(0, len(dump2)-1):
                
                #отбрасываем не ip пакеты
                if "IP" not in dump2[j]:
                    continue
                
                #оставляем только icmp пакеты, относящиеся к взаимодействию исследуемой пары хостов
                if  dump2[j]['IP'].src == src and dump2[j]['IP'].dst == dst and dump2[j]['IP'].proto == 1:
                    #находим пакеты с одинаковой контрольной суммой и вычисляем время между отправкой и получением
                    if dump1[i]['ICMP'].chksum == dump2[j]['ICMP'].chksum:
                        result.append(round(abs(dump1[i].time - dump2[j].time)*1000))
    
    return result

list_A_to_B = one_direction_time(dump_A, dump_B, ip_A, ip_B)
list_B_to_A = one_direction_time(dump_B, dump_A, ip_B, ip_A)


print ("A -> B  B -> A")
for i in range(0, min(len(list_A_to_B), len(list_B_to_A)) - 1):
    print (str(list_A_to_B[i]) + 'ms    ' + str(list_B_to_A[i]) + 'ms')