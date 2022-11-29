Title: Rust Cargo release build is not the fastest
Date: 2022-11-29
Category: en,
Tags: rust, lto, cargo

As a Rust developer, it's well known that `cargo build` will build a debug binary at ./target/debug/filename, which is helpful for development/debug but without many binary optimizations, thus, runs slow.

When build with `cargo build --release`, it will build an optimized binary, which is ready for production:

```
--release                    Build artifacts in release mode, with optimizations
```

But it still not the fastest it can be.

## Cargo profiles
Cargo has 4 builtin profiles: `dev, release, test, and bench` <https://doc.rust-lang.org/cargo/reference/profiles.html> which pre-defined build options.
User can customize them in Cargo.toml, e.g:

```
[profile.dev]
opt-level = 1
debug = true
```

## LTO - Link time optimizations

<https://doc.rust-lang.org/cargo/reference/profiles.html#lto>

Default profile.release sets lto = false.

```
[profile.release]
opt-level = 3
debug = false
split-debuginfo = '...'  # Platform-specific.
debug-assertions = false
overflow-checks = false
lto = false
panic = 'unwind'
incremental = false
codegen-units = 16
rpath = false
```

Set lto = true or lto = "fat" will

> Performs "fat" LTO which attempts to perform optimizations across all crates within the dependency graph.

which makes build much slower, but the binary often faster 10-20% compare to lto = false.
User may try lto = "thin" for faster build but the output still good comparable to lto = "fat"

> "thin": Performs "thin" LTO. This is similar to "fat", but takes substantially less time to run while still achieving performance gains similar to "fat".

## Reference
- <https://doc.rust-lang.org/cargo/reference/profiles.html#lto>

Happy building!
