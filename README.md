# TtoZ

TtoZ is a python implementation of Hughett's t-to-z tranform for whole brain statistical maps. 

For background about the problem, see [Hughett's paper](doc/JStats_Hughett.pdf). For a detailed example of the problem pertaining to whole brain statistical maps, see [this ipython notebook](http://nbviewer.ipython.org/github/vsoch/TtoZ/blob/master/doc/t_to_z_procedure.ipynb). For a more concise summary of the particular problems addressed by Hughett's algorithm, as compared to traditional procedures using scipy see [this ipython notebook](http://nbviewer.ipython.org/github/vsoch/TtoZ/blob/master/doc/TtoZ_method_comparison.ipynb).  While we have not robustly tested against AFNI (3dcalc) and [FSLs](http://www.fmrib.ox.ac.uk/analysis/techrep/tr08ss1/tr08ss1.pdf), we have used both tools and see truncation in the distributions of Z values. [An image produced with AFNI's 3D calc](example/zstat_afni.nii) from the equivalent data in the example is included with this package.

# Installation

     pip install git+https://github.com/vsoch/TtoZ.git

# Usage


# Example

