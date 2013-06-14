#!/usr/bin/env python

import sys
import subprocess
import re
import os

#qaz@bob~/paramedia/gps/20120707$ gpsdump.0.09 -cu0 -gy -l"0" -f0
#Product: Flymaster Gps  SN00558  SW1.02a
#Track list:
# 2   07.07.12   17:26:41   00:21:10
# 3   07.07.12   17:06:21   00:08:43
# 4   07.07.12   15:24:37   00:13:48
# 5   21.06.12   15:06:38   03:39:49
# 6   29.05.12   18:17:43   01:23:33
# 7   17.05.12   13:12:49   18:12:15


def callGpsDump( args ):
	return subprocess.Popen( " ".join( args ) , stdout=subprocess.PIPE, shell=True ).stdout.read()

def main( argv ):
	argIter = iter( argv[1:] )
	
	gpsDumpExe = "gpsdump.0.09"
	comPort = "-cu0"
	gpsMake = "-gy"
	extraArgs = []
	
	for arg in argIter:
		if arg in [ "-a", "--gpsdump-args" ]:
			arg = argIter.next()
			if arg[ : 2 ] == "-c":
				comPort = arg
			elif arg[ : 2 ] == "-g":
				gpsMake = arg
			else:
				extraArgs.append( arg )
		elif arg in [ "-e", "--exe-path" ]:
			gpsDumpExe = argIter.next()		
		else:
			print "unknown arg", arg
			exit(-1)
	
	gpsDumpCallBase = [ gpsDumpExe, comPort, gpsMake ]  + extraArgs
		
	ret = callGpsDump( gpsDumpCallBase + [ "-f0", "-l0" ] )
	print ret
	
	tracks = []
	for line in ret.split('\n'):
		match = re.match('\s*(\d+)\s+([\d.]+)\s+([\d:]+)\s+([\d:]+).*', line )
		if match:
			#print match.group(0), match.group(1)
			tracks.append( [ match.group(1), match.group(2), match.group(3) ] )
		
	print("tracks: " + " ".join( [ t[0] for t in tracks] ) )
	print("list tracks to download (empty for all, s-e for ranged from s to and including e):")
	com = raw_input()
	
	runTracks = []
	if not com.strip():
		runTracks = tracks
	else:
		for n in com.split():
			trackstoadd = []
			#print n
			if '-' in n:
				s = int( n.split('-') [0] )
				e = int( n.split('-') [1] )
				trackstoadd = [ str( v ) for v in range( s, e+1 ) ]
			else:
				trackstoadd = [n]
			for track in trackstoadd:
				found = False
				for t in tracks:
					if track == t[0]:
						runTracks.append( t )
						found = True
				if not found:
					print("unknown track " + track )
					exit( 2 )
	#print runTracks
	#sys.exit(0)
		
	for t in runTracks:
		date = t[ 1 ].split( "." )
		dir = date[ 2 ] + date[ 1 ] + date[ 0 ]		
		name = t[ 2 ].replace( ":", "" )
		print( dir + " " + name )
		
		if not os.path.exists( dir ):
			os.mkdir( dir )
		ret = callGpsDump( gpsDumpCallBase + [ "-f"+t[0], "-l\""+os.path.join( dir, name ) + "\"" ] )
		print ret
		#ret = callGpsDump( [ "--noana", "-f"+t[0], "-l\""+os.path.join( dir, name ) + "_noana\"" ] )
		#print ret
		
		
	
	
	


if __name__ == "__main__":
	main( sys.argv )