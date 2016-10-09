# -*- coding: utf-8 -*-
"""
Created on Sun Oct 09 09:51:28 2016

@author: lipei
"""

import os
import zipfile 
import sys
import shutil 
sys.setrecursionlimit(1000000) 
class Homework:
    def __init__(self,path,zipFiles=None,zipDirs=None):
        self.path=path
        if not zipFiles:
            zipFiles=list()
        if not zipDirs:
            zipDirs=list()
        self.zipFiles=zipFiles
        self.zipDirs=zipDirs
    def __zipfiles(self):
        dirs=os.listdir(self.path)
        for d in dirs:
            if d.endswith('zip')or d.endswith('rar'):
                self.zipFiles.append(os.path.abspath(d))
    def unzip_dir(self):
        self.__zipfiles()
        for zipF in self.zipFiles:
            self.zipDirs.append(zipF[:-4])
            if not os.path.exists(zipF[:-4]):
                os.mkdir(zipF[:-4])
                
            srcZip=zipfile.ZipFile(zipF,'r')
            for eachFile in srcZip.namelist():
                print 'eachfile:',eachFile
                eachFileName=os.path.normpath(os.path.join(zipF[:-4],eachFile))
                #print 'eachFileName: ',eachFileName
                eachDirName=os.path.dirname(eachFileName)
              #  print 'eachDirName:',eachDirName
                if not os.path.exists(eachDirName):
                    os.mkdir(eachDirName)
                if eachFileName.endswith('h')or eachFileName.endswith('cpp'):
                    print eachFileName
                    fd=open(eachFileName,'w')
                    fd.write(srcZip.read(eachFile))
                    fd.close()
                    shutil.copy(eachFileName,os.path.normpath(os.path.join(zipF[:-4],os.path.split(eachFile)[-1])))
            srcZip.close()
    def checkMain(self,f):
        with open(f,'r') as cpp:
            for line in cpp:
                if 'main' in line:
                    return True
        return False
    def compileCpp(self):
        for path in self.zipDirs:
            for f in os.listdir(path):
                if f.endswith('cpp') and not self.checkMain(os.path.abspath(f)):
                    #do copy
                
        
if __name__=='__main__':
    path=r'D:\c++\dataStructure'    
    h=Homework(path)
    h.unzip_dir()
    print h.zipFiles
    print h.zipDirs
        
