import os

dirs = [
"../smallGameClient/Assets/Plugins",
"../tankServer/packages",
".",
]

files = [
"src/ProtocolBuffers/bin/Debug/Google.ProtocolBuffersLite.dll",
"src/ProtocolBuffers/bin/Debug/Google.ProtocolBuffersLite.pdb"
]

for f in files:
	for d in dirs:
		cmd = "cp %s %s" % (f, d)
		print(cmd)
		os.system(cmd)


files2 = [
"src/ProtoGen/bin/Debug/ProtoGen.exe",
]

dirs2 = [
"./"
]
for f in files2:
	for d in dirs2:
		cmd = "cp %s %s" % (f, d)
		print(cmd)
		os.system(cmd)
