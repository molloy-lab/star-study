import os
import subprocess as sp
import re

import sys
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('time_path', type=str, help="time_path")
parser.add_argument('score_path', type=str, help="score_path")
parser.add_argument("usage", type=str, help="usage")
args = parser.parse_args()
time_path = args.time_path
nj_usage = args.nj_usage
usage = args.usage
def get_wall_clock_time(file_path:str):
    time_regex = re.compile(r"Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): (.*:.*(:.*)?)")

    with open(file_path, 'r') as file:
        content = file.read()
        time_match = re.search(time_regex, content)
        if time_match:
            time_str = time_match.group(1)
            time_parts = time_str.split(":")
            if len(time_parts) == 3:
                hrs, mins, secs = float(time_parts[0]), float(time_parts[1]), float(time_parts[2])
                return hrs * 3600 + mins * 60 + secs
            elif len(time_parts) == 2:
                mins, secs = float(time_parts[0]),  float(time_parts[1])
                return mins * 60 + secs
    return None

def main():
   

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/bio_result/startle_nni'

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/KPTracer-Data"

    folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]
    

    for folder in folders:
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)
        
        if not os.path.exists(cur_res_path):
            os.mkdir(cur_res_path)
        
        


        # time_path = os.path.join(cur_res_path, 'original_cmat_to_nj_nni_time.csv')
        time_path = os.path.join(cur_res_path, time_path)

        data_prefix = folder
        print(data_prefix)
        # nj_usage = os.path.join(cur_res_path, 'unpruned_nj_usage.log')
        # usage = os.path.join(cur_res_path, 'original_cmat_to_nj_nni_usage.log')

        nj_usage = os.path.join(cur_res_path, nj_usage)
        usage = os.path.join(cur_res_path, usage)
        # time = get_wall_clock_time(nj_usage)
        time = get_wall_clock_time(usage)
        time += get_wall_clock_time(nj_usage)
        
        with open(time_path, 'w', newline="") as tf:
            tf.write(f"{time}\n")
            
        

if __name__ == '__main__':

    main()