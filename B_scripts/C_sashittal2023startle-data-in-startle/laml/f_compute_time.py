import os
import subprocess as sp
import re

import sys

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
   

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_data_in_startle/laml'

    data_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/sashittal2023startle_data_in_startle'

    folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]
    

    for folder in folders:
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)


        reps = [rep for rep in os.listdir(cur_data_path) if os.path.isdir(os.path.join(cur_data_path, rep))]

        for rep in reps:

            cur_rep_res_path = os.path.join(cur_res_path, rep)
            cur_rep_data_path = os.path.join(cur_data_path, rep)
        
            time_path = os.path.join(cur_rep_res_path, 'time.csv')

            data_prefix = folder + '\\' + rep
            print(data_prefix)
            nj_usage = os.path.join(cur_rep_res_path, 'nj_usage.log')
            nni_usage = os.path.join(cur_rep_res_path, 'nni_usage.log')
            laml_usage = os.path.join(cur_rep_res_path, 'laml_usage-1.log')
            time = get_wall_clock_time(nj_usage)
            time += get_wall_clock_time(nni_usage)
            time += get_wall_clock_time(laml_usage)
        

            with open(time_path, 'w', newline="") as tf:
                tf.write(f"{time}\n")
            #else:
                #os.remove(score_path)
        
        

if __name__ == '__main__':

    main()