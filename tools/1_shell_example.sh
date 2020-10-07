# check cpu
lscpu

# zip
zip -r output.zip folder1 folder2
zip -r output.zip segmented_wavs_selected720db20rand

# count
ls *600* | wc -l
ls *.wav | wc -l
ls . | wc -l

# size of folder
du -h --max-depth=1 | sort -hr

# git commit
git commit -a -m 'comment'

git diff master..old-state


ss='111|2222'
A="$(cut -d'm' -f2 <<<$ss)"

declare -a arr=("element1" "element2" "element3")

## now loop through the above array
# for i in "${arr[@]}"
for i in 222_rand 222_randd
do
   echo "$i"
   A="$(cut -d'_' -f1 <<<$i)"
   echo "$A"
   # or do whatever with individual element of the array
done


# vim; to replace
# :%s/foo/bar/gc
