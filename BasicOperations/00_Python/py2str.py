#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
Function:
銆愭暣鐞嗐€慞ython涓瓧绗︾紪鐮佺殑鎬荤粨鍜屽姣旓細Python 2.x鐨剆tr鍜寀nicode vs Python 3.x鐨刡ytes鍜宻tr
http://www.crifan.com/summary_python_string_encoding_decoding_difference_and_comparation_python_2_x_str_unicode_vs_python_3_x_bytes_str

Author:     Crifan
Verison:    2012-11-29
-------------------------------------------------------------------------------
"""

def python2xStrToUnicode():
    strUtf8 = 'w我哦我我我'
    print strUtf8.decode('UTF-8')
    print strUtf8.decode('gb2312')
    print "type(strUtf8)=",type(strUtf8); #type(strUtf8)= <type 'str'>
    decodedUnicode = strUtf8.decode("UTF-8");
    print "You should see these unicode zh-CN chars in windows cmd normally: decodedUnicode=%s"%(decodedUnicode); #You should see these unicode zh-CN chars in windows cmd normally: decodedUnicode=1.姝ゅ鏄疷TF-8缂栫爜鐨勪腑鏂囧瓧绗� ...... 杞崲涓哄搴旂殑锛堟澶勭殑GBK锛夌紪鐮佺殑锛夛紱
    
###############################################################################
if __name__=="__main__":
    python2xStrToUnicode();