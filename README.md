# RAYT

Ray Tracing codes. I follow Peter Shirley's [Ray Tracing](https://raytracing.github.io/) trilogy. The goal is to have the same output with Python, solving the performance problems.

![](assets/image.png)

## How to Build

I tested the project using the latest stable version of Python (3.13).

```shell
uvx maturin develop
uv run one-weekend --image-width=1200 > image.ppm
```

Performance status (image width is 300px):

```shell
time uv run one-weekend --image-width=1200 > image.ppm
```

```
Scanlines remaining: 1
Done.
uv run one-weekend --image-width=1200 > image.ppm  47.36s user 0.03s system 99% cpu 47.504 total
```
