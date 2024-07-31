#######TODO: LINK THIS REPO TO GITHUB AND NAME IT PYSANDBOX####

import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import cv2

# Load the U^2-Net model
model = torch.hub.load('NathanUA/U-2-Net', 'u2net')
model.eval()

# Preprocess the image
def preprocess_image(image_path):
    transform = transforms.Compose([
        transforms.Resize((320, 320)),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    ])
    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0)
    return image

# Post-process the output mask
def postprocess_mask(output):
    output = output.squeeze().cpu().detach().numpy()
    mask = (output > 0.5).astype(np.uint8) * 255
    return mask

# Background removal function
def remove_background(image_path, output_path):
    image = preprocess_image(image_path)
    with torch.no_grad():
        d1, d2, d3, d4, d5, d6, d7 = model(image)
        output = d1[:, 0, :, :]
    mask = postprocess_mask(output)
    
    # Load the original image
    original_image = cv2.imread(image_path)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    original_image = cv2.resize(original_image, (320, 320))

    # Apply the mask to the original image
    foreground = cv2.bitwise_and(original_image, original_image, mask=mask)

    # Save the result
    cv2.imwrite(output_path, cv2.cvtColor(foreground, cv2.COLOR_RGB2BGR))

# Example usage
image_path = 'path_to_your_image.jpg'
output_path = 'output_image.png'
remove_background(image_path, output_path)
