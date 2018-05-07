I solved the challenge using a simple Python server and some geometric insights.

Run server:

$ make

Run tests:

$ make tests


Description of solution:

A point is inside of a convex polygon if and only if a ray extending infinitely in one direction intersects the polygon exactly once. An edge case occurs if that ray is tangent to the polygon, which can only happen in the event the ray intersects a corner point. Each corner point is a part of two distinct edges so it will be count as two intersections, therefore this will not trigger a false positive.

To determine if two line segments intersect, we first find the point at which the infinite lines intersect. Then, we say that the segments intersect if the calculated intersection point is within the bounding box of both segments.

This solution runs in O(n) where n = # of defined boundary points.

The Request Handler calls the States logic by calling the checkPoint(point) method in line 99 in do_POST(), the POST request handler.



