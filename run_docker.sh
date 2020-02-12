#! /bin/sh

for img in pypy:3-slim python:3-slim ; do
  outdir=${img%:*}-result
  if [ ${img%:*} = "pypy" ] ; then
    did=$(docker run -d -v $PWD:/w -w /w -ti ${img} sh run.sh pypy3)
  else
    did=$(docker run -d -v $PWD:/w -w /w -ti ${img} sh run.sh python3)
  fi
  docker wait ${did}
  mkdir -p ${outdir}
  docker logs ${did} > ${outdir}/result.txt
  docker rm ${did}
  mv *.ppm ${outdir}/
done
