"""
Deploy Models Script.

Copy trained models from notebooks to api-service.
Only copies the final production models.
"""

import shutil
from pathlib import Path


def deploy_models():
    """Copy final models from notebooks to api-service."""

    # Get project root (parent of scripts/)
    project_root = Path(__file__).parent.parent

    # Paths
    source_dir = project_root / "notebooks" / "models"
    target_dir = project_root / "api-service" / "models"

    # Create target directory
    target_dir.mkdir(exist_ok=True)

    # Models to copy (only final production models)
    models_to_copy = [
        "final_model.joblib",
        "final_label_encoders.joblib",
        "final_target_encodings.joblib",
        "final_metadata.joblib"
    ]

    print("=" * 80)
    print("DEPLOYING ML MODELS TO API")
    print("=" * 80)
    print(f"\nSource: {source_dir.absolute()}")
    print(f"Target: {target_dir.absolute()}")
    print(f"\nModels to deploy: {len(models_to_copy)}")

    # Copy each model
    for model_file in models_to_copy:
        source_path = source_dir / model_file
        target_path = target_dir / model_file

        if not source_path.exists():
            print(f"\n✗ NOT FOUND: {model_file}")
            continue

        # Copy file
        shutil.copy2(source_path, target_path)

        # Get file size
        size_mb = target_path.stat().st_size / (1024 * 1024)

        print(f"\n✓ COPIED: {model_file}")
        print(f"  Size: {size_mb:.2f} MB")

    print("\n" + "=" * 80)
    print("DEPLOYMENT COMPLETE!")
    print("=" * 80)
    print("\nAPI models ready at: api-service/models/")


if __name__ == "__main__":
    deploy_models()

