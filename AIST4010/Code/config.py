import os

class Config:
    # Paths
    RAW_DATA_DIR = "./data/raw"
    PROCESSED_DIR = "./data/processed"
    ROI_DIR = "./data/processed/roi_crops"
    
    # Data Parameters
    TARGET_SPACING = (0.5, 0.5, 0.5)
    CROP_SIZE = (96, 96, 96)
    NUM_CLASSES = 14  # 1 Global + 13 Local
    
    # Anatomical Labels
    LABELS = [
        "aneurysm_global",
        "l_ica", "r_ica", 
        "l_mca", "r_mca", 
        "l_aca", "r_aca",
        "acom", "pcom", 
        "basilar", "other_posterior",
        "l_supraclinoid", "r_supraclinoid", 
        "l_infraclinoid", "r_infraclinoid"
    ]

    # Training Hyperparameters
    BATCH_SIZE = 8
    LEARNING_RATE = 1e-4
    EPOCHS = 50
    DEVICE = "cuda"