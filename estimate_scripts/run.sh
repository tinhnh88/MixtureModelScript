export CURR_DIR=`pwd`
cd ${CURR_DIR}/loop$1/step3/group$2
bsub < train$2.bsub
