import sharp from 'sharp';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function cropAvatar() {
  const inputPath = path.join(__dirname, 'public', 'img', 'avatar.jpg');
  const outputPath = path.join(__dirname, 'public', 'img', 'avatar-cropped.jpg');
  
  try {
    // Get image metadata first
    const metadata = await sharp(inputPath).metadata();
    console.log('Original image dimensions:', metadata.width, 'x', metadata.height);
    
    // ZOOM OUT WAAAAAYYYY MORE - use almost the entire original image
    // Show the full context with minimal cropping
    const cropWidth = Math.floor(metadata.width * 1.0); // Take 100% of width (MAXIMUM ZOOM OUT)
    const cropHeight = Math.floor(metadata.height * 1.0); // Take 100% of height (MAXIMUM ZOOM OUT)
    
    // Use the entire image with no cropping
    const left = 0; // Start from the very left
    const top = 0; // Start from the very top
    
    await sharp(inputPath)
      .extract({
        left: left,
        top: top,
        width: cropWidth,
        height: cropHeight
      })
      .resize(400, 400, {
        fit: 'cover',
        position: 'center'
      })
      .jpeg({ quality: 90 })
      .toFile(outputPath);
    
    console.log('Avatar cropped successfully!');
    console.log('Cropped from:', `${metadata.width}x${metadata.height}`);
    console.log('Crop area:', `${cropWidth}x${cropHeight} at position (${left}, ${top})`);
    console.log('Final size: 400x400');
    
    // Replace the original avatar with the cropped version
    await sharp(outputPath)
      .toFile(inputPath);
    
    console.log('Original avatar.jpg updated with cropped version');
    
  } catch (error) {
    console.error('Error cropping avatar:', error);
  }
}

cropAvatar();
