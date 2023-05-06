for entry in `ls out$2`; do
	iqtree-2.2.2.1 -seed 1 -T $1 -s out$2/$entry --prefix $entry -m "MIX{Q.step3.4x.1,Q.step3.4x.2,Q.step3.4x.3,Q.step3.4x.4}*G4" --no-seq-comp -wslmr
done
touch step3.iqtree
