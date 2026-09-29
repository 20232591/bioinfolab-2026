for X in {1..10}
do
    echo $X
done
 
for F in data/*.fasta
do
    echo $F
    grep -c ">" $F
done



