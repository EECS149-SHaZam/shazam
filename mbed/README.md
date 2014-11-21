mbed folder
===========
Here are the files related to programming the FRDM-KL25Z.

## Installing the toolchain
For the C and C++ projects, you will need to install ARM cross-compilers. Binaries are available [here][ARM cross-compilers] for Linux, Mac OS X and Windows.

Do not try to compile the toolchain from source unless you really have to. This can take hours.

### Mac
Here are the steps I used to install the cross-compiler:

1. Download the Mac-specific tarball from [ARM cross-compilers][].

2. Unzip it.

3. In the Terminal, make sure you have the directory `/usr/local/opt`. If you don't have it, create it with 
    
    ```
    mkdir -p /usr/local/opt
    ```

4. Move the cross compiler folder in and rename it at the same time (one line):

    ```
    mv ~/Downloads/gcc-arm-none-eabi-4_8-2014q3 /usr/local/opt/gcc-arm-none-eabi
    ```

5. Link the binaries to `/usr/local/bin`:

    ```
    cd /usr/local/bin
    for prog in ../opt/gcc-arm-none-eabi/bin/* ; do ln -s "$prog"; done
    ```

6. Make sure it's in your PATH:

    ```
    arm-none-eabi-gcc --version
    ```

7. If you get an error, only do the following once. Run this:

    ```
    echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bashrc
    export PATH="/usr/local/bin:$PATH"
    ```
    
    Then try step 6 again. You should see a version message.

Now you have compilers for the FRDM-KL25Z.

## Compiling
Run `make` wherever you see a Makefile. If you have the right compilers, it should just work. The file you drag to the MBED disk will be the one ending in .bin.

[ARM cross-compilers]: https://launchpad.net/gcc-arm-embedded/
