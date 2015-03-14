#!/usr/bin/python

#TtoZ   Convert T score brain statistical map to Z score map

#  USAGE: 
#  python TtoZ.py [input_nii] [dof] [output_nii]
#  python TtoZ.py T_score_map.nii 32 Z_score_map.nii

# This script converts a T distribution brain map with dof
# degrees of freedom to a Z score map (standard normal) with
# mean 0, standard deviation 1. The algorithm is modified for
# brain images, and originally published here:
# http://www.stats.uwo.ca/faculty/aim/2010/JSSSnipets/V23N1.pdf

import sys
import numpy as np
import nibabel as nib
from scipy.stats import norm, t


mr_file = sys.argv[1]
dof = int(sys.argv[2])
output_nii = sys.argv[3]
mr = nib.load(mr_file)

data = mr.get_data()

# Select just the nonzero voxels
nonzero = data[data!=0]

# We will store our results here
Z = np.zeros(len(nonzero))

# Select values less than or == 0, and greater than zero
c  = np.zeros(len(nonzero))
k1 = (nonzero <= c)
k2 = (nonzero > c)

# Subset the data into two sets
t1 = nonzero[k1]
t2 = nonzero[k2]

# Calculate p values for <=0
p_values_t1 = t.cdf(t1, df = dof)
z_values_t1 = norm.ppf(p_values_t1)

# Calculate p values for > 0
p_values_t2 = t.cdf(-t2, df = dof)
z_values_t2 = -norm.ppf(p_values_t2)
Z[k1] = z_values_t1
Z[k2] = z_values_t2

# Write new image to file
empty_nii = np.zeros(mr.shape)
empty_nii[mr.get_data()!=0] = Z
Z_nii_fixed = nib.nifti1.Nifti1Image(empty_nii,affine=mr.get_affine(),header=mr.get_header())
nib.save(Z_nii_fixed,output_nii)
