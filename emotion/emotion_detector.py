import torch
import torch.backends.cudnn as cudnn
import torchvision.transforms as transforms
from pathlib import Path

from PIL import Image
from emotion.repvgg import create_RepVGG_A0 as create

# Load model
model = create(deploy=True)

# 8 Emotions
emotions = ("anger","contempt","disgust","fear","happy","neutral","sad","surprise")

def init(device):
    # Initialise model
    global dev
    dev = device
    model.to(device)
    # load weights from package-relative path
    weights_path = Path(__file__).resolve().parent / "weights" / "repvgg.pth"
    try:
        if not weights_path.exists():
            raise FileNotFoundError(f"RepVGG weights not found at {weights_path}")
        state = torch.load(str(weights_path), map_location=device, weights_only=False)
        model.load_state_dict(state)
    except Exception as e:
        # log error and continue with uninitialized weights (random)
        print(f"Warning: could not load emotion model weights: {e}")

    # Save to eval
    cudnn.benchmark = True
    model.eval()

def detect_emotion(images,conf=True):
    with torch.no_grad():
        # Normalise and transform images
        normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                        std=[0.229, 0.224, 0.225])
        x = torch.stack([transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                normalize,
            ])(Image.fromarray(image)) for image in images])
        # Feed through the model
        y = model(x.to(dev))
        result = []
        for i in range(y.size()[0]):
            # Add emotion to result
            emotion = (max(y[i]) == y[i]).nonzero().item()
            # Add appropriate label if required
            result.append([f"{emotions[emotion]}{f' ({100*y[i][emotion].item():.1f}%)' if conf else ''}",emotion])
    return result