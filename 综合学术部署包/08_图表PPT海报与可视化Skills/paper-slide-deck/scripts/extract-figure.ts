/**
 * extract-figure.ts
 * Extract a specific page from a PDF and save as PNG image.
 *
 * Usage:
 *   npx -y bun extract-figure.ts --pdf paper.pdf --page 4 --output figure.png
 *
 * Options:
 *   --pdf     Path to source PDF file (required)
 *   --page    Page number to extract, 1-indexed (required)
 *   --output  Output PNG file path (required)
 *   --scale   Render scale factor, default 2.0 for high quality (optional)
 */

import { existsSync, writeFileSync, mkdirSync } from "fs";
import { dirname, resolve } from "path";
// Use legacy build for Node.js compatibility
import * as pdfjsLib from "pdfjs-dist/legacy/build/pdf.mjs";
import { createCanvas } from "canvas";

interface Args {
  pdf: string;
  page: number;
  output: string;
  scale: number;
}

function parseArgs(): Args {
  const args = process.argv.slice(2);
  let pdf = "";
  let page = 0;
  let output = "";
  let scale = 2.0;

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case "--pdf":
        pdf = args[++i];
        break;
      case "--page":
        page = parseInt(args[++i], 10);
        break;
      case "--output":
        output = args[++i];
        break;
      case "--scale":
        scale = parseFloat(args[++i]);
        break;
    }
  }

  if (!pdf || !page || !output) {
    console.error("Usage: bun extract-figure.ts --pdf <pdf-path> --page <number> --output <output.png>");
    console.error("\nOptions:");
    console.error("  --pdf     Path to source PDF file (required)");
    console.error("  --page    Page number to extract, 1-indexed (required)");
    console.error("  --output  Output PNG file path (required)");
    console.error("  --scale   Render scale factor, default 2.0 (optional)");
    process.exit(1);
  }

  return { pdf, page, output, scale };
}

async function extractPage(pdfPath: string, pageNum: number, outputPath: string, scale: number) {
  // Validate PDF exists
  const absolutePdfPath = resolve(pdfPath);
  if (!existsSync(absolutePdfPath)) {
    throw new Error(`PDF file not found: ${absolutePdfPath}`);
  }

  console.log(`Loading PDF: ${absolutePdfPath}`);

  // Load the PDF document
  const loadingTask = pdfjsLib.getDocument({
    url: absolutePdfPath,
    useSystemFonts: true,
    standardFontDataUrl: "node_modules/pdfjs-dist/standard_fonts/",
  });

  const pdfDoc = await loadingTask.promise;
  const totalPages = pdfDoc.numPages;

  console.log(`PDF loaded: ${totalPages} pages`);

  // Validate page number
  if (pageNum < 1 || pageNum > totalPages) {
    throw new Error(`Page ${pageNum} out of range (1-${totalPages})`);
  }

  // Get the page
  const page = await pdfDoc.getPage(pageNum);
  const viewport = page.getViewport({ scale });

  console.log(`Page ${pageNum}: ${Math.round(viewport.width)}x${Math.round(viewport.height)} px (scale: ${scale})`);

  // Create canvas
  const canvas = createCanvas(viewport.width, viewport.height);
  const ctx = canvas.getContext("2d");

  // Fill white background
  ctx.fillStyle = "#FFFFFF";
  ctx.fillRect(0, 0, viewport.width, viewport.height);

  // Render page to canvas
  const renderContext = {
    canvasContext: ctx as any,
    viewport: viewport,
  };

  console.log("Rendering page...");
  await page.render(renderContext).promise;

  // Ensure output directory exists
  const outputDir = dirname(outputPath);
  if (outputDir && !existsSync(outputDir)) {
    mkdirSync(outputDir, { recursive: true });
  }

  // Save as PNG
  const buffer = canvas.toBuffer("image/png");
  writeFileSync(outputPath, buffer);

  console.log(`\nSaved: ${outputPath}`);
  console.log(`Size: ${Math.round(buffer.length / 1024)} KB`);
}

async function main() {
  const { pdf, page, output, scale } = parseArgs();

  try {
    await extractPage(pdf, page, output, scale);
    console.log("\nExtraction complete!");
  } catch (error) {
    console.error("\nError:", error instanceof Error ? error.message : error);
    process.exit(1);
  }
}

main();
