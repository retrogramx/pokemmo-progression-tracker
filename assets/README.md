# Assets Directory

This directory contains application assets like icons, images, and other resources.

## Icon Files

- `icon.ico` - Windows application icon (optional)
- `icon.png` - Application icon in PNG format (optional)

## Adding an Icon

To add a custom icon to your executable:

1. Create an `.ico` file for Windows (recommended size: 256x256 pixels)
2. Place it in this directory as `icon.ico`
3. The build scripts will automatically use it

## Icon Creation Tools

- [GIMP](https://www.gimp.org/) - Free image editor
- [Inkscape](https://inkscape.org/) - Free vector graphics editor
- [IcoFX](https://icofx.ro/) - Windows icon editor
- Online converters: [ConvertICO](https://convertico.com/)

## Notes

- Icons are optional - the app will work without them
- Windows prefers `.ico` format for best compatibility
- Icon size should be at least 32x32 pixels, with 256x256 recommended
