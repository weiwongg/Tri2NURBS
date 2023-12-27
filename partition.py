from src.eigens import eigens
from src.morseSmaleQuadrangulation import morseSmaleQuadrangulation
from src.patches_search import conformal_patch_gen
from src.nurbs import approximate_mp_nurbs_surf
from src.io import write_to_bembel
import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input', help='Path to input quadmesh obj file.')
parser.add_argument('--num', help='How many eigen functions to compute.')
parser.add_argument('--start', help='Which eigen function you want to start.')
parser.add_argument('--id', help='Which eigen function is used to compute quad partion.')
parser.add_argument('--output', help='Path to output remeshed dat file.')

args = parser.parse_args()
input = args.input
num = int(args.num)
start = int(args.start)
id = int(args.id)
output = args.output

#Frist step: compute eigen functions
eigens(input, 'EigenFunctions', num)

#Second step: Morse Smale Quadrangulation
os.makedirs("./Quadrangulation",exist_ok=True)
morseSmaleQuadrangulation("EigenFunctions.vtu", "./Quadrangulation", num, start)

#Third step: singularities and separatrices 
pt_list, idx_patches = conformal_patch_gen(f'./Quadrangulation/EigenFunction{id}.obj')

#Fourth step: NURBS multi-patch surface approximation
max_deg = 3
ctrlpts_size = 8
degree_us,degree_vs,kv_us,kv_vs,ctrlpts_size_us,ctrlpts_size_vs,ctrlpts,weights=approximate_mp_nurbs_surf(pt_list, idx_patches,max_deg,ctrlpts_size)
    
#Final step: Write geo in the format of dat required by Bembel
write_to_bembel(degree_us, degree_vs, kv_us, kv_vs, ctrlpts_size_us, ctrlpts_size_vs, ctrlpts, weights, output)
