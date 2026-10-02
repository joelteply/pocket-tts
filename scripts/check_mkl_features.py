"""Check the resolved dependency graph without compiling or downloading MKL binaries."""
import os
import subprocess


for target in (
    "x86_64-pc-windows-msvc",
    "x86_64-unknown-linux-gnu",
    "aarch64-apple-darwin",
):
    for enabled in (False, True):
        command = [
            "cargo", "tree", "--locked", "-p", "pocket-tts",
            "--target", target, "--no-default-features", "-e", "normal",
            "--prefix", "none",
        ]
        if enabled:
            command += ["--features", "mkl"]
        result = subprocess.run(
            command, check=True, capture_output=True, text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        present = any(line.startswith("intel-mkl-src v") for line in result.stdout.splitlines())
        if present != enabled:
            raise SystemExit(f"{target}: MKL presence {present}, requested {enabled}")
        print(f"PASS {target}: mkl={enabled}")
