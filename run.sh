#! /bin/sh
python=${1-pypy36}
pydir=$(basename $python)

rm -f *.ppm
rm -rf ${pydir}
${python} -m venv ${pydir}
. ./${pydir}/bin/activate
pip install -r requirements.txt
bash test_all.sh
