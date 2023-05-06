for ((i=0;i<51;i++))do
	cp -rf out$i loop3/step3/group$i
	sh step4.sh $1 $i
done
sh step5.sh $1 51
