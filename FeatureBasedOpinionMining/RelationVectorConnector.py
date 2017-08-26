from __future__ import division
import math
import numpy as np

# all helper methods
def euclidean_distance(v1, v2):
    return np.linalg.norm(v1 - v2)

def connectionVec(v1,v2):
    return v1 - v2;

def cosine_distance(u, v):
    """ Returns the cosine of the angle between vectors v and u. This is equal to u.v / |u||v|.  """
    return np.dot(u, v) / (math.sqrt(np.dot(u, u)) * math.sqrt(np.dot(v, v)))

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in degrees between vectors 'v1' and 'v2':
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return math.degrees(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)))

def cluster_centroid_vector(clusterOfVectors):
    centroid = np.mean(clusterOfVectors, axis=0)
    return centroid