find *notcgcnnunlabel*.csv -type f -newermt '13 Jul 2019 00:00:00 -exec cp {} targetdir \;
find *notcgcnnunlabel*.csv -type f -newermt '13 Jul 2019 20:00:00' -exec cp {} csv0718 \;


echo $i
done

cp $i csv0718/
