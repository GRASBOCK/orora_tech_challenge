import matplotlib.pyplot as plt
import netCDF4

# load dataset
dir="C:/Users/grasb/Downloads/Suomi-NPP_sample_data"
file="VNP02MOD_NRT.A2020233.1000.001.nc"
nc = netCDF4.Dataset(dir + "/" + file)

# extract data
m13_data = nc['observation_data']['M13'][:].T # really Transpose?

# plot
plt.imshow(m13_data, cmap='jet', interpolation='nearest')
plt.show()