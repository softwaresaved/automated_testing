for F in $(ls samples)
do
    count_frequency samples/$F testoracle/freqs_$F
    count_frequency samples/$F testoracle/freqs5_$F 5
done
