import subprocess
import os
import pycolmap

def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {' '.join(command)}")
        print(f"Error output: {result.stderr}")
        return False
    return True

def run_colmap(database_path, images_path, output_path):
    # Feature extraction
    if not run_command([
        'colmap', 'feature_extractor',
        '--database_path', database_path,
        '--image_path', images_path
    ]):
        return False
    
    # Feature matching
    if not run_command([
        'colmap', 'exhaustive_matcher',
        '--database_path', database_path
    ]):
        return False
    
    # Sparse reconstruction
    sparse_path = os.path.join(output_path, 'sparse')
    os.makedirs(sparse_path, exist_ok=True)
    if not run_command([
        'colmap', 'mapper',
        '--database_path', database_path,
        '--image_path', images_path,
        '--output_path', sparse_path
    ]):
        return False
    
    # Dense reconstruction
    dense_path = os.path.join(output_path, 'dense')
    os.makedirs(dense_path, exist_ok=True)
    
    if not run_command([
        'colmap', 'patch_match_stereo',
        '--workspace_path', output_path,
        '--workspace_format', 'COLMAP',
        '--PatchMatchStereo.max_image_size', '2000',
        '--PatchMatchStereo.geom_consistency', '1'
    ]):
        return False
    
    if not run_command([
        'colmap', 'poisson_mesher',
        '--input_path', dense_path,
        '--output_path', dense_path
    ]):
        return False
    
    return True

def analyze_results(database_path):
    db = pycolmap.Database(database_path)
    
    # Query cameras
    cameras = db.read_all_cameras()
    for camera in cameras:
        print(f"Camera ID: {camera.id}, Model: {camera.model}, Width: {camera.width}, Height: {camera.height}")

    # Query images
    images = db.read_all_images()
    for image in images:
        print(f"Image ID: {image.id}, Name: {image.name}, Qvec: {image.qvec}, Tvec: {image.tvec}")

# Paths
database_path = './database/database.db'
images_path = './frames'
output_path = './3D_model'

# Run COLMAP
if run_colmap(database_path, images_path, output_path):
    print("COLMAP processing completed successfully.")
    
    # Analyze results
    analyze_results(database_path)
else:
    print("COLMAP processing failed.")
