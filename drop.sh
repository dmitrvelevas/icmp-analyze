N=62
for i in $(seq 1 $N)
do
	echo ip netns del node$i
	ip netns del node$i
done
