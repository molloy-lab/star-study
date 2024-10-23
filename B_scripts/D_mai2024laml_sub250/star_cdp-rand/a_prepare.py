import os
import subprocess as sp
import shutil



def add_outgroup(newick, outgroup='0'):
    """
    Adds an outgroup to a Newick string.
    The Newick tree is assumed to end with a semicolon.
    The outgroup is added by modifying the base call with a new root that includes the outgroup.
    """
    # Remove the last semicolon and then add the outgroup
    newick_trimmed = newick.strip()[:-1]  # Remove semicolon and any extra whitespace
    return f"({outgroup},{newick_trimmed});"


def process_newick_file(input_file, output_file, outgroup):
    """
    Reads a file with Newick strings, adds an outgroup to each, and writes them to a new file.
    """
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            updated_newick = add_outgroup(line, outgroup)
            outfile.write(updated_newick + '\n')



def main():

    data_path = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/mai2024laml_sub250"

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/star_cdp-rand'
    paup_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/paup'

    folders = [f for f in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, f))]
    
    for folder in folders:
        cur_paup_path = os.path.join(paup_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)
        
        if not os.path.exists(cur_res_path):
            os.mkdir(cur_res_path)
        

     
            
        paup_usage_path = os.path.join(cur_paup_path, 'paup_usage.log')
        paup_search_space_path = os.path.join(cur_paup_path, 'paup_trees.trees')
            
        data_prefix = folder 
        print(data_prefix)
            
            
        if not os.path.exists(os.path.join(cur_res_path, 'search_space.trees')):
            process_newick_file(paup_search_space_path, os.path.join(cur_res_path, 'search_space.trees'), 'OUTG')

        shutil.copy(paup_usage_path, os.path.join(cur_res_path, 'paup_usage.log'))

                
            

if __name__ == '__main__':

    main()