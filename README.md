# RAYT

Ray Tracing codes. I follow Peter Shirley's [Ray Tracing](https://raytracing.github.io/) trilogy. The goal is to have the same output in three languages; C++, Python, and Rust.

![](assets/image.png)

## Build Rust Project

I'll add a screenshot when the Rust project is ready.

```shell
cargo build --release

# if you have strip command
strip target/release/one_weekend
strip target/release/next_week

# run the project
./target/release/one_weekend > rayt_rust_one_weekend.ppm
./target/release/next_week > rayt_rust_next_week.ppm
```

Performance status (image width is 600px):

```shell
./target/release/one_weekend > image.ppm

Scanlines remaining: 0
Done.
./target/release/one_weekend > image.ppm  13.05s user 0.31s system 98% cpu 13.624 total
```

## Build Python Project

I tested the project using the latest stable version of Python (3.11).

```shell
cd rayt-python
poetry install
poetry run maturin develop
poetry run one-weekend --image-width=1200 > image.ppm
```

Performance status (image width is 300px):

```shell
time poetry run one-weekend --image-width=300 > image.ppm

Scanlines remaining: 1
Done.
poetry run one-weekend --image-width=300 > image.ppm  55.39s user 0.12s system 98% cpu 56.236 total
```
