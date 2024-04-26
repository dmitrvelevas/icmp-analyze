#количество узлов
N=62

#начальные параметры для настройки туннелей
prefix="10.249.249"
net_address=0

#адреса точек A и B
first_addr=$prefix.$((net_address+1))
last_addr=$prefix.$((N*4 - 6))

#добавляем первый узел
ip netns add node1

#настройка узла A
ip link add inter-1 type veth peer name inter-2
ip link set inter-1 netns node1
ip netns exec node1 ip addr add $prefix.$((net_address+1))/30 dev inter-1
ip netns exec node1 ip link set dev inter-1 up
ip netns exec node1 ip route add $last_addr/32 via $prefix.$((net_address+2))

#добавляем следующий узел
ip netns add node2

for i in $(seq 2 $((N-1)))
do
	#настройка первого внутреннего интерфейса
	ip link set inter-$((i*2 - 2)) netns node$i
	ip netns exec node$i ip addr add $prefix.$((net_address+2))/30 dev inter-$((i*2 - 2))
	ip netns exec node$i ip link set dev inter-$((i*2 - 2)) up
	ip netns exec node$i ip route add $first_addr/32 via $prefix.$((net_address+1))

	#добавляем задержку
	ip netns exec node$i tc qdisc add dev inter-$((i*2 - 2)) root netem delay 1ms

	#переключаемся на следующую сеть
	net_address=$((net_address+4))

	#настройка второго внутреннего интерфейса
	ip link add inter-$((i*2-1)) type veth peer name inter-$((i*2))
	ip link set inter-$((i*2-1)) netns node$i
	ip netns exec node$i ip addr add $prefix.$((net_address+1))/30 dev inter-$((i*2-1))
        ip netns exec node$i ip link set dev inter-$((i*2-1)) up
	ip netns exec node$i ip route add $last_addr/32 via $prefix.$((net_address+2))

	#добавляем задержку
	ip netns exec node$i tc qdisc add dev inter-$((i*2-1)) root netem delay 1ms

	#добавляем следующий узел
	ip netns add node$((i+1))
done

#настраиваем узел B
ip link set inter-$((N*2 - 2)) netns node$N
ip netns exec node$N ip addr add $prefix.$((net_address+2))/30 dev inter-$((N*2 - 2))
ip netns exec node$N ip link set dev inter-$((N*2 - 2)) up
ip netns exec node$N ip route add $first_addr/32 via $prefix.$((net_address+1))

echo -------------------
echo Namespace A: node1
echo ip address: $first_addr
echo ip netns exec node1 ping $last_addr
echo ip netns exec node1 tcpdump icmp -w A.dump
echo -------------------
echo "Namespace B: node$N"
echo ip address: $last_addr
echo ip netns exec node$N ping $first_addr
echo ip netns exec node$N tcpdump icmp -w B.dump

