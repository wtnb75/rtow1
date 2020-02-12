#! /bin/sh
# Usage: $0 output-dir input-files...
outdir=$1
shift

[ -d "${outdir}" ] || exit 1

for i; do
  ofn=$(basename $i .ppm)
  pnmtopng $i > ${outdir}/${ofn}.png
  optipng ${outdir}/${ofn}.png
done
