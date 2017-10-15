#coding:utf8
import os
import json
import re
import sys
import shutil
import tempfile

print sys.path
sys.path.append(".")
#sys.path.append("protoc")
#sys.path.append("c#protoGen")

'''
{
	moduleName: {
		"id":name,

		"methodName":1,
		"methodName2": 2,
	}
}
'''


pat = re.compile('message (\w+)')

#msgID = 1
moduleID = 1

msgMap = {}
newMsgMap = {}
if os.path.exists('nameMap.json'):
	con = open('nameMap.json').read()
	msgMap = json.loads(con)

'''
分配一个模块的 消息ID
'''
def getMsgID(moduleName):
	#global msgID
	#global moduleID
	global msgMap
	msgID = 1
	for k in msgMap[moduleName]:
		if k != 'id':
			if msgMap[moduleName][k] >= msgID: #and k.find('Push') == -1:
				msgID = msgMap[moduleName][k]+1
	return msgID


'''
Push Msg ID
'''
'''
def getPushMsgID(moduleName):
	global msgMap
	msgID = 1000
	for k in msgMap[moduleName]:
		if k != 'id':
			if msgMap[moduleName][k] >= msgID:
				msgID = msgMap[moduleName][k]+1
	return msgID				
'''


'''
分配一个模块ID
'''
def getModuleID(modName):
	global moduleID
	global msgMap
	for k in msgMap:
		if msgMap[k]["id"] >= moduleID:
			moduleID = msgMap[k]["id"]+1
	if moduleID >= 256:
		raise Exception("Module Id too Big "+modName+" "+moduleID)
	return moduleID



f1 = os.listdir('protos')
#f1 = ["CommonProtoc.proto", "McpProtoc.proto"]
allProtos = []
for i in f1:
	if i.find('.proto') != -1  and i.find("dump") == -1 and i.find('.swp') == -1:
		modName = i.replace('.proto', '')
		if msgMap.get(modName) == None and modName[0] == 'M':
			msgMap[modName] = {"id":getModuleID(modName)}
		#newMsgMap[modName] = {}	
			
		allProtos.append(i)

		profile = open("protos/"+i).read()
		#all Messsage
		mat = pat.findall(profile)
		for n in mat:
			if msgMap.get(modName) != None and msgMap[modName].get(n) == None:
				if n[:2] == 'CG' or n[:2] == 'GC':
					print "Add Name is", n
					#if n.find("Push") != -1:
					#	msgMap[modName][n] = getPushMsgID(modName)
					#else:
					msgMap[modName][n] = getMsgID(modName)
			newMsgMap[n] = True

#检查是否有MsgName 在nameMap.json 里面但是不在 proto里 表示这个Message被删除了 可以从MsgName 中去掉
cleanMsgMap = {}
for mod in msgMap:
	newMod = {}
	for msg in msgMap[mod]:
		if msg != 'id':
			if newMsgMap.get(msg) != None:
				newMod[msg] = msgMap[mod][msg]
		else:
			newMod["id"] = msgMap[mod]["id"]
	cleanMsgMap[mod] = newMod

msgMap = cleanMsgMap

						
comStr = ''
for a in allProtos:
	comStr += 'protos/%s ' % (a)

print "all protos"

print "CMDIs"
fullCMD = 'mono ProtoGen.exe %s protos/google/protobuf/csharp_options.proto protos/google/protobuf/descriptor.proto --proto_path=protos' % (comStr)
print fullCMD
#print comStr
os.system(fullCMD)


def Main():
	if os.path.exists("temp"):
		#os.system("rm -r temp")
		shutil.rmtree("temp")
	#os.system('cp -r protos temp')

	shutil.copytree("protos", "temp")

	allF = os.listdir('temp')
	csharpRep = '''
	import "google/protobuf/csharp_options.proto";
	option (google.protobuf.csharp_file_options).namespace = "MyLib";
	option (google.protobuf.csharp_file_options).umbrella_classname = "CommonProtoc";
	'''
	newoption = '''
	option optimize_for = LITE_RUNTIME;
	'''

	comStr2 = ''
	for p in allF:
	    if p.find('.dump') == -1 and p.find('.swp') == -1 and p.endswith('.proto'):
	        name = os.path.join('temp', p)
	        if not os.path.isdir(name):
	            con = open(name).readlines()
	            ncon = ''
	            for l in con:
	                #if l.find('csharp') == -1 and l.find('optimize_for') == -1:
	                    ncon += l
	                    
	            #con = con.replace(csharpRep, '')
	            f = open(name, 'w')
	            f.write(ncon)
	            f.close()
	            comStr2 += name+" "

	print 'cmdstr'
	print comStr2
	shutil.rmtree("temp")
		
		
		
			
	f = os.listdir('.')
	delFile = [
	'Util2.cs',
	'Util3.cs',
	'CSharpOptions.cs',
	'DescriptorProtoFile.cs',
	]
	for i in f:
		#if i.find('.cs') != -1 and i.find(".csproj") == -1 :
		if i.endswith(".cs"):
			if i in delFile:
				os.remove(i)
			else:
				#os.system('mv %s cs/%s' % (i, i))
				shutil.move(i, "cs/%s" % (i))

	f = open('nameMap.json', 'w')
	f.write(json.dumps(msgMap, indent=4, sort_value=True, separators=(', ', ': ')))
	f.close()


	import GenUtilFile
	GenUtilFile.GenUtil(msgMap.values())

	#os.system('cp UpdateSln.py cs/')
	shutil.copy2("UpdateSln.py", "cs/")
	shutil.copy2("protoDll.csproj ", "cs/")
	shutil.copy2("Google.ProtocolBuffersLite.dll", "cs/")
	#os.system('cp protoDll.csproj cs/')
	#os.system('cp Google.ProtocolBuffersLite.dll cs/')
	#os.system("cp protoDll2.csproj protoDll.csproj")

	os.chdir('cs')
	os.system('python UpdateSln.py')
	os.system('xbuild new.csproj')
	os.chdir('..')


	#U3D = '/Users/liyong/Desktop/allUnity/Assets/Plugins'
	U3D = '../smallGameClient/Assets/Plugins'
	#os.system('cp cs/obj/Debug/protoDll.dll %s' % (U3D))
	shutil.copy2("cs/obj/Debug/protoDll.dll", U3D)

	#U3D = '/Users/liyong/Desktop/allUnity/Assets/scripts/util'
	U3D = '../smallGameClient/Assets/scripts/util'
	#os.system('cp Util2.cs %s' % (U3D))
	shutil.copy2("Util2.cs", U3D)


	#U3D = '/Users/liyong/Desktop/allUnity/Assets/Resources'
	U3D = '../smallGameClient/Assets/Resources'
	#os.system('cp nameMap.json %s' % (U3D))
	shutil.copy2("nameMap.json", U3D)

	#Server = '/Users/liyong/Projects/SocketServer/packages'
	Server = '../tankServer/packages'
	#os.system('cp cs/obj/Debug/protoDll.dll %s' % (Server))
	shutil.copy2("cs/obj/Debug/protoDll.dll", Server)

	#Server2 = '/Users/liyong/Projects/SocketServer/SocketServer/bin/Debug'
	Server2 = '../tankServer/SocketServer/bin/Debug'
	#os.system('cp nameMap.json %s' % (Server2))
	shutil.copy2("nameMap.json", Server2)
	#os.system('cp cs/obj/Debug/protoDll.dll %s' % (Server2))
	shutil.copy2("cs/obj/Debug/protoDll.dll", Server2)


	f = open('Util2.cs', 'r')
	con = f.read();
	con = con.replace('using UnityEngine;', '')
	nf = open('Util3.cs', 'w')
	nf.write(con)
	nf.close()

	#Server3 = '/Users/liyong/Projects/SocketServer/SocketServer/Common/Util2.cs'
	Server3 = '../tankServer/SocketServer/Common/Util2.cs'
	#os.system('cp Util3.cs %s' % (Server3))
	shutil.copy2("Util3.cs", Server3)


Main()