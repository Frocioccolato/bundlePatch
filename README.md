# bundlePatch

This script allows you to patch functions of a react application from the bundle code


USAGE python3 ./tool [fileName.bundle]

if [fileName] is not added, the file index.android.bundle is read by deafualt

At the beginning you will be asked whether to display all the naturally patchable functions, if among these there is the one you want well, otherwise if there is but has a different number of parameters or there is not, the tool changes the name of all the functions called and overwrites a new function with that name, that name will print the parameters to the console and return the original function.

Usually to get the bundle file it is enough to unzip the react apk and go to the assets folder, otherwise try with the apktool tool

The tool modifies the original file, initially creating a copy where the initial file is.
