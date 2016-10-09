# -*- coding: utf-8 -*-
"""
Created on Sun Oct 09 09:51:28 2016

@author: lipei
"""

#import sys
#reload(sys)
#sys.setdefaultenconding('utf-8')
import os
import zipfile 
import shutil 
import pdb
import copy
from collections import OrderedDict
class Homework:
    def __init__(self,path,testFile,result,zipFiles=None,zipDirs=None):
        self.path=path
        self.testFile=testFile
        if not zipFiles:
            zipFiles=list()
        if not zipDirs:
            zipDirs=list()
        self.zipFiles=zipFiles
        self.zipDirs=zipDirs
        self.result=OrderedDict()
        self.initResult(result)
    def initResult(self,r):
        for i in r:
            self.result[str(i)]=0
    def __zipfiles(self):
        dirs=os.listdir(self.path)
        for d in dirs:
            if d.endswith('zip'):
                self.zipFiles.append(os.path.abspath(d))
    def nums(self,fstr):
        for index ,e in enumerate(fstr):
            if '1'==e and fstr[index+1]!=' ':
                tmps=fstr[index:index+9]
                #pdb.set_trace()
                break
            else:
                tmps=fstr
        return tmps
    def extractNum(self,fname):
        flist=list(os.path.split(fname))
        #print flist
        
        tmps=self.nums(flist[-1])
      #  pdb.set_trace()
        print tmps
        self.result[tmps]=0;
        return os.path.join(flist[0],tmps)
            
    def unzip_dir(self):
        self.__zipfiles()
        print self.zipFiles
        for zipF in self.zipFiles:
           # pdb.set_trace()
            #print (zipF[:-4])
            #pdb.set_trace()
            numpath=self.extractNum(zipF[:-4])
            
           # pdb.set_trace()
            self.zipDirs.append(numpath)
            if not os.path.exists(numpath):
                os.mkdir(numpath)
                
            srcZip=zipfile.ZipFile(zipF,'r')
            for eachFile in srcZip.namelist():
                #print 'eachfile:',eachFile
                if type(eachFile) is unicode:
                    eachFileCopy=eachFile.encode('utf8')
                else:
                    eachFileCopy=eachFile
                   # print eachFile
                
                #pdb.set_trace()
                eachFileName=os.path.normpath(os.path.join(numpath,eachFileCopy))
                #print 'eachFileName: ',eachFileName
                eachDirName=os.path.dirname(eachFileName)
              #  print 'eachDirName:',eachDirName
                if not os.path.exists(eachDirName):
                    try:
                        os.mkdir(eachDirName)
                    except:
                        pass
                if eachFileName.endswith('.h')or eachFileName.endswith('.cpp'):
                   
                    fd=open(eachFileName,'w')
                    fd.write(srcZip.read(eachFile))
                    fd.close()
                    try:
                        shutil.copy(eachFileName,numpath)
                    except:
                        pass
            srcZip.close()
    def checkMain(self,f):
        with open(f,'r') as cpp:
            for line in cpp:
                if 'main' in line:
                    return True
        return False
    def checkStdafx(self,f):
        tmp=list()
        with open(f,'r') as cpp:
            for line  in cpp:
                if "stdafx.h" in line or 'targetver.h' in line or 'pragma' in line:
                    continue
                elif 'main' in line:
                    tmp.append('int main(int argc,char ** argv)\n')
                else:
                    tmp.append(line)
        with open(f,'w') as ncpp:
            for nline in tmp:
                ncpp.write(nline)
                
    def compileCpp(self):
        for path in self.zipDirs:
            #pdb.set_trace()
            #print path
            for f in os.listdir(path):
                if f.endswith('.cpp') and not self.checkMain(os.path.normpath(os.path.join(path,f))):
                    self.checkStdafx(os.path.normpath(os.path.join(path,f)))
                    shutil.copy(self.testFile,path)
                elif f.endswith('.h') or f.endswith('.cpp'):
                    self.checkStdafx(os.path.normpath(os.path.join(path,f)))
           # pdb.set_trace()
            os.system('g++ -std=c++11 -o {0}/test {0}/*.h {0}/*.cpp'.format(path))
            os.system('g++ -o {0}/test {0}/*.h {0}/*.cpp'.format(path))
            key=list(os.path.split(path))[-1]
            if os.path.exists('{0}/test'.format(path)):
                os.system('{0}/test > {0}/test.result'.format(path))
                self.result[key]=self.computeResult('{0}/test.result'.format(path))
            else:
                self.result[key]=60
                
            
        #print flist
            
    def computeResult(self,f):
        result=list()
        with open(f,'r') as rs:
            for r in rs:
                try:
                    result.append(int(r))
                except:
                    result.append(60)
        if result==[]:
            return 60
        else:
            return max(result)
    def save(self):
        with open('result.csv','w') as r:
            for key,value in self.result.items():
                r.write(str(key))
                r.write(',')
                r.write(str(value))
                r.write('\n')
            
        
if __name__=='__main__':
    path=r'.'    
    testFile=r'/home/lipei/cpp/hwpy/hmpy/LibArray.cpp'
    import numpy as np
    students='students.txt'
    s=np.loadtxt(students,'int')
    h=Homework(path,testFile,s)
    h.unzip_dir()
    h.compileCpp()
    h.save()
   
        
