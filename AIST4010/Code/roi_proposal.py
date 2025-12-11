import numpy as np
from skimage.morphology import skeletonize
from sklearn.cluster import DBSCAN

def get_roi_centroids(vessel_mask, downsample_factor=5, eps=15, min_samples=10):
    """
    Core logic for Stage 1 -> Stage 2 transition.
    Extracts candidate centroids from a binary vessel mask.
    """
    
    # 1. Skeletonize the vessel tree to get centerlines
    skeleton = skeletonize(vessel_mask > 0)
    points = np.argwhere(skeleton > 0)

    if len(points) < min_samples:
        return []

    # 2. Downsample points to speed up clustering
    sampled_points = points[::downsample_factor]

    # 3. Apply DBSCAN to cluster nearby points along branches
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(sampled_points)
    labels = clustering.labels_
    
    unique_labels = set(labels)
    if -1 in unique_labels: 
        unique_labels.remove(-1) # Remove noise

    centroids = []
    
    # 4. Calculate centroid for each cluster
    for label in unique_labels:
        cluster_mask = (labels == label)
        cluster_points = sampled_points[cluster_mask]
        
        # Simple geometric center of the cluster
        center = cluster_points.mean(axis=0).astype(int)
        centroids.append(center)

    return centroids

def crop_roi(volume, center, crop_size=96):
    """
    Extracts a fixed-size 3D crop around the center.
    Handles padding if crop goes out of bounds.
    """
    z, y, x = center
    d, h, w = volume.shape
    r = crop_size // 2

    # Calculate bounds
    z1, z2 = max(0, z-r), min(d, z+r)
    y1, y2 = max(0, y-r), min(h, y+r)
    x1, x2 = max(0, x-r), min(w, x+r)

    crop = volume[z1:z2, y1:y2, x1:x2]

    # Pad if crop is smaller than required size
    pad_z = (0, crop_size - (z2-z1))
    pad_y = (0, crop_size - (y2-y1))
    pad_x = (0, crop_size - (x2-x1))

    if any(p > 0 for p in pad_z + pad_y + pad_x):
        crop = np.pad(crop, (pad_z, pad_y, pad_x), mode='constant', constant_values=0)
        
    return crop