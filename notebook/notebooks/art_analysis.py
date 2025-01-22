Art Image Data Exploration and Analysis
This notebook provides a comprehensive approach to exploring and analyzing a personal art image dataset.

# Import required libraries
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2
print('Libraries imported successfully')
class ArtDataProcessor:
    def __init__(self, data_path):
        self.data_path = data_path
        self.image_paths = []
        self.image_metadata = []
    
    def load_images(self):
        """Load all images from the specified directory"""
        for root, dirs, files in os.walk(self.data_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    full_path = os.path.join(root, file)
                    self.image_paths.append(full_path)
                    
                    # Extract metadata
                    try:
                        img = cv2.imread(full_path)
                        metadata = {
                            'filename': file,
                            'height': img.shape[0] if img is not None else None,
                            'width': img.shape[1] if img is not None else None,
                            'channels': img.shape[2] if img is not None else None,
                            'file_size': os.path.getsize(full_path)
                        }
                    except Exception as e:
                        print(f"Error processing {file}: {str(e)}")
                        metadata = {
                            'filename': file,
                            'height': None,
                            'width': None,
                            'channels': None,
                            'file_size': os.path.getsize(full_path)
                        }
                    self.image_metadata.append(metadata)
        
        return pd.DataFrame(self.image_metadata)
    
    def analyze_metadata(self, metadata_df):
        """Generate basic statistics and visualizations"""
        # Basic statistics
        stats = {
            'total_images': len(metadata_df),
            'avg_width': metadata_df['width'].mean(),
            'avg_height': metadata_df['height'].mean(),
            'total_size_mb': metadata_df['file_size'].sum() / (1024 * 1024)
        }
        
        # Create visualizations
        plt.figure(figsize=(15, 5))
        
        # Image dimensions distribution
        plt.subplot(131)
        plt.scatter(metadata_df['width'], metadata_df['height'])
        plt.xlabel('Width')
        plt.ylabel('Height')
        plt.title('Image Dimensions Distribution')
        
        # File size distribution
        plt.subplot(132)
        plt.hist(metadata_df['file_size'] / (1024 * 1024), bins=30)
        plt.xlabel('File Size (MB)')
        plt.ylabel('Count')
        plt.title('File Size Distribution')
        
        plt.tight_layout()
        plt.show()
        
        return stats
# Main execution
def main():
    # Initialize processor
    processor = ArtDataProcessor('data/raw/')
    
    # Load and analyze images
    metadata_df = processor.load_images()
    
    # Analyze metadata
    stats = processor.analyze_metadata(metadata_df)
    
    # Print basic statistics
    print("\nAnalysis Results:")
    for key, value in stats.items():
        print(f"{key}: {value:.2f}")
    
    # Save metadata
    metadata_df.to_csv('data/processed/image_metadata.csv', index=False)

if __name__ == '__main__':
    main()
