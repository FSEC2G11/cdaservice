import numpy as np
import ctypes
import pathlib
import os
import json

from cdaengine.cfenginestructs import *

analysisresult = {}

class CfEngineTest:

    def __init__(self):   
        if os.name == 'nt':
            libname = str(os.path.join(pathlib.Path().absolute() / "cdaengine/cfengine.dll"))
            #os.add_dll_directory(os.getcwd())
        else:
            libname = 'libcfenginelinux.so'
            #cdll.LoadLibrary(str(os.path.join(pathlib.Path().absolute() / "cdaengine/libkaxlicvallinux.so")))
        print(libname)
        self.c_lib = ctypes.CDLL(libname)
        pass
        
    def printresults(self, result: vresult_o):
        print('Result Id = {0}'.format(result.id.decode()))
        analysisresult['Result Id'] = result.id.decode()
        print('Size = {0} x {1} x {2}'.format(result.rows, result.columns, result.slices))
        count = 0
        for k in range(result.slices):
            for i in range(result.rows):
                for j in range(result.columns):
                    print(result.data[count], end='\t')
                    analysisresult['Result' + str(count)] = result.data[count]
                    count = count + 1
            print()

    def printmodelinfo(self, minfo: vmodelinfo_o):
        print('Model Type = {0}'.format(minfo.type.decode()))
        print('Model Name = {0}'.format(minfo.name.decode()))
        print('Model Info = {0}'.format(minfo.info.decode()))
        print('Data count = {0}'.format(minfo.useddatacount))
        print('Set Component = {0}'.format(minfo.setcomponent))
        print('Max Component = {0}'.format(minfo.maxcomponent))
        analysisresult['Model Type'] = minfo.type.decode()
        analysisresult['Model Name'] = minfo.name.decode()
        #analysisresult['Model Info'] = minfo.info.decode()
        analysisresult['Data Count'] = minfo.useddatacount
        analysisresult['Set Component'] = minfo.setcomponent
        analysisresult['Max Component'] = minfo.maxcomponent


    def getcsvdata(self, file: str):
        data = np.genfromtxt(file, dtype=float, delimiter=',')
        return data

    def getrandomdata(self, size: int):
        sampl = np.random.uniform(low=5.0, high=13.3, size=(size,)).astype('float32', 'C')
        print(sampl.data.contiguous)
        return sampl

    def executesinglemodel(self, samplefile, modelfile):
        # csvfile = str(os.path.join(pathlib.Path().absolute() / "data/data.csv"))
        #csvfile = str(os.path.join(pathlib.Path().absolute() / "data/TestCase1/Data_1.csv"))
        #csvfile = str(os.path.join(pathlib.Path().absolute() / "data/TestCase2/Data_1.csv"))

        # file = str(os.path.join(pathlib.Path().absolute() / "data/SampleModels.vpb"))

        # PLS Model
        #csvfile = str(os.path.join(pathlib.Path().absolute() / "datafiles/samples/Data_1.csv"))
        #file = str(os.path.join(pathlib.Path().absolute() / "datafiles/models/TestModel1.vpb"))

        # SIMCA Model
        #csvfile = str(os.path.join(pathlib.Path().absolute() / "data/TestCase2/Data_1.csv"))
        #file = str(os.path.join(pathlib.Path().absolute() / "data/TestCase2/TestCase2.vpb"))

        csvfile = samplefile
        file = modelfile
        csvdata = self.getcsvdata(csvfile)

        ret = self.c_lib.kax_loadfile(file.encode())
        if ret < 0:
            print('kax_loadfile returned error {0}'.format(ret))
            return
        fileid = ret

        kax_getmodels = self.c_lib.kax_getmodels
        kax_getmodels.argtypes = [c_int, POINTER(POINTER(vmodel_o)), POINTER(c_int)]
        kax_getmodels.restype = c_int

        vmodel_o_mem = POINTER(vmodel_o)()
        size = c_int()
        ret = kax_getmodels(fileid, byref(vmodel_o_mem), byref(size))
        if ret < 0:
            print('kax_getmodels returned error {0}'.format(ret))
            return
        print("Models Count: {}".format(size.value))

        kax_getmodelinfo = self.c_lib.kax_getmodelinfo
        kax_getmodelinfo.argtypes = [POINTER(vmodel_i), POINTER(vmodelinfo_o)]
        kax_getmodelinfo.restype = c_int

        vmi = vmodel_i()
        vminfo = vmodelinfo_o()
        vmip = vmodel_i()
        vminfop = vmodelinfo_o()

        for i in range(size.value):
            # print(vmodel_o_mem[i].name.decode())
            # print(vmodel_o_mem[i].type.decode())
            # print(vmodel_o_mem[i].fileid)
            # print(vmodel_o_mem[i].id.decode())
            vmi.fileid = vmodel_o_mem[i].fileid
            vmi.id = vmodel_o_mem[i].id
            ret = kax_getmodelinfo(byref(vmi), byref(vminfo))
            if ret < 0:
                print('kax_getmodelinfo returned error {0}'.format(ret))
                continue

            # Use PLS and SIMCA Models only for prediction
            if vmodel_o_mem[i].type.decode() == 'simcamodel' or vmodel_o_mem[i].type.decode() == 'pls':
                vmip.fileid = vmi.fileid
                vmip.id = vmi.id
                vminfop = vminfo

        self.printmodelinfo(vminfop)

        kax_getheaders = self.c_lib.kax_getheaders
        kax_getheaders.argtypes = [POINTER(vmodel_i), c_int, POINTER(vstringdata_io)]
        kax_getheaders.restype = c_int

        # using first model from kax_getmodels output
        headers = vstringdata_io()
        htype = c_int(0)
        ret = kax_getheaders(byref(vmip), htype, byref(headers))
        if ret < 0:
            print('kax_getheaders returned error {0}'.format(ret))
            return
        for i in range(headers.count):
            print(headers.names[i].decode(), end='\t')
        print()

        kax_initmodel = self.c_lib.kax_initmodel
        kax_initmodel.argtypes = [POINTER(vmodel_i), c_int]
        kax_initmodel.restype = c_int

        ret = kax_initmodel(byref(vmip), -1)
        if ret < 0:
            print('kax_initmodel returned error {0}'.format(ret))
            return

        modelid = ret

        if csvdata.ndim == 1:
            rows = 1
        else:
            rows, columns = csvdata.shape

        for r in range(rows):
            data1 = csvdata if rows == 1 else csvdata[[r], :]
            data = data1.astype('float32', 'C')
            #data = self.getrandomdata(vminfop.useddatacount)
            vi = vdata_i()
            vi.data = data.ctypes.data_as(POINTER(c_float))
            vi.columns = data.size
            vi.rows = 1
            vi.slices = 1

            results = vmodelresults_o()

            kax_analyze = self.c_lib.kax_analyze
            kax_analyze.argtypes = [POINTER(vdata_i), c_int, POINTER(vmodelresults_o)]
            kax_analyze.restype = c_int

            ret = kax_analyze(byref(vi), modelid, byref(results))
            if ret < 0:
                print('kax_analyze returned error {0}'.format(ret))
                return
            for i in range(results.count):
                rid = results.results[i].id.decode()
                if rid == 'ynewpred' or rid == 'classname':
                    self.printresults(results.results[i])

        kax_closemodel = self.c_lib.kax_closemodel
        kax_closemodel.argtypes = [c_int]
        kax_closemodel.restype = c_int

        kax_closemodel(modelid)

        kax_unloadfile = self.c_lib.kax_unloadfile
        kax_unloadfile.argtypes = [c_int]
        kax_unloadfile.restype = c_int

        kax_unloadfile(fileid)

        return analysisresult

