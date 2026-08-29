"""
test_reid.py

Evaluate Person Re-ID using multiple image pairs.

The test compares:
1. Same-person pairs
2. Different-person pairs

The goal is to understand the similarity distribution
before selecting a Re-ID matching threshold.
"""

import cv2
import numpy as np

from src.reid import PersonReID


# --------------------------------------------------
# Test pairs
# --------------------------------------------------

# Format:
#
# ("image_1", "image_2", "label")
#
# label:
#   SAME      -> images belong to the same person
#   DIFFERENT -> images belong to different people

TEST_PAIRS = [

    # Same person
    (
        "test_data/A1.jpg",
        "test_data/A2.jpg",
        "SAME"
    ),

    (
        "test_data/A1.jpg",
        "test_data/A3.jpg",
        "SAME"
    ),

    (
        "test_data/B1.jpg",
        "test_data/B2.jpg",
        "SAME"
    ),

    # Different people
    (
        "test_data/A1.jpg",
        "test_data/B1.jpg",
        "DIFFERENT"
    ),

    (
        "test_data/A2.jpg",
        "test_data/B2.jpg",
        "DIFFERENT"
    ),

    (
        "test_data/A3.jpg",
        "test_data/B1.jpg",
        "DIFFERENT"
    ),
]


# --------------------------------------------------
# Cosine Similarity
# --------------------------------------------------

def cosine_similarity(embedding_a, embedding_b):
    """
    Calculate cosine similarity between two embeddings.

    The embeddings produced by PersonReID are already
    L2-normalized, therefore their dot product is
    equivalent to cosine similarity.
    """

    return float(
        np.dot(
            embedding_a,
            embedding_b
        )
    )


# --------------------------------------------------
# Extract embedding
# --------------------------------------------------

def get_embedding(reid, image_path):
    """
    Read an image and extract its Re-ID embedding.
    """

    image = cv2.imread(image_path)

    if image is None:

        print(
            f"ERROR: Cannot read image: {image_path}"
        )

        return None

    # The input image is already a person crop.
    bbox = (
        0,
        0,
        image.shape[1],
        image.shape[0]
    )

    return reid.extract_embedding(
        image,
        bbox
    )


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    # Load Re-ID model once.
    reid = PersonReID()

    print()
    print("--------------------------------")
    print("Re-ID Multi-Pair Evaluation")
    print("--------------------------------")

    same_scores = []
    different_scores = []

    # --------------------------------------------------
    # Process test pairs
    # --------------------------------------------------

    for image_1, image_2, label in TEST_PAIRS:

        embedding_1 = get_embedding(
            reid,
            image_1
        )

        embedding_2 = get_embedding(
            reid,
            image_2
        )

        # Skip invalid pairs.
        if embedding_1 is None or embedding_2 is None:
            continue

        similarity = cosine_similarity(
            embedding_1,
            embedding_2
        )

        print(
            f"{label:10s} | "
            f"{image_1:25s} | "
            f"{image_2:25s} | "
            f"Similarity = {similarity:.4f}"
        )

        # Store results according to class.
        if label == "SAME":

            same_scores.append(
                similarity
            )

        elif label == "DIFFERENT":

            different_scores.append(
                similarity
            )

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    print()
    print("--------------------------------")
    print("Summary")
    print("--------------------------------")

    if same_scores:

        print(
            f"Same-person pairs     : "
            f"{len(same_scores)}"
        )

        print(
            f"Same-person mean      : "
            f"{np.mean(same_scores):.4f}"
        )

        print(
            f"Same-person minimum   : "
            f"{np.min(same_scores):.4f}"
        )

        print(
            f"Same-person maximum   : "
            f"{np.max(same_scores):.4f}"
        )

    if different_scores:

        print(
            f"Different-person pairs: "
            f"{len(different_scores)}"
        )

        print(
            f"Different-person mean : "
            f"{np.mean(different_scores):.4f}"
        )

        print(
            f"Different-person min  : "
            f"{np.min(different_scores):.4f}"
        )

        print(
            f"Different-person max  : "
            f"{np.max(different_scores):.4f}"
        )

    # --------------------------------------------------
    # Initial threshold estimation
    # --------------------------------------------------

    if same_scores and different_scores:

        lowest_same = np.min(same_scores)

        highest_different = np.max(
            different_scores
        )

        print()
        print("--------------------------------")
        print("Threshold Analysis")
        print("--------------------------------")

        print(
            f"Lowest SAME similarity     : "
            f"{lowest_same:.4f}"
        )

        print(
            f"Highest DIFFERENT similarity: "
            f"{highest_different:.4f}"
        )

        # If there is a gap between the two groups,
        # use the midpoint as an initial threshold.
        if lowest_same > highest_different:

            threshold = (
                lowest_same +
                highest_different
            ) / 2

            print(
                f"Initial threshold          : "
                f"{threshold:.4f}"
            )

            print(
                "A clear separation exists "
                "in this small test set."
            )

        else:

            print(
                "WARNING: The similarity ranges "
                "overlap."
            )

            print(
                "A reliable threshold cannot be "
                "determined from this small test."
            )

    print("--------------------------------")


if __name__ == "__main__":
    main()