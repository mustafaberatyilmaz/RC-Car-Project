import torch
import traceback

print(f"Torch version: {torch.__version__}")
try:
    # Try different loading strategies
    print("Attempting torch.load...")
    torch.load('yolov8n.pt')
    print("Success torch.load")
except Exception:
    import traceback
    with open('debug_error.log', 'w') as f:
        traceback.print_exc(file=f)

