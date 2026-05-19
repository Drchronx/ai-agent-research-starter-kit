# Figure Container Template

Visual specifications for applying the academic-paper style container to extracted PDF figures.

## Container Dimensions

| Property | Value | Notes |
|----------|-------|-------|
| Aspect Ratio | 16:9 | Standard presentation format |
| Resolution | 1920 x 1080 px | Full HD |
| High-Res Option | 3840 x 2160 px | 4K for print quality |

## Layout Specifications

```
┌─────────────────────────────────────────────────────────────────┐
│                           TITLE AREA                            │
│                         (120px height)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                                                                 │
│                       FIGURE AREA                               │
│                    (centered, scaled)                           │
│                     max 85% width                               │
│                     max 70% height                              │
│                                                                 │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                         CAPTION AREA                            │
│                          (80px height)                          │
└─────────────────────────────────────────────────────────────────┘
```

## Dimensions (1920x1080)

| Area | Position | Size |
|------|----------|------|
| Title | y: 40px, centered | height: 80px |
| Figure Container | centered | max-width: 1632px (85%), max-height: 756px (70%) |
| Caption | y: 960px, centered | height: 60px |
| Margins | all sides | 60px |

## Color Specifications (academic-paper style)

| Element | Color | Hex |
|---------|-------|-----|
| Background | White | #FFFFFF |
| Title Text | Dark Blue-Gray | #1E3A5F |
| Caption Text | Medium Gray | #6B7280 |
| Figure Border | Light Gray | #E5E7EB |
| Figure Shadow | Gray (10% opacity) | rgba(0,0,0,0.1) |

## Typography

### Title
- Font: Sans-serif (system default: Arial, Helvetica)
- Size: 48px (1920w) / 96px (3840w)
- Weight: Bold (700)
- Color: #1E3A5F
- Alignment: Center
- Max lines: 2

### Caption
- Font: Sans-serif (system default: Arial, Helvetica)
- Size: 24px (1920w) / 48px (3840w)
- Weight: Normal (400)
- Style: Italic
- Color: #6B7280
- Alignment: Center
- Format: "Figure N: [Caption text]"

## Figure Area Styling

### Container
- Background: White (#FFFFFF)
- Border: 1px solid #E5E7EB
- Border Radius: 8px
- Box Shadow: 0 4px 6px rgba(0,0,0,0.1)
- Padding: 20px

### Figure Scaling
- Maintain aspect ratio
- Scale to fit container (contain mode)
- Center horizontally and vertically
- Minimum margin from container edge: 20px

## Implementation Notes

### Canvas Setup (Node.js)

```typescript
import { createCanvas, loadImage } from 'canvas';

const WIDTH = 1920;
const HEIGHT = 1080;

const canvas = createCanvas(WIDTH, HEIGHT);
const ctx = canvas.getContext('2d');

// Background
ctx.fillStyle = '#FFFFFF';
ctx.fillRect(0, 0, WIDTH, HEIGHT);
```

### Title Rendering

```typescript
ctx.fillStyle = '#1E3A5F';
ctx.font = 'bold 48px Arial, Helvetica, sans-serif';
ctx.textAlign = 'center';
ctx.textBaseline = 'middle';
ctx.fillText(title, WIDTH / 2, 80);
```

### Figure Placement

```typescript
// Load and scale figure
const figure = await loadImage(figurePath);
const maxWidth = WIDTH * 0.85;
const maxHeight = HEIGHT * 0.70;

const scale = Math.min(maxWidth / figure.width, maxHeight / figure.height);
const scaledWidth = figure.width * scale;
const scaledHeight = figure.height * scale;

// Center position
const x = (WIDTH - scaledWidth) / 2;
const y = (HEIGHT - scaledHeight) / 2;

// Draw shadow
ctx.shadowColor = 'rgba(0,0,0,0.1)';
ctx.shadowBlur = 12;
ctx.shadowOffsetY = 4;

// Draw border
ctx.strokeStyle = '#E5E7EB';
ctx.lineWidth = 1;
ctx.strokeRect(x - 20, y - 20, scaledWidth + 40, scaledHeight + 40);

// Draw figure
ctx.drawImage(figure, x, y, scaledWidth, scaledHeight);
```

### Caption Rendering

```typescript
ctx.fillStyle = '#6B7280';
ctx.font = 'italic 24px Arial, Helvetica, sans-serif';
ctx.textAlign = 'center';
ctx.textBaseline = 'middle';
ctx.fillText(`Figure ${figureNum}: ${caption}`, WIDTH / 2, HEIGHT - 60);
```

## Variants

### Minimal Container
- No border or shadow
- Figure fills more space (90% width)
- Smaller title/caption (36px/18px)

### With Sub-caption
- Add second line below caption
- For additional notes or source attribution
- Smaller font (18px), lighter gray (#9CA3AF)

### Table Container
- Same layout as figure
- Replace "Figure N" with "Table N"
- Consider larger padding for table borders

## Output Format

- Format: PNG
- Color Space: sRGB
- Compression: Lossless
- Filename: Same as slide filename from outline
