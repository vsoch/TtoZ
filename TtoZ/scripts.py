#!/usr/bin/env python

#TtoZ   Convert T score brain statistical map to Z score map

#  USAGE: 
#  TtoZ [t_stat_map] [dof] --output_nii=z_stat_map.nii
#  TtoZ T_score_map.nii 32 --output_nii=Z_score_map.nii

# This script converts a T distribution brain map with dof
# degrees of freedom to a Z score map (standard normal) with
# mean 0, standard deviation 1. The algorithm is modified for
# brain images, and originally published here:
# http://www.stats.uwo.ca/faculty/aim/2010/JSSSnipets/V23N1.pdf

import sys
import os
import argparse
import numpy as np
import nibabel as nib
from scipy.stats import norm, t


def main():
  parser = argparse.ArgumentParser(
  description="Convert a whole brain T score map to a Z score map without loss of precision for strongly positive and negative values.")
  parser.add_argument("--t_stat_map", help="T-score statistical map in the form of a 3D NIFTI file (.nii or .nii.gz).", type=nifti_file, dest='t_stat_map', required=True)
  parser.add_argument("--dof", dest="dof",help="Degrees of freedom (eg. for a two-sample T-test: number of subjects in group - 2)",required=True,type=int)
  parser.add_argument("--output_nii", dest='output_nii', help="The name for the output Z-Score Map.",type=str,default="z_stat_map.nii")
  args = parser.parse_args()

  print "Converting map %s to Z-Scores..." %(args.t_stat_map)
  
  mr = nib.load(args.t_stat_map)
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
  p_values_t1 = t.cdf(t1, df = args.dof)
  z_values_t1 = norm.ppf(p_values_t1)

  # Calculate p values for > 0
  p_values_t2 = t.cdf(-t2, df = args.dof)
  z_values_t2 = -norm.ppf(p_values_t2)
  Z[k1] = z_values_t1
  Z[k2] = z_values_t2

  # Write new image to file
  empty_nii = np.zeros(mr.shape)
  empty_nii[mr.get_data()!=0] = Z
  Z_nii_fixed = nib.nifti1.Nifti1Image(empty_nii,affine=mr.get_affine(),header=mr.get_header())
  nib.save(Z_nii_fixed,args.output_nii)

# From Chrisfilo alleninf
def nifti_file(string):
    if not os.path.exists(string):
        msg = "%r does not exist" % string
        raise argparse.ArgumentTypeError(msg)
    try:
        nii = nib.load(string)
    except IOError as e:
        raise argparse.ArgumentTypeError(str(e))
    except:
        msg = "%r is not a nifti file" % string
        raise argparse.ArgumentTypeError(msg)
    else:
        if len(nii.shape) == 4 and nii.shape[3] > 1:
            msg = "%r is four dimensional" % string
            raise argparse.ArgumentTypeError(msg)
    return string


if __name__ == '__main__':
    main()

