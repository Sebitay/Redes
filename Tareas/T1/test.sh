
n=$1

script="./client_echo3.py"
size=$2
host="localhost"
file=$3
port=$4


for ((j=1; j<=n; j++)); do
    python3 $script $size $host $port < "in_files/$file" > "out_files/txt/${file}_${port}_${size}_${n}${j}.out" &
done


wait