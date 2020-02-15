# [Python] Ray Tracing In One Weekend

https://raytracing.github.io/books/RayTracingInOneWeekend.html

- pure python code
- no optimization
- no parallelism
- no numpy
- no GPU

# Usage

## Prepare

pypy3 is recommended.

- using pyenv
    - pyenv install pypy3.6-7.3.0
    - pyenv shell pypy3.6-7.3.0
    - python -m venv pypy36
    - . pypy36/bin/activate
- Mac(Homebrew)
    - brew install pypy3
    - pypy3 -m venv pypy3
    - . pypy3/bin/activate
- Ubuntu
    - apt update; apt install pypy3
    - pypy3 -m venv pypy3
    - . pypy3/bin/activate
- Docker
    - docker pull pypy:3-slim
    - docker run -v $PWD/w -w /w pypy:3-slim sh
- pip install -r requirements.txt

## Run

- python -m rtow.chap2
- python -m rtow.chap4
- python -m rtow.chap6
- python -m rtow.chap9
- python -m rtow.chap11
- python -m rtow.chap13

# Performance

- nx=640, ny=320, ns=100
- experimental setup 1 (VPS)
    - server spec
        - CPU: Intel(R) Xeon(R) CPU E5-2650 v3 @ 2.30GHz
        - bogomips : 4589.36
    - pypy-3.6 7.3.0 (docker image: pypy:3.6-7.3.0-slim)
    - python 3.8.1 (docker image: python:3.8.1-slim)
- setup 2
    - Raspberry Pi 2B (RasPi2B)
        - CPU: ARMv7 Processor rev 5 (v7l)
        - BogoMIPS : 57.60
    - Raspbian jessie
    - pypy-3.5 6.0.0 (download from [pypy release](https://bitbucket.org/pypy/pypy/downloads/) pypy3-v6.0.0-linux-armhf-raspbian.tar.bz2)
- setup 3
    - Raspberry Pi 3B (RasPi3B)
        - CPU: ARMv7 Processor rev 4 (v7l)
        - BogoMIPS : 38.40
    - Raspbian buster
    - pypy3.5.3 7.0.0 (apt install pypy3)
- setup 4
    - MacBook Pro Late 2013
        - CPU: Intel Core i5 @ 2.4 GHz
    - macOS Catalina (10.15.3)
    - pypy3.6.9 7.3.0 (pyenv install pypy3.6-7.3.0)

(render time, seconds)

| mode | VPS, pypy36 | VPS, python38 | RasPi2B, pypy35 | RasPi3B, pypy35 | MBP2013, pypy36 |
| --- | ---:| ---:| ---:| ---:| ---: |
| [output-image](img/output-image.png) | 0.266 | 1.865 | 6.297 | 3.212 | 0.280 |
| [output-image-vec3](img/output-image-vec3.png) | 0.315 | 2.297 | 6.486 | 3.711 | 0.342 |
| [blue](img/blue.png) | 0.707 | 6.252 | 12.616 | 7.170 | 0.956 |
| [sphere](img/sphere.png) | 0.841 | 7.907 | 15.537 | 8.326 | 1.129 |
| [sphere2](img/sphere2.png) | 0.934 | 7.608 | 15.552 | 8.749 | 1.181 |
| [antialias](img/antialias.png) | 62.843 | 884.650 | 939.587 | 549.351 | 94.840 |
| [diffuse](img/diffuse.png) | 109.713 | 1567.526 | 1749.937 | 1013.685 | 169.924 |
| [diffuse-glay](img/diffuse-glay.png) | 110.881 | 1586.712 | 1746.330 | 1000.875 | 169.769 |
| [sphere-multi](img/sphere-multi.png) | 1.259 | 10.592 | 19.295 | 10.226 | 1.434 |
| [metal](img/metal.png) | 221.577 | 3445.722 | 3413.407 | 2005.142 | 335.289 |
| [metal-dielectric](img/metal-dielectric.png) | 218.255 | 3324.230 | 3499.167 | 1981.587 | 329.822 |
| [metal-dielectric-a](img/metal-dielectric-a.png) | 224.377 | 3408.464 | 3539.292 | 1991.539 | 341.333 |
| [metal-dielectric2](img/metal-dielectric2.png) | 307.219 | 4783.187 | 4745.875 | 2697.381 | 488.966 |
| [metal-dielectric2-a](img/metal-dielectric2-a.png) | 319.007 | 4839.520 | 4979.991 | 2772.328 | 498.040 |
| [metal-fuzz](img/metal-fuzz.png) | 227.517 | 3417.419 | 3461.942 | 1999.956 | 381.543 |
| [camera-blur](img/camera-blur.png) | 356.629 | 4406.891 | 5232.319 | 2896.651 | 545.660 |
| [camera-pos](img/camera-pos.png) | 123.810 | 1752.388 | 1921.965 | 1125.020 | 214.053 |
| [camera-pos2](img/camera-pos2.png) | 137.546 | 2388.454 | 2138.728 | 1235.664 | 229.874 |
| [camera-pos2-2](img/camera-pos2-2.png) | 149.255 | 2538.759 | 2432.056 | 1323.773 | 244.083 |
| [where-next](img/where-next.png) | 4694.568 | **164038.643** | - | 45098.358 | 8104.066 |
