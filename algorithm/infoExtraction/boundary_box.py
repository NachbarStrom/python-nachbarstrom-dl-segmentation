#!/usr/bin/python

# Find the minimum-area bounding box of a set of 2D points
#
# The input is a 2D convex hull, in an Nx2 numpy array of x-y co-ordinates. 
# The first and last points points must be the same, making a closed polygon.
# This program finds the rotation angles of each edge of the convex polygon,
# then tests the area of a bounding box aligned with the unique angles in
# 90 degrees of the 1st Quadrant.
# Returns the 
#
# Tested with Python 2.6.5 on Ubuntu 10.04.4
# Results verified using Matlab

# Copyright (c) 2013, David Butterworth, University of Queensland
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the Willow Garage, Inc. nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

#from numpy import *
import numpy as np
from pyproj import Proj
from shapely.geometry import shape
from scipy.spatial import ConvexHull

def py_ang(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'    """
    cosang = np.dot(v1, v2)
    sinang = np.linalg.norm(np.cross(v1, v2))
    return np.arctan2(sinang, cosang)

def minBoundingRect(points_2d):
    
    hull = ConvexHull(points_2d)
    
    # rectangle for image extraction
    imgLength = max(hull.max_bound - hull.min_bound)*1.1
    center = hull.min_bound + (hull.max_bound - hull.min_bound)/2.0
    minLon = center[0] - imgLength/2.0
    maxLon = center[0] + imgLength/2.0
    minLat = center[1] - imgLength/2.0
    maxLat = center[1] + imgLength/2.0
       
    lon = hull.points[:,0]
    lat = hull.points[:,1]
    
    # orientation using PCA
    coords = np.vstack([lat, lon])

    cov = np.cov(coords)
    evals, evecs = np.linalg.eig(cov)

    sort_indices = np.argsort(evals)[::-1]
    x_v1, y_v1 = evecs[:, sort_indices[0]]  # Eigenvector with largest eigenvalue
    #x_v2, y_v2 = evecs[:, sort_indices[1]]
    
    orientation = np.degrees(np.arctan2(y_v1,x_v1) + 0.5*py_ang(evecs[:,sort_indices[0]], evecs[:,sort_indices[1]]))
    
    pa = Proj("+proj=aea +lat_1=37.0 +lat_2=41.0 +lat_0=39.0 +lon_0=-106.55")
    
    x, y = pa(lon, lat)
    cop = {"type": "Polygon", "coordinates": [zip(x, y)]}
    area = shape(cop).area
        
    return (minLon, maxLon, minLat, maxLat, orientation, area, center) # rot_angle, area, width, height, center_point, corner_points
