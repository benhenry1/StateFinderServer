import json
from http import server
import socketserver

class StatesData():
	statesDict = {}

	#Input: Point [x, y], Line ([x,y], [x2,y2])
	#Output: T/F Will the right-facing ray intersect the segment
	def intersectsRight(self, point, line):
		#Check the intersection point of the infinite lines
		#Confirm that the intersection point is a part of both segments
		xp = point[0]
		yp = point[1]
		xp1 = point[0] + 10000 # Create a horizontal ray from src point
		yp1 = point[1]

		x1 = line[0][0]
		y1 = line[0][1]
		x2 = line[1][0]
		y2 = line[1][1]

		#Vertical borders require a special case
		vertical = False

		#Generate line given segments
		slope1 = 0
		yint1  = yp;
		if (x2 - x1 == 0):
			slope2 = float("inf")
			vertical = True;
		else:
			slope2 = (y2 - y1) / (x2 - x1)
		yint2  = y1 - slope2 * x1

		#In case they're parallel, check intersection
		if (slope1 == slope2 and max(x1, x2) > xp and min(x1, x2) < xp):
			return True;

		#(x, y) is where the infinite lines intersect
		x = (yint2 - yint1) / (slope1 - slope2)
		y = slope1 * x + yint1

		#Confirm (x,y) is in BOTH line segments
		segment = (point, (xp1, yp1));

		#Special case for verical borders
		if vertical:
			x = x2
			y = yp

		#Return whether the intersection is a part of both segments
		return self.segmentContains(line, (x, y)) and self.segmentContains(segment, (x, y))

	#The point we calculated is on both infinite lines
	#So, we can assume that the point is in the segment
	#as long as it's in the segment's bounding box.
	def segmentContains(self, line, point):
		minx = min(line[0][0], line[1][0])
		miny = min(line[0][1], line[1][1])
		maxx = max(line[0][0], line[1][0])
		maxy = max(line[0][1], line[1][1])
		in_x_bb = point[0] >= minx and point[0] <= maxx
		in_y_bb = point[1] >= miny and point[1] <= maxy
		return in_x_bb and in_y_bb;

	#Build dict of state borders	
	def initializeStates(self):
		statesRaw = open("states.json", "r")
		for state in statesRaw:
			stateData = json.loads(state)
			self.statesDict[stateData['state']] = stateData['border']
		statesRaw.close()
		return 0;

	#Input: point (x, y)
	def checkPoint(self, point):
		if not self.statesDict:
			self.initializeStates();

		candidates = []
		#For each state
		for key in self.statesDict.keys():
			borderPoints = self.statesDict[key]
			sumHits = 0;
			#For each border point
			for i in range(len(borderPoints) - 1):
				line = (borderPoints[i], borderPoints[i+1])
				if self.intersectsRight(point, line):
					sumHits+=1;
			if sumHits == 1:
				candidates.append(key)
		return candidates;

class RequestHandler(server.BaseHTTPRequestHandler):
	statesClass = StatesData()
	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		post_data = self.rfile.read(content_length)

		point = self.decodeData(str(post_data))
		if point != None:
			result = self.statesClass.checkPoint(point)
			for item in result:
				self.wfile.write(bytes(item, 'utf8'))
				self.wfile.write(b'\n')
		else:
			self.wfile.write(b'Bad Input\n')

	#Returns (lon, lat) or None on error
	def decodeData(self, data):
		longitude = -181
		lattitude = -181
		try:
			two = data.split('&')
			for item in two:
				arg = item.split('=')
				arg[1] = arg[1].rstrip("'")
				if "lat" in arg[0]:
					lattitude = float(arg[1])
				elif "lon" in arg[0]:
					longitude = float(arg[1])

			#If lat or lon wasn't set, bad input
			if lattitude == -181 or longitude == -181:
				raise Exception
			
			return (longitude, lattitude)
		except:
			return None;


#Run server
def init():
	PORT = 8080
	Handler = RequestHandler
	httpd = socketserver.TCPServer(("", PORT), Handler)
	print("Listening on port " + str(PORT))
	httpd.serve_forever()

if __name__ == "__main__":
	init()