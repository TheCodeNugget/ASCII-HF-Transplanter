#Author: Ken The Nugget
#TODO: Delete This Comment
import pandas as pd
import argparse as ap
import numpy as np
import matplotlib.path as mpl
from re import sub
from pathlib import Path

def coordMask(coords, x, y):
	x0, y0, x1, y1 = map(int, coords.strip().split(','))
	assert x0 <= x1 and y0 <= y1, "Invalid Coordinates"

	#Creates a boolean mask at the x,y coordinates
	x, y = x.flatten(), y.flatten()
	points = np.vstack((x,y)).T

	#Marks the selected are as true on mask
	p = mpl.Path([(x0,y0-1), (x1, y0-1), (x1,y1), (x0,y1)])
	grid = p.contains_points(points)
	mask = grid.reshape(cols, rows)

	return pd.DataFrame(mask)

parser = ap.ArgumentParser(description = "Python Script for transfering data between heightmap in ASC format.")
parser.add_argument("fromfile", type = str, help = "Path of the Heightfile to cut from.")
parser.add_argument("tofile", type = str, help = "Path of the Heightfile to copy to.")
parser.add_argument("coords", type = str, help = "Bottom Left and Upper Right Coordinates of the area to be transfered. Format: X0,Y0,X1,Y1")
parser.add_argument("-o" ,"--output", type = str, default = "./out.asc", help = "Path of the output file. Default: out.asc")
args = parser.parse_args()

#Checking Files
from_path = Path(args.fromfile)
assert from_path.exists(), f"Heightfield {args.fromfile} does not exist"
assert from_path.suffix in [".asc"], f"{args.fromfile} needs to end with \".asc\""

to_path = Path(args.tofile)
assert to_path.exists(), f"Heightfield {args.tofile} does not exist"
assert to_path.suffix in [".asc"], f"{args.tofile} needs to end with \".asc\""

out_path = Path(args.output)
assert out_path.suffix in [".asc"], f"{args.output} needs to end with \".asc\""

#Reading Heightmap Header
file0 = open(from_path, 'r')
cols = int(sub('[^0-9.]','', file0.readline()))
rows = int(sub('[^0-9.]','', file0.readline()))
xcorner = int(float(sub('[^0-9.]','', file0.readline())))
ycorner = int(float(sub('[^0-9.]','', file0.readline())))
cellsize = int(float(sub('[^0-9.]','', file0.readline())))
file0.close

#Creates a boolean mask of the area to be copied
x, y = np.meshgrid(np.arange(xcorner, xcorner + cols * cellsize, cellsize), np.arange(ycorner + (rows - 1) * cellsize, ycorner - 1, - cellsize))
mask = coordMask(args.coords, x, y)

#Reads Heightmaps
data_fromfile = pd.read_csv(from_path,
							skiprows = 6,
							delim_whitespace = True,
							header = None
							)

data_tofile = pd.read_csv(to_path,
						  skiprows = 6,
						  delim_whitespace = True,
						  header = None
						  )

#Extracts Data from both files with the mask
data_fromfile = data_fromfile * mask
mask = mask != True
data_tofile = data_tofile * mask
out_data = data_fromfile + data_tofile

#Writes the Header of output
with open(out_path, 'w') as file:
	file.write("ncols	")
	file.write(str(cols))
	file.write("\n")
	file.write("nrows	")
	file.write(str(rows))
	file.write("\n")
	file.write("xllcorner	")
	file.write(str(xcorner))
	file.write("\n")
	file.write("yllcorner	")
	file.write(str(ycorner))
	file.write("\n")
	file.write("cellsize	")
	file.write(str(cellsize))
	file.write("\n")
	file.write("NODATA_value	-9999")
	file.write("\n")

#Writes the Height Data
out_data.to_csv(out_path,
				mode = 'a',
				header = False,
				index = False,
				sep = " ")
