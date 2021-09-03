# Palettes

## Fundamentals

## Loading Palettes

### From Files

```python
load_palette(name: str) -> ColorPalette
```

Palettes can have named colors:

```txt
pink=#e84393
purple=#673ab7
cyan=#03a9f4
green=#64dd17
```

Or palettes can just be a list of colors (in which case they'll be named as 0, 1, 2, etc.)

```txt
#16171a
#7f0622
#d62411
#ff8426
```

### Lospec

Palettes can also be loaded from the [Lospec palette list](https://lospec.com/palette-list)

```python
load_or_download_palette(name: str, save: bool = True) -> ColorPalette:
```

By default, this function will save any palettes downloaded from Lospec into the palettes/ subdirectory.
