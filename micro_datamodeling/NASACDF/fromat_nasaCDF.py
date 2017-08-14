#-*-coding:utf8-*-
"""
releaseCDF
releaseCDF input/output filters
Written by Zahi Yang May 2017
- contains read function
"""

import pymongo
import time,datetime
import spacepy.datamodel as dm
from spacepy import pycdf

filename = 'ac_at_def_19970826_v01.cdf'
cdf_file = dm.fromCDF(filename)

def readCDF(filename,cdf_file):
    diction_attrs = {}
    diction_data = {}
    diction_attrs['_id'] = filename
    for key in cdf_file.attrs.keys():
        value = cdf_file.attrs[key]
        if not value == ' ':
            diction_attrs[key] = value
        else:
            diction_attrs[key] = None

    data_recorder = []
    keys = cdf_file.keys()
    for key in keys:
        if key == 'Epoch':
            for i in range(cdf_file[key].size):
                diction_data['Datas'] = {'time_stamp':time.mktime(cdf_file[key][i].timetuple()),
                'r_RTN':float(cdf_file['RTN_ATT'][i][0]),'t_RTN':float(cdf_file['RTN_ATT'][i][1]),'n_RTN':float(cdf_file['RTN_ATT'][i][2]),
                'x_GSE':float(cdf_file['GSE_ATT'][i][0]),'y_GSE':float(cdf_file['GSE_ATT'][i][1]),'z_GSE':float(cdf_file['GSE_ATT'][i][2]),
                'x_GCI':float(cdf_file['GCI_ATT'][i][0]),'y_GCI':float(cdf_file['GCI_ATT'][i][1]),'z_GCI':float(cdf_file['GCI_ATT'][i][2])}
                data_recorder.append(diction_data['Datas'])
    return diction_attrs,data_recorder

def release(filename):
    connection = pymongo.MongoClient()
    tdb = connection.CDF_Release
    post_attrs = tdb.attrs
    post_datas = tdb.data

    cdf_file = dm.fromCDF(filename)
    cdf = readCDF(filename,cdf_file)
    attrs_value = cdf[0]
    data_value = cdf[1]
    
    try:
        if post_attrs.find_one({'_id':filename}) == None: 
            post_attrs.insert(attrs_value)
            post_datas.insert(data_value)
        else:
            print 'the file attrs has been imported'
    except Exception as e:
        print '---------------wrong cdf---------------'


if __name__ == '__main__':
    filename = 'ac_at_def_19970826_v01.cdf'
    release(filename)
# print '----------------------'
# for key in keys:
    # print cdf_file[key].shape,key,cdf_file[key].attrs
# dm.toJSONheadedASCII('outFile.txt', cdf_file)
# dm.toJSONheadedASCII('outFile.json', cdf_file)
# dm.toHDF5('outFile.h5', cdf_file)