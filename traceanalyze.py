#!/usr/bin/env python
import sys
	


def main( argv ):
	
	files = argv[1:]
	
	sum = 0
	for file in files:
		lineIter = open( file ).readlines().__iter__()
		secs = []
		pAlt = []
		for line in lineIter:
			line = line.strip()
			#print line
			if line == "<SecondsFromTimeOfFirstPoint>":
				for line in lineIter:
					line = line.strip()
					if line == "</SecondsFromTimeOfFirstPoint>":
						break
					secs += line.split()
			if line == "<PressureAltitude>":
				for line in lineIter:
					line = line.strip()
					if line == "</PressureAltitude>":
						break
					pAlt += line.split()
		assert( len( secs ) == len( pAlt ) )
		data = []
		for s,pa in zip( secs, pAlt):
			#print s,pa
			data.append( [ int(pa), int(s) ] )
		
		print file
		
		start = 0
		while start < len( data ):
			for i in xrange( start +1, len( data) ):
				if abs( data[ i ][ 0 ] - data[ start ][ 0 ]  ) > 2 :
					start = i - 1
					break
			end = start + 1
			maxPA = data[ start ][ 0 ]
			minPA = maxPA
			for i in xrange( end + 1, len( data) ):
				maxPA = max( maxPA, data[ i ][ 0 ] )
				minPA = min( minPA, data[ i ][ 0 ] )
				aDiff = abs( data[ i ][ 0 ] - data[ end ][ 0 ]  )
				aSlope = abs( data[ i ][ 0 ] - data[ end ][ 0 ]  ) / float( abs( data[ i ][ 1 ] - data[ end ][ 1 ]  ) )
				if  aDiff > 1 and aSlope > 0.1:
					end = i
				if i - end > 20:
					#end  -= 9
					break
			if ( maxPA - minPA ) > 10:
				print "  t:%6.2f" % ( (data[ end ][1] - data[ start ][1] )/60.0 ), " alt: %3d/%3d" % (minPA, maxPA), "    range: [%4d,%4d] (%4d)" % (start, end, len( data )), "    [%4d,%4d], [%4d,%4d]" % ( data[ start ][ 0 ], data[ start ][ 1 ], data[ end ][ 0 ], data[ end ][ 1 ] )
				sum += (data[ end ][1] - data[ start ][1] )
				start = end + 1
			else:
				start = start + 1
	print "sum:", sum/60.0



if __name__ == "__main__":
	main( sys.argv )