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
import re
import pdb
from collections import OrderedDict
import time
def getTime():        
    return time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime())

class Homework:
    def __init__(self,path,testFile,result,zipFiles=None,zipDirs=None):
        self.path=os.path.abspath(path)
        self.testFile=os.path.abspath(testFile)
       # pdb.set_trace()
        self.checkStdafx(self.testFile)
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
                self.zipFiles.append(os.path.join(self.path,d))  
    def nums(self,fstr):
        num=re.findall(r'[0-9]+',fstr)
        if num==[]:
            return fstr
        else:
            lenN=map(len,num)
            return num[lenN.index(max(lenN))]
    def extractNum(self,fname):
        flist=list(os.path.split(fname))
        #print flist
        tmps=self.nums(flist[-1])
      #  pdb.set_trace()
        #print tmps
        self.result[tmps]=0;#初始化成绩
        return os.path.join(flist[0],tmps)#返回绝对路径
            
    def unzip_dir(self):
        self.__zipfiles()
       # print self.zipFiles
        for zipF in self.zipFiles:
            numpath=self.extractNum(zipF[:-4])
            self.zipDirs.append(numpath)
          #  pdb.set_trace()
            if not os.path.exists(numpath):
                os.mkdir(numpath)
           # print numpath
            try:
                srcZip=zipfile.ZipFile(zipF,'r')
                
            except:
                print zipF
                continue
            for eachFile in srcZip.namelist():
                if type(eachFile) is unicode:
                   # pdb.set_trace()
                    eachFileCopy=eachFile.encode('utf8')
                else:
                    eachFileCopy=eachFile
                eachFileName=os.path.normpath(os.path.join(numpath,eachFileCopy))
                eachFileName=eachFileName.replace(' ','')
                eachDirName=os.path.dirname(eachFileName)
                eachDirName=eachDirName.replace(' ','')
               
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
                        if self.checkMain(eachFileName):
                            os.remove(eachFileName)
                            continue
                    #    pdb.set_trace()
                        self.checkStdafx(eachFileName)
                        shutil.copy(eachFileName,numpath)
                    except:
                        pass
            shutil.copy(self.testFile,numpath)
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
                if "stdafx.h" in line:
                   # pdb.set_trace()
                    continue
                elif 'main' in line:
                    if '{' in line:
                        tmp.append('int main(int argc,char ** argv){\n')
                    else:
                        tmp.append('int main(int argc,char ** argv)\n')
                elif 'iostream' in line:
                    continue
                else:
                    tmp.append(line)
        with open(f,'w') as ncpp:
         #   pdb.set_trace()
            ncpp.write('#include<iostream>\n')
            for nline in tmp:
                ncpp.write(nline)
                
    def compileCpp(self):
	for path in self.zipDirs:
           # pdb.set_trace()
            os.system('g++ -std=c++11 -o {0}/test11 {0}/*.h {0}/*.cpp '.format(path))
            os.system('g++ -o {0}/test1 {0}/*.h {0}/*.cpp '.format(path))
            key=list(os.path.split(path))[-1]
            if os.path.exists('{0}/test.result'.format(path)):#remove old test.result file
                os.remove('{0}/test.result'.format(path))
            if os.path.exists('{0}/test1'.format(path)):
                os.system('{0}/test1 > {0}/test.result'.format(path))
                self.result[key]=self.computeResult('{0}/test.result'.format(path))
            if os.path.exists('{0}/test11'.format(path)):
                os.system('{0}/test11 >> {0}/test.result'.format(path))
                self.result[key]=self.computeResult('{0}/test.result'.format(path))
            else:
                self.result[key]=60
                
            
        #print flist
            
    def computeResult(self,f):
        result=list()
        with open(f,'r') as rs:
            for r in rs:
                try:
                    score=[int(num) for num in re.findall(r'[0-9]+',r) if 0<int(num)<=100]
                    result.append(max(score))
                except:
                    result.append(60)
        if result==[]:
            return 60
        else:
            return max(result)
    def save(self):
   	os.chdir(self.path)
	with open('result.csv','w') as r:
            for key,value in self.result.items():
                r.write(str(key))
                r.write(',')
                r.write(str(value))
                r.write('\n')
class RarHomework(Homework):
    def __init__(self,path,testFile,result,zipFiles=None,zipDirs=None):
        Homework.__init__(self,path,testFile,result)
        self.rarFile=list()
    def __rarfiles(self):
        dirs=os.listdir(self.path)
        for d in dirs:
            if d.endswith('.rar'):
               # pdb.set_trace()
                self.rarFile.append(os.path.join(self.path,d))  
    def filesOrDir(self,l):
        for f in l:
            if '.h' in f or '.cpp' in f:
                return True
        return False
    def hcppFile(self,p):
        for lists in os.listdir(p): 
            path = os.path.join(p, lists)
            if path.endswith('.cpp') or path.endswith('.h'):
                self.hcpp.append(path) 
            if os.path.isdir(path): 
                self.hcppFile(path) 
    def checkSpace(self,tmps):
        if ' ' in tmps:
            tmps=tmps.replace(' ','')
        return tmps
    def copyHCpp(self,path):
        if not self.hcpp:
            return
        for f in self.hcpp:
            if self.checkMain(f):
                os.remove(f)
                continue
            self.checkStdafx(f)
            fs=os.path.split(f)[-1]  
            shutil.move(f,os.path.join(path,fs))
    def unrar(self):
        self.__rarfiles()
       # print self.zipFiles
        print len(self.zipDirs)
        for rar in self.rarFile:
            self.hcpp=list()
            
            numpath=self.extractNum(rar[:-4])
            numpath=self.checkSpace(numpath)
            if not os.path.exists(numpath):
                os.mkdir(numpath)
            self.zipDirs.append(numpath)
           # shutil.copy(rar,numpath)
#            rarFile=os.path.split(rar)[-1]
#            noSpaceRarFile=self.checkSpace(rarFile)
            newRar=os.path.join(numpath,os.path.split(numpath)[-1]+'.rar')
            #pdb.set_trace()
            shutil.copy(rar,newRar)
            os.chdir(numpath)
            s1=os.system('rar x {}'.format(newRar))
            if s1>0:
                print rar
                continue
            
            self.hcppFile(numpath)
            #print self.hcpp
            #pdb.set_trace()
            self.copyHCpp(numpath)
            
            shutil.copy(self.testFile,numpath)
    def combine(self):
        self.unzip_dir()
        self.unrar()
        
       # self.zipDirs.excend(self.rar)
            
            
            

            
            
        
        
            
        
if __name__=='__main__':
    import sys
    if len(sys.argv)!=4:
        print 'usage: python homework.py homeworkDir testFilePath studentsNameFile'
        exit()
    path=sys.argv[1]    
    testFile=sys.argv[2]
    students=sys.argv[3]
    import numpy as np
    s=np.loadtxt(students,'int')
    r=RarHomework(path,testFile,s)
    r.unzip_dir()
    r.unrar()
    print len(r.zipDirs)
   # pdb.set_trace()
    r.compileCpp()
    r.save()
    
   # r.compileCpp()
   # r.save()
   
        
