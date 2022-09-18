from ctypes import *


class vmodel_o(Structure):
    _fields_ = [("name", c_char_p),
                ("type", c_char_p),
                ("fileid", c_int),
                ("id", c_char_p)]


class vmodel_i(Structure):
    _fields_ = [("fileid", c_int),
                ("id", c_char_p)]


class vmodelinfo_o(Structure):
    _fields_ = [("name", c_char_p),
                ("type", c_char_p),
                ("info", c_char_p),
                ("useddatacount", c_int),
                ("setcomponent", c_int),
                ("maxcomponent", c_int)]


class vresultinfo_o(Structure):
    _fields_ = [("id", c_char_p),
                ("name", c_char_p),
                ("row", c_int),
                ("columns", c_int),
                ("slices", c_int)]


class vresult_o(Structure):
    _fields_ = [("id", c_char_p),
                ("rows", c_int),
                ("columns", c_int),
                ("slices", c_int),
                ("data", POINTER(c_float))]


class vmodelresults_o(Structure):
    _fields_ = [("modelid", c_int),
                ("count", c_int),
                ("results", POINTER(vresult_o))]


class vresultresponse_i(Structure):
    _fields_ = [("count", c_int),
                ("resultcollection", POINTER(vmodelresults_o)),
                ("response", c_int)]


class vdata_i(Structure):
    _fields_ = [("rows", c_int),
                ("columns", c_int),
                ("slices", c_int),
                ("data", POINTER(c_float))]


class vstringdata_io(Structure):
    _fields_ = [("names", POINTER(c_char_p)),
                ("count", c_int)]


class vloaded_o(Structure):
    _fields_ = [("modelname", c_char_p),
                ("filename", c_char_p),
                ("fileid", c_int),
                ("modelid", c_int)]


class vloadedlist_o(Structure):
    _fields_ = [("models", POINTER(vloaded_o)),
                ("count", c_int)]
