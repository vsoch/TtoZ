#!/usr/bin/sh

t_stat_nii="tfMRI_LANGUAGE_STORY.nii_tstat1.nii.gz"

# The degrees of freedom is the number of subjects -2
dof=484

# Our output file
output_nii="Z_score_map.nii"

python ../TtoZ.py $t_stat_nii $dof $output_nii
