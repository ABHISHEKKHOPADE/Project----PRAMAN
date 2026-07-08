class Config:

    # Resize Factor
    RESIZE_SCALE = 3

    # CLAHE
    CLAHE_CLIP_LIMIT = 2.0
    CLAHE_GRID_SIZE = (8, 8)

    # Adaptive Threshold
    BLOCK_SIZE = 11
    C = 2

    # Gaussian Blur
    GAUSSIAN_KERNEL = (3, 3)

    # Save Debug Images
    SAVE_DEBUG_IMAGES = True