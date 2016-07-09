#coding:utf8
import os
csharpRep = '''
import "google/protobuf/csharp_options.proto";
'''
newoption = '''
option optimize_for = LITE_RUNTIME;
'''

f1 = os.listdir('protos')
for i in f1:
	name = 'protos/'+i
	if i.find('.proto') != -1  and i.find("dump") == -1:
		con = open(name, 'r').read()
		if name.find('optimize_for') == -1:
			print 'write', name
			ncon = con.replace(csharpRep, csharpRep+newoption)
			wf = open(name, 'w')
			wf.write(ncon)
			wf.close()