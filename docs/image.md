# Image

Convenience functions for working with images, or folders of images.

## Directory Helpers

```python
images_from_path(filepath: str, input_root: str = "input") -> list[str]
```

```python
load_images_from_path(filepath: str, input_root: str = "input") -> list[Image]
```

```python
load_from_path(filepath: str, input_root: str = "input") -> list[tuple[str, Image]]
```

## Wrapping

```python
swap_quadrants(im: Image) -> Image
```

```python
wrapped_alpha_composite(im: Image, paste: Image, coord: tuple[int, int]) -> Image
```
