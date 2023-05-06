for ((i=0;i<$2;i++))do
    rm loop$1/step3/group${i}/Q.step3.*
    rm loop$1/step3/group${i}/Ord*
    rm loop$1/step3/group${i}/step3.iqtree
    cp loop$1/step5/Q.step5.4x.1.normalized loop$1/step3/group${i}/Q.step3.4x.1
    cp loop$1/step5/Q.step5.4x.2.normalized loop$1/step3/group${i}/Q.step3.4x.2
    cp loop$1/step5/Q.step5.4x.3.normalized loop$1/step3/group${i}/Q.step3.4x.3
    cp loop$1/step5/Q.step5.4x.4.normalized loop$1/step3/group${i}/Q.step3.4x.4
done
rm -rf loop$1/step4/*
rm -rf loop$1/step5/*
