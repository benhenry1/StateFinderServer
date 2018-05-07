import unittest
from stateserver import StatesData

class TestStateMethods(unittest.TestCase):

	#SegmentContains checks that a point is within a segment's BoundingBox
	def testSegmentContains(self):
		statesData = StatesData()
		line = ((0,0), (1,1))
		point = (0.5, 0.5)
		self.assertTrue(statesData.segmentContains(line, point))

		#Not on the line, but in the BB so should be true
		point = (0.25, 0.25)
		self.assertTrue(statesData.segmentContains(line, point))

		#Not in the BB in 1 axis
		point = (0.5, 10)
		self.assertFalse(statesData.segmentContains(line, point))

		#Not in BB on 2 axes
		point = (10, 10)
		self.assertFalse(statesData.segmentContains(line, point))

		#Edge case
		point = (1, 1)
		self.assertTrue(statesData.segmentContains(line, point))
		return;

	#Test IntersectsRight given a point and a segment
	def testIntersectsRight(self):
		statesData = StatesData()
		line = ((5,0), (5,10))
		point = (-1, -1)

		#Underneath the segment
		self.assertFalse(statesData.intersectsRight(point, line))

		#To the right of the segment
		point = (6, 5)
		self.assertFalse(statesData.intersectsRight(point, line))

		#intersect in center
		point = (0, 5)
		self.assertTrue(statesData.intersectsRight(point, line))

		#intsersects at endpoint
		point = (0, 0)
		self.assertTrue(statesData.intersectsRight(point, line))

		#Corner case
		point = (5, 0)
		self.assertTrue(statesData.intersectsRight(point, line))
		return;

		#far away
		point = (-100, 3)
		self.assertTrue(statesData.intersectsRight(point, line))

		#nonvertical boundary
		line = ((0, 0), (10, 10))
		point = (0, 5)
		self.assertTrue(statesData.intersectsRight(point, line))

	def testStates(self):
		statesData = StatesData()
		#Centroid of a few states
		cali = (-119.4179, 36.77)
		penn = (-77.036133, 40.513799)
		texas= (-99.9, 31.9686)

		self.assertEqual(statesData.checkPoint(cali), ["California"])
		self.assertEqual(statesData.checkPoint(penn), ["Pennsylvania"])
		self.assertEqual(statesData.checkPoint(texas),["Texas"])


if __name__ == '__main__':
	unittest.main()