from PIL import Image
import torch
from clip import load,tokenize
import io
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = load("ViT-B/32", device=device)
from torchvision import transforms


preprocess = transforms.Compose([
    transforms.Resize((224, 224)),  
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def image_processing(image_file):
    try:
        # Convert image file to PIL Image
        if isinstance(image_file, bytes):
            image = Image.open(io.BytesIO(image_file)).convert("RGB")
        elif isinstance(image_file, str):  # If it's a file path
            image = Image.open(image_file).convert("RGB")
        elif isinstance(image_file, Image.Image):  # If already a PIL image
            image = image_file
        else:
            raise ValueError("Unsupported image format")

        # Preprocess & move to device inside torch.no_grad()
        with torch.no_grad():
            image = preprocess(image).unsqueeze(0).to(device)
            embedding = model.encode_image(image).cpu().numpy().flatten()

        return embedding.tolist()

    except Exception as e:
        print(f"Error processing image: {e}")
        return None  # Return None if there's an error

def get_text_embedding(text):
    try:
        text_tokenized = tokenize([text]).to(device)
        with torch.no_grad():
            embedding = model.encode_text(text_tokenized).cpu().numpy().flatten()
        return embedding  
    except Exception as e:
        print(f"Error processing text: {e}")
        return None  
