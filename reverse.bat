./apktool d test.apk
./dexjar/dex2jar.sh test.apk
mkdir -p result
cp -rv test result
cp -rv test_dex2jar.jar result
rm -rf test
rm -rf test_dex2jar.jar