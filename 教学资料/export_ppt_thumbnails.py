import re
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def natural_key(path):
    nums = re.findall(r"\d+", path.stem)
    return int(nums[-1]) if nums else 0


def export_with_win32(pptx, outdir):
    import win32com.client

    app = win32com.client.Dispatch("PowerPoint.Application")
    app.Visible = True
    pres = app.Presentations.Open(str(pptx), True, False, False)
    try:
        pres.Export(str(outdir), "JPG", 1600, 900)
    finally:
        pres.Close()
        app.Quit()


def export_with_powershell(pptx, outdir):
    ps = f"""
$pptx = "{str(pptx).replace('"', '`"')}"
$outdir = "{str(outdir).replace('"', '`"')}"
$app = New-Object -ComObject PowerPoint.Application
$app.Visible = $true
$pres = $app.Presentations.Open($pptx, $true, $false, $false)
$pres.Export($outdir, "JPG", 1600, 900)
$pres.Close()
$app.Quit()
"""
    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps], check=True)


def export_slides(pptx, outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    for p in outdir.glob("*.jpg"):
        p.unlink()
    for p in outdir.glob("*.JPG"):
        p.unlink()
    try:
        export_with_win32(pptx, outdir)
    except Exception:
        export_with_powershell(pptx, outdir)
    candidates = sorted(
        list(outdir.glob("Slide*.JPG"))
        + list(outdir.glob("Slide*.jpg"))
        + list(outdir.glob("幻灯片*.JPG"))
        + list(outdir.glob("幻灯片*.jpg")),
        key=natural_key,
    )
    slides = []
    seen = set()
    for p in candidates:
        key = str(p).lower()
        if key in seen or not p.exists():
            continue
        seen.add(key)
        slides.append(p)
    for i, p in enumerate(slides, 1):
        target = outdir / f"幻灯片{i}.jpg"
        if p.name == target.name:
            continue
        if p.name.lower() == target.name.lower():
            tmp = outdir / f"__tmp_slide_{i}.jpg"
            if tmp.exists():
                tmp.unlink()
            p.rename(tmp)
            tmp.rename(target)
            continue
        if target.exists():
            target.unlink()
        p.rename(target)


def make_grid(outdir, cols=5):
    imgs = sorted(outdir.glob("幻灯片*.jpg"), key=natural_key)
    if not imgs:
        raise RuntimeError(f"No slide thumbnails in {outdir}")
    thumbs = []
    for idx, p in enumerate(imgs, 1):
        im = Image.open(p).convert("RGB")
        im.thumbnail((320, 180))
        canvas = Image.new("RGB", (336, 214), "white")
        canvas.paste(im, ((336 - im.width) // 2, 8))
        d = ImageDraw.Draw(canvas)
        try:
            font = ImageFont.truetype("arial.ttf", 18)
        except Exception:
            font = ImageFont.load_default()
        d.text((12, 188), f"Slide {idx}", fill=(32, 42, 54), font=font)
        thumbs.append(canvas)
    rows = (len(thumbs) + cols - 1) // cols
    grid = Image.new("RGB", (cols * 336, rows * 214), (242, 244, 246))
    for i, im in enumerate(thumbs):
        x = (i % cols) * 336
        y = (i // cols) * 214
        grid.paste(im, (x, y))
    grid.save(outdir / "thumbnail_grid.jpg", quality=92)


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python export_ppt_thumbnails.py <pptx> <outdir>")
    pptx = Path(sys.argv[1]).resolve()
    outdir = Path(sys.argv[2]).resolve()
    export_slides(pptx, outdir)
    make_grid(outdir)
    print(outdir)


if __name__ == "__main__":
    main()
