#! /bin/sh
set -x
opts="--xsize 640 --ysize 320"
python --version
for chap in chap{2,4,6,9,11,13}; do
  for cmd in $(python -m rtow.${chap} --help | grep -A100 Commands: | grep -v Commands:); do
    python -m rtow.${chap} ${cmd} ${cmd}.ppm ${opts}
  done
done
