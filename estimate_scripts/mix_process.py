import numpy as np
import os
import time
import sys
import glob
os.environ["CURR_DIR"] = os.getcwd()
site_rate_type = "4x"
def create_bjob_file(folder, number_core, job_id, loop_id):
    print("Folder: ",folder)
    bjFile = "train" + str(job_id) + ".bsub"
    BJ = open(folder +  bjFile, 'w')
    if int(job_id) <= 16:
	number_core = 8
    BJ.write('#BSUB -J iq4x_' + str(job_id) + '\n')
    BJ.write('#BSUB -n ' + str(number_core) + '\n')
    BJ.write('#BSUB -R "span[hosts=1]"\n')
    BJ.write('#BSUB -q normal\n')
    BJ.write('#BSUB -m "fit01 fit02 fit03 fit04 fit05 fit08 fit09 fit10 fit11 fit12 fit13 fit14 fit15 fit16"\n')
    # Run Modelfinder on training set
    if site_rate_type == "4x":
        cmd = 'sh run_step3_4x.sh %d %d'%(number_core,int(job_id))
    else:
	cmd = 'sh run_step3_4m.sh %d %d'%(number_core,int(job_id))
    BJ.write(cmd)
    BJ.close()
    step3file = open("step3.sh","w")
    step3file.write(cmd)
    step3file.close()
    cmd = 'mv %s/%s %s/group%d'%(folder,bjFile,folder,job_id)
    os.system(cmd)
    if site_rate_type == "4x":
        cmd = "cp run_step3_4x.sh %s/group%d"%(folder,job_id)
    else:
	cmd = "cp run_step3_4m.sh %s/group%d"%(folder,job_id)
    os.system(cmd)
    if loop_id == 1:
        cmd = 'cp Q.LG %s/group%d/Q.step3.4x.1'%(folder,job_id)
        os.system(cmd)
        cmd = 'cp Q.LG %s/group%d/Q.step3.4x.2'%(folder,job_id)
        os.system(cmd)
        cmd = 'cp Q.LG %s/group%d/Q.step3.4x.3'%(folder,job_id) 
        os.system(cmd)
        cmd = 'cp Q.LG %s/group%d/Q.step3.4x.4'%(folder,job_id)
        os.system(cmd)
    cmd = 'sh run.sh %d %d'%(loop_id,job_id)
    os.system(cmd)
    print(cmd)

def prepare_folder(number_file):
    folder_id = 0
    file_id = 0
    job_id = 0
    count_file = 0
    cmd = "mkdir out0"
    os.system(cmd)
    for f in glob.glob(r"hssp/*phyml"):
        if file_id == number_file:
            cmd = "mkdir out%d"%(folder_id+1)
            os.system(cmd)
	    print(cmd)
            folder_id = folder_id + 1
	    file_id = 0
        cmd = "cp %s out%d"%(f,folder_id)
        os.system(cmd)
        file_id = file_id + 1
	
def pearon_corr(model1, model2):
    print(model1)
    print(model2)
    file1 = open(model1,"r")
    file2 = open(model2,"r")
    list1 = [0]*190
    list2 = [0]*190
    line1 = file1.read().split()
    line2 = file2.read().split()
    line1 = line1[:-20]
    line2 = line2[:-20]
    for i in range(len(line1)):
        list1[i] = float(line1[i])
        list2[i] = float(line2[i])
    matrix = np.corrcoef(list1, list2)
    corr = matrix[0][1]
    return corr
def do_step3(loop_id, group_count):
    print("This is step 3")
    number_core = 4
    for i in range(group_count):
	cmd = "mkdir -p loop%d/step3/group%d"%(loop_id,i)
	os.system(cmd)
 	cmd = "cp -rf out%d loop%d/step3/group%d/"%(i,loop_id,i)
	os.system(cmd)
	path="loop%d/step3/"%loop_id
	create_bjob_file(path, number_core, i,loop_id)
    
def do_step4(loop_id, group_count):
    for i in range(group_count):
	cmd = 'sh step4.sh %d %d '%(loop_id, i)
	os.system(cmd)
    
def do_step5(loop_id, group_count):
    print("This is step 5")
    cmd = "sh step5.sh %d %d"%(loop_id,group_count)
    os.system(cmd)

def loop(loop_id, group_count):
    print("Continue loop %d"%loop_id)
    do_step3(loop_id,group_count)
    
    while 1:
	check = 0
	for i in range(group_count):
	    if str(os.path.exists("loop%d/step3/group%d/step3.iqtree"%(loop_id,i))) == "True":
		check = check + 1
	if check < group_count:
	    time.sleep(10)
	else:
	    break
    print("Finish step3, continue to step4_5")
    do_step4(loop_id,group_count)
    do_step5(loop_id,group_count)
    while 1:
        check = 0
        for i in range(1,5):
            if str(os.path.exists("loop%d/step5/Q.step5.4x.%d"%(loop_id,i))) == "True":
                check = check + 1
        if check < 4:
            time.sleep(10)
        else:
            break
    print("Finish loop %d"%loop_id)

def main(sum_aln,group_aln,corr_thres,loop_undo):
    print("Start process...: ")
    loop_id = 1
    exit_loop = 0
    #prepare_folder(int(sum_aln))
    group_count = int(group_aln)
    while exit_loop == 0:
        if str(os.path.exists("un.do")) != "True":
	    loop(loop_id, group_count)
	else:
	    loop_id = int(loop_undo)
	    cmd = "rm un.do"
	    os.system(cmd)
	cmd = "sh normalized.sh %d"%loop_id
	os.system(cmd)
        corr1 = pearon_corr("loop%d/step5/Q.step3.4x.1"%loop_id,"loop%d/step5/Q.step5.4x.1.normalized"%loop_id)
        corr2 = pearon_corr("loop%d/step5/Q.step3.4x.2"%loop_id,"loop%d/step5/Q.step5.4x.2.normalized"%loop_id)
        corr3 = pearon_corr("loop%d/step5/Q.step3.4x.3"%loop_id,"loop%d/step5/Q.step5.4x.3.normalized"%loop_id)
        corr4 = pearon_corr("loop%d/step5/Q.step3.4x.4"%loop_id,"loop%d/step5/Q.step5.4x.4.normalized"%loop_id)
        print("Pearson correllation: %.8f, %.8f, %.8f, %.8f"%(corr1,corr2,corr3,corr4))
        if corr1 < float(corr_thres) or corr2 < float(corr_thres) or corr3 < float(corr_thres) or corr4 < float(corr_thres):
            cmd = "cp -rf loop%d loop%d"%(loop_id,loop_id+1)
            os.system(cmd)
	    cmd = "sh reset_models.sh %d %d"%(loop_id+1,group_count)
	    os.system(cmd)
	    loop_id = loop_id + 1
        else:
	    exit_loop = 1
            print("Finish process")

# call main function
# python mix_process.py 4x 29 51 1 0.999. This is for 4x type, 51 group, 29 aln each group, undo loop with id = 1 and corr thres is 0.999
if __name__ == '__main__':
    site_rate_type = sys.argv[1]
    sum_aln = sys.argv[2]
    group_aln = sys.argv[3]
    loop_undo = sys.argv[4]
    corr_thres = sys.argv[5]
    main(sum_aln,group_aln,corr_thres,loop_undo)
