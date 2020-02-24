import os
import pandas as pd
from defi import Desktop
# #####################################################################################################################
#   将经度作为一列保存至.csv中，纬度作为第二列保存至.csv中,还需要一列空列
#   然后运行程序
#
# #####################################################################################################################

path1 = Desktop + "\\a.csv"


def csvtokml(filename, savepath, cavfilepath):
    df = pd.read_csv(cavfilepath, header=None, usecols=[0, 1])  # 读经纬度，标记
    fullname = filename + '.kml'
    with open(os.path.join(savepath, fullname), 'a') as file:
        file.write('<?xml version="1.0" encoding="UTF-8"?>' + '\n')
        file.write('<kml xmlns="http://earth.google.com/kml/2.2">' + '\n')
        file.write('<Document>' + '\n')
        for num in range(df.shape[0]):
            file.write('<Placemark>' + '\n')
            des = "<description>" + str(df.iloc[num, 2]) + "</description>"
            coordinate = "<Point><coordinates>" + str(df.iloc[num, 0]) + "," + str(
                df.iloc[num, 1]) + ",0</coordinates></Point>"  # 此处0代表海拔，如果有海拔，可更改
            file.write(des + '\n')
            file.write(coordinate + '\n')
            file.write('</Placemark>' + '\n')
        file.write('</Document>' + '\n')
        file.write('</kml>' + '\n')


csvtokml('test', Desktop, path1)
