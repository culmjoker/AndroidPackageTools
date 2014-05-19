#!/usr/bin/python
# coding=utf-8
import os
import shutil
import json

def readChannelfile(filename):
    f = file(filename)
    while True:
        line = f.readline().strip('\n')
        if len(line) == 0:
            break
        else:
            channelList.append(line);
    f.close()

def loadConfigFile(filename):
    f = file(filename)
    strJson="";
    while True:
        line = f.readline().strip('\n')
        if len(line) == 0:
            break
        else:
            strJson=strJson+line;
    f.close()
    config=json.loads(strJson)
    print '-------------------- config: load Success -------------------'
    return config

def backUpManifest():
    if os.path.exists('./AndroidManifest.xml'):
        os.remove('./AndroidManifest.xml')
    manifestPath = './temp/AndroidManifest.xml'
    shutil.copyfile(manifestPath, './AndroidManifest.xml')

def modifyChannel(value):
    tempXML = ''
    f = file('./AndroidManifest.xml')
    for line in f:
        if line.find(config['channle_key']) > 0:
            line = line.replace(config['channle_key'], value)
        tempXML += line
    f.close()

    output = open('./temp/AndroidManifest.xml', 'w')
    output.write(tempXML)
    output.close()
    
    unsignApk = r'./bin/%s_%s_unsigned.apk'% (easyName, value.replace(' ','_'))
    cmdPack = r'java -jar apktool.jar b temp %s'% (unsignApk)
    os.system(cmdPack)
    
    unsignedjar = r'./bin/%s_%s_unsigned.apk'% (easyName, value.replace(' ','_'))
    signed_unalignedjar = r'./bin/%s_%s_signed_unaligned.apk'% (easyName, value.replace(' ','_'))
    signed_alignedjar = r'./bin/%s_%s.apk'% (easyName, value.replace(' ','_'))
    cmd_sign = r'jarsigner -verbose -keystore %s -storepass %s -signedjar %s %s %s'% (keystore, storepass, signed_unalignedjar, unsignedjar, alianame)
    cmd_align = r'zipalign -v 4 %s %s' % (signed_unalignedjar, signed_alignedjar)
    os.system(cmd_sign)
    os.remove(unsignedjar)
    os.system(cmd_align)
    os.remove(signed_unalignedjar)
    
channelList = []
apkName=''
easyName=''
keystore=''
storepass=''
alianame=''
output_apk_dir=''
config=loadConfigFile('./config')
apkName = config['input_file']
easyName = apkName.split('.apk')[0]
keystore = config['keystore']
storepass = config['keystore_pwd']
alianame = config['alianame']
output_apk_dir=config['output']

if os.path.exists(output_apk_dir):
    shutil.rmtree(output_apk_dir)

readChannelfile(config['channel'])

print '-------------------- your channel values --------------------'
print 'channel list: ', channelList

cmdExtract = r'java -jar apktool.jar  d -f -s %s temp'% (apkName)

os.system(cmdExtract)

backUpManifest()
for channel in channelList:
    modifyChannel(channel)

if os.path.exists('./temp'):
    shutil.rmtree('./temp')
if os.path.exists('./AndroidManifest.xml'):
    os.remove('./AndroidManifest.xml')
print '-------------------- Done --------------------'
