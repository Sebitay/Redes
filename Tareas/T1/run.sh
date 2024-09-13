#!/bin/bash

# Nombre del script que quieres ejecutar
script="./test.sh"

# Lista de parámetros (n, size, port, file)
params=(
    "100 5000 s.txt"
    "100 10000 s.txt"
    "100 50000 s.txt"
)

# Puertos que deseas usar
ports=(1819)

# Loop a través de los puertos
for port in "${ports[@]}"; do
    output_file="time_results_$port.txt"
    echo "### Puerto $port ###" >> $output_file
    echo "Ejecutando en puerto $port..."

    # Loop a través de los parámetros
    for param in "${params[@]}"; do
        echo "Ejecutando: $param en puerto $port"
        echo "Experimento: $param en puerto: $port" >> $output_file
        # Guarda el tiempo de ejecución usando el comando time
        { time $script $param $port ; } 2>> $output_file

        echo "------------------------------------" >> $output_file
    done
done

echo "Todos los experimentos completados. Los resultados se guardaron en $output_file."
