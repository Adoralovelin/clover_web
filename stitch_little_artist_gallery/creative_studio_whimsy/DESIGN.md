---
name: Creative Studio Whimsy
colors:
  surface: '#fdf7ff'
  surface-dim: '#dfd5f9'
  surface-bright: '#fdf7ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f8f1ff'
  surface-container: '#f2ebff'
  surface-container-high: '#ede4ff'
  surface-container-highest: '#e7deff'
  on-surface: '#1d1832'
  on-surface-variant: '#514347'
  inverse-surface: '#322c48'
  inverse-on-surface: '#f5eeff'
  outline: '#837377'
  outline-variant: '#d5c2c6'
  surface-tint: '#864d61'
  primary: '#864d61'
  on-primary: '#ffffff'
  primary-container: '#ffb7ce'
  on-primary-container: '#7b4458'
  inverse-primary: '#fab3ca'
  secondary: '#685f25'
  on-secondary: '#ffffff'
  secondary-container: '#eee199'
  on-secondary-container: '#6d6329'
  tertiary: '#2f6a3f'
  on-tertiary: '#ffffff'
  tertiary-container: '#9bdaa5'
  on-tertiary-container: '#266137'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffd9e3'
  primary-fixed-dim: '#fab3ca'
  on-primary-fixed: '#360b1e'
  on-primary-fixed-variant: '#6a364a'
  secondary-fixed: '#f1e39c'
  secondary-fixed-dim: '#d4c782'
  on-secondary-fixed: '#201c00'
  on-secondary-fixed-variant: '#50470f'
  tertiary-fixed: '#b2f2bb'
  tertiary-fixed-dim: '#96d5a0'
  on-tertiary-fixed: '#00210b'
  on-tertiary-fixed-variant: '#145129'
  background: '#fdf7ff'
  on-background: '#1d1832'
  surface-variant: '#e7deff'
typography:
  headline-lg:
    fontFamily: Quicksand
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Quicksand
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Quicksand
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.3'
  headline-sm:
    fontFamily: Quicksand
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Be Vietnam Pro
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Be Vietnam Pro
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-md:
    fontFamily: Quicksand
    fontSize: 14px
    fontWeight: '700'
    lineHeight: '1.0'
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base-unit: 8px
  gutter: 24px
  margin-mobile: 20px
  margin-desktop: 64px
  card-gap: 32px
---

## Brand & Style

This design system is built to celebrate the imaginative spirit of a young artist. The brand personality is joyful, curious, and tactile, echoing the feeling of a physical scrapbooking table or a dedicated arts-and-crafts nook. It avoids the clinical precision of traditional portfolios in favor of a "Handmade Digital" aesthetic.

The visual style blends **Soft Neomorphism** with **Playful Illustration**. It uses high-quality "sticker" motifs, paper-like textures, and organic, hand-drawn strokes to frame digital content. The goal is to make the user feel like they are flipping through a cherished sketchbook where every project is a "masterpiece" held up by colorful tape.

## Colors

The palette is a curated selection of "Sugar Pastels" designed to feel vibrant yet soft on the eyes. 

- **Primary (Cupcake Pink):** Used for main actions, active states, and decorative "washi tape" accents.
- **Secondary (Sunshine Yellow):** Reserved for highlights, badges, and "star" icons to denote special achievements.
- **Tertiary (Mint Sorbet):** Used for success states, growth indicators, and nature-themed craft categories.
- **Neutral (Lavender Mist):** Provides a soft alternative to grey for backgrounds and borders, keeping the interface warm and inviting.

Surface colors should prioritize a "Paper White" (#FCFCFD) background to allow the pastels to pop without looking muddy.

## Typography

The typography system balances whimsy with legibility. 

**Quicksand** is the hero font, used for all headings and labels. Its rounded terminals mirror the "bubbly" nature of the design system. All headings should be set in Semi-Bold or Bold to ensure they stand out against colorful backgrounds.

**Be Vietnam Pro** serves as the body typeface. It is clean and modern with a friendly geometric construction that maintains high readability for descriptions of art projects or "About Me" stories. 

For a "hand-written" feel, certain pull-quotes or decorative captions can be slightly rotated (1-2 degrees) to mimic manual lettering.

## Layout & Spacing

The layout follows a **Fluid "Scrapbook" Grid**. While it adheres to a standard 12-column system for alignment, elements are encouraged to break the grid slightly using offsets and rotations.

- **Desktop:** A centered container with wide 64px margins creates a "canvas" feel.
- **Mobile:** Margins shrink to 20px, and content stacks into a single, vertical "feed" of art cards.
- **Rhythm:** Use a loose spacing scale based on 8px increments. Padding inside cards should be generous (min 32px) to maintain a soft, breathable atmosphere.

## Elevation & Depth

This design system rejects harsh, black shadows. Instead, it uses **Colored Ambient Shadows** and **Layered Surfaces** to create depth.

- **Shadows:** Use large blur radii (20px+) with low-opacity versions of the Lavender or Pink brand colors. This makes elements appear to "float" like paper cutouts.
- **Inner Shadows:** Used sparingly on input fields and "pressed" buttons to create a tactile, squishy feel.
- **The "Sticker" Effect:** Interactive elements feature a 2px solid white border *outside* the shadow, mimicking the die-cut edge of a physical sticker.

## Shapes

The shape language is dominated by **Extreme Softness**. Sharp corners are non-existent.

- **Primary Containers:** Use the `rounded-lg` (1rem) or `rounded-xl` (1.5rem) setting to ensure every corner feels safe and friendly.
- **Buttons and Chips:** Always use the "Pill" shape (fully rounded sides) to maximize the tactile, "toy-like" quality of the UI.
- **Squiggles:** Incorporate non-geometric, hand-drawn SVG shapes as background decorations or dividers between sections.

## Components

### Buttons
Buttons are pill-shaped and use a "Dual-Tone" shadow. The resting state has a soft colored shadow; on hover, the button moves 2px down and the shadow tightens to create a "pressed" effect.

### Art Cards
Cards are the heart of the system. Each card has a thick white border (4px) and a subtle 2-degree tilt (alternating left/right in a grid). They should feature a "Paper Texture" overlay at 5% opacity.

### Stickers & Badges
Use secondary and tertiary colors for status badges (e.g., "New Drawing", "School Project"). These should look like physical stickers with a slight white "die-cut" outline.

### Input Fields
Forms should be large and easy to tap. Use a soft Lavender background instead of a white one to make the input feel "filled-in."

### Progress Brushes
Instead of standard progress bars, use "Paint Stroke" graphics that fill with color from left to right to show completion or skill levels.