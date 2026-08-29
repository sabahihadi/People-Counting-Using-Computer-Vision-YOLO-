"""
reid.py

Person Re-Identification module.

This module extracts appearance embeddings from person crops
using an OSNet-based Re-ID model.

The module does NOT perform tracking by itself.
It only converts a person image into a feature vector that
can later be compared with previously seen persons.
"""

import cv2
import numpy as np
import torch
import torchreid
from torchvision import transforms


class PersonReID:
    """
    Extract appearance embeddings for person Re-ID.

    OSNet is used as the feature extractor.
    """

    def __init__(self):

        # Select GPU if CUDA is available.
        # Otherwise, use CPU.
        self.device = (
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        print(
            f"Re-ID device: {self.device}"
        )

        # Create the OSNet model.
        #
        # x1_0 is a relatively lightweight OSNet
        # architecture suitable for person Re-ID.
        self.model = torchreid.models.build_model(
            name="osnet_x1_0",
            num_classes=1000,
            pretrained=True
        )

        # Move model to selected device.
        self.model.to(self.device)

        # Evaluation mode.
        # We are extracting features, not training the model.
        self.model.eval()

        # Image transformation used by the Re-ID model.
        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((256, 128)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def extract_embedding(self, frame, bbox):
        """
        Extract an appearance embedding from a person bounding box.

        Parameters
        ----------
        frame : numpy.ndarray
            Original video frame.

        bbox : tuple
            Bounding box in the format:
            (x1, y1, x2, y2)

        Returns
        -------
        numpy.ndarray or None
            L2-normalized appearance embedding.
            Returns None if the crop is invalid.
        """

        x1, y1, x2, y2 = bbox

        # Make sure coordinates are inside the image.
        height, width = frame.shape[:2]

        x1 = max(0, x1)
        y1 = max(0, y1)

        x2 = min(width, x2)
        y2 = min(height, y2)

        # Invalid bounding box.
        if x2 <= x1 or y2 <= y1:
            return None

        # Crop the person from the frame.
        person_crop = frame[
            y1:y2,
            x1:x2
        ]

        # Make sure the crop is not empty.
        if person_crop.size == 0:
            return None

        # Convert OpenCV BGR image to RGB.
        person_crop = cv2.cvtColor(
            person_crop,
            cv2.COLOR_BGR2RGB
        )

        # Apply OSNet preprocessing.
        image = self.transform(person_crop)

        # Add batch dimension.
        image = image.unsqueeze(0)

        # Move tensor to selected device.
        image = image.to(self.device)

        # Disable gradient calculation.
        with torch.no_grad():

            embedding = self.model(image)

        # Convert tensor to NumPy.
        embedding = embedding.cpu().numpy()[0]

        # L2 normalization.
        #
        # This makes cosine similarity easier and more stable.
        norm = np.linalg.norm(embedding)

        if norm == 0:
            return None

        embedding = embedding / norm

        return embedding