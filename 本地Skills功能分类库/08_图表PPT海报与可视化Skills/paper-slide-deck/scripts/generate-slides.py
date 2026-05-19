"""
generate-slides.py - Generate slide images using Gemini API

Usage:
    python generate-slides.py <slide-deck-dir> [--model MODEL]

Arguments:
    slide-deck-dir    Directory containing prompts/ folder with slide prompts

Options:
    --model MODEL     Gemini model to use (default: gemini-3-pro-image-preview)

Environment:
    GOOGLE_API_KEY or GEMINI_API_KEY must be set

Example:
    python generate-slides.py ./slide-deck/my-presentation --model gemini-3-pro-image-preview
"""

import os
import sys
import time
import argparse
from pathlib import Path

def check_dependencies():
    """Check and install required dependencies."""
    try:
        from google import genai
        from google.genai import types
        return genai, types
    except ImportError:
        print("Installing google-genai package...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "google-genai", "-q"])
        from google import genai
        from google.genai import types
        return genai, types

def generate_slide(client, types, model: str, prompt: str, output_path: Path, max_retries: int = 3) -> bool:
    """Generate a single slide image with retry logic."""

    for attempt in range(max_retries):
        try:
            if attempt > 0:
                wait_time = 5 * (attempt + 1)
                print(f"  Retry {attempt}/{max_retries-1} (waiting {wait_time}s)...")
                time.sleep(wait_time)
            else:
                print(f"  Generating image...")

            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    image_config=types.ImageConfig(
                        aspect_ratio="16:9",
                        image_size="4K"
                    )
                )
            )

            # Extract image from response
            if response.candidates:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                        image_data = part.inline_data.data
                        # Save image (data is already bytes)
                        output_path.parent.mkdir(parents=True, exist_ok=True)
                        with open(output_path, "wb") as f:
                            f.write(image_data)
                        size_kb = len(image_data) / 1024
                        print(f"  Saved: {output_path.name} ({size_kb:.1f} KB)")
                        return True

            print(f"  Warning: No image in response")

        except Exception as e:
            print(f"  Error: {e}")
            if attempt == max_retries - 1:
                return False

    return False

def find_slides_to_generate(prompts_dir: Path, slides_dir: Path) -> list:
    """Find slides that need generation (have prompts but no output or small output)."""
    slides = []

    for prompt_file in sorted(prompts_dir.glob("*.txt")):
        slide_name = prompt_file.stem
        output_file = slides_dir / f"{slide_name}.png"

        # Skip if output exists and is valid (> 10KB)
        if output_file.exists() and output_file.stat().st_size > 10000:
            continue

        slides.append({
            "name": slide_name,
            "prompt_file": prompt_file,
            "output_file": output_file,
        })

    return slides

def main():
    parser = argparse.ArgumentParser(description="Generate slide images using Gemini API")
    parser.add_argument("slide_deck_dir", help="Directory containing prompts/ folder")
    parser.add_argument("--model", default="gemini-3-pro-image-preview",
                        help="Gemini model to use (default: gemini-3-pro-image-preview)")
    args = parser.parse_args()

    # Check dependencies
    genai, types = check_dependencies()

    # Initialize paths
    deck_dir = Path(args.slide_deck_dir)
    prompts_dir = deck_dir / "prompts"
    slides_dir = deck_dir / "slides"

    if not prompts_dir.exists():
        print(f"Error: Prompts directory not found: {prompts_dir}")
        sys.exit(1)

    # Get API key
    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY or GEMINI_API_KEY environment variable not set")
        sys.exit(1)

    # Initialize client
    client = genai.Client(api_key=api_key)

    # Create output directory
    slides_dir.mkdir(parents=True, exist_ok=True)

    # Find slides to generate
    slides = find_slides_to_generate(prompts_dir, slides_dir)

    if not slides:
        print("All slides already generated. Nothing to do.")
        # List existing slides
        existing = sorted(slides_dir.glob("*.png"))
        print(f"\nExisting slides ({len(existing)}):")
        for slide in existing:
            size_kb = slide.stat().st_size / 1024
            print(f"  - {slide.name} ({size_kb:.1f} KB)")
        return

    print(f"Generating {len(slides)} slides using {args.model}...")
    print(f"Output directory: {slides_dir}\n")

    success_count = 0
    failed_slides = []

    for i, slide in enumerate(slides):
        print(f"[{i + 1}/{len(slides)}] {slide['name']}")

        # Read prompt
        prompt = slide["prompt_file"].read_text(encoding="utf-8")

        # Generate slide
        if generate_slide(client, types, args.model, prompt, slide["output_file"]):
            success_count += 1
        else:
            failed_slides.append(slide["name"])

    print(f"\nDone! Generated {success_count}/{len(slides)} slides.")

    if failed_slides:
        print(f"\nFailed slides ({len(failed_slides)}):")
        for name in failed_slides:
            print(f"  - {name}")

    # List all slides in output directory
    all_slides = sorted(slides_dir.glob("*.png"))
    print(f"\nTotal slides in output: {len(all_slides)}")
    for slide in all_slides:
        size_kb = slide.stat().st_size / 1024
        print(f"  - {slide.name} ({size_kb:.1f} KB)")

if __name__ == "__main__":
    main()
