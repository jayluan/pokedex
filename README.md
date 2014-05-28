pokedex
=======
Hopefully this eventually becomes our cool pokedex. Recognizes pokemon sprites using machine learning!

some code referenced from here:
http://www.juergenwiki.de/work/wiki/doku.php?id=public%3ahog_descriptor_computation_and_visualization

Setup Instructions:
=================
Install dependencies for openCV:
$ sudo apt-get install libavformat-dev libgtk2.0-dev pkg-config cmake libswscale-dev bzip2

clone the latest openCV repo:
$ git clone https://github.com/Itseez/opencv.git

cd into your opencv directory, and create a new folder called release:
$ cd opencv && mkdir release && cd release/

call cmake within release:
$ cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D BUILD_PYTHON_SUPPORT=ON ..

after configuration is done, make (I used 4 cores) and install:
$ make -j4
$ make install

setup correct paths so linker can find everything:
$ export LD_LIBRARY_PATH=/usr/local/lib/:$LD_LIBRARY_PATH
$ sudo ldconfig

pull this repository to somwhere:
$ git clone https://github.com/jayluan/pokedex.git
$ cd pokedex
$ mkdir build && cd build
$ cmake ..
$ make
