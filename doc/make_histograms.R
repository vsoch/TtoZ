afni = "zstat_afni.nii"
original = "tfMRI_LANGUAGE_STORY.nii_tstat1.nii.gz"
ttz = "zstat_ttz.nii"
nosplit = "zstat_nosplit.nii"

library(Rniftilib)
library(plyr)
library(reshape2)
library(ggplot2)
library(scales)
library(gridExtra)

#################### Read in nonzero voxels data

get_data = function(nifti_file){
  mr = nifti.image.read(nifti_file,read_data=1)
  mr = as.vector(mr[,,,1])
  mr = mr[mr!=0]
  mr = melt(mr)
  return(mr)
}

afni = get_data(afni)
original = get_data(original)
ttz = get_data(ttz)
nosplit = get_data(nosplit)
data = list(original=original,afni=afni,nosplit=nosplit,ttz=ttz)

#################### Plot each one
colors = c("tomato","slateblue1","plum1","honeydew1")
map_types = c("t-stat map","z-stat map","z-stat map","z-stat map")

# Make the ggplots

make_plot = function(df,n,image_name,map_type){
return(ggplot(df,aes(x=value, fill=colors[n])) + 
  geom_density(alpha=0.25,binwidth=1) +
  theme(legend.position="none") +
  xlim(-67,37) +
  xlab(paste(image_name,map_type)) +
  guides(fill=FALSE))
}

plot1 = make_plot(data[[1]],n,names(data[1]),map_types[1])
plot2 = make_plot(data[[2]],n,names(data[2]),map_types[2])
plot3 = make_plot(data[[3]],n,names(data[3]),map_types[3])
plot4 = make_plot(data[[4]],n,names(data[4]),map_types[4])
g = arrangeGrob(plot1,plot2,plot3,plot4,ncol=4)
ggsave(file="histograms.png",g)

