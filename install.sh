#!/bin/bash

echo "Starting........."

mkdir /usr/local/cxoracle

cp -f libs/instantclient-basic-macos.x32-11.2.0.3.0.zip /usr/local/cxoracle
cp -f libs/instantclient-sdk-macos.x32-11.2.0.3.0.zip /usr/local/cxoracle
cp -f libs/cx_Oracle-5.1.2.zip /usr/local/cxoracle

cd /usr/local/cxoracle

echo "Unzipping........."

if ! [ -d /usr/local/cxoracle/instantclient_11_2/ ]; then
	unzip /usr/local/cxoracle/instantclient-basic-macos.x32-11.2.0.3.0.zip
	unzip /usr/local/cxoracle/instantclient-sdk-macos.x32-11.2.0.3.0.zip
fi

if ! [ -d /usr/local/cxoracle/cx_Oracle-5.1.2 ]; then
	unzip /usr/local/cxoracle/cx_Oracle-5.1.2.zip 
fi

echo "Creating simbolics links........."

ln -s /usr/local/cxoracle/instantclient_11_2/libclntsh.dylib.11.1 /usr/local/cxoracle/instantclient_11_2/libclntsh.dylib
ln -s /usr/local/cxoracle/instantclient_11_2/libocci.dylib.11.1 /usr/local/cxoracle/instantclient_11_2/libocci.dylib

echo "Configuring exports............"

sed -n '/LD_LIBRARY_PATH/!p' ~/.bash_profile > temp.txt
mv temp.txt  ~/.bash_profile

if ! grep -q ORACLE_HOME ~/.bash_profile; 
  then
    echo "export ORACLE_HOME=/usr/local/cxoracle/instantclient_11_2" >> ~/.bash_profile
	echo "export PATH=$PATH:$ORACLE_HOME" >> ~/.bash_profile
	echo "export VERSIONER_PYTHON_PREFER_32_BIT=yes" >> ~/.bash_profile
fi

echo "Reloading Bash.........."
source  ~/.bash_profile            

if ! grep -q LD_LIBRARY_PATH ~/.bash_profile; 
  then
   echo "export LD_LIBRARY_PATH=$ORACLE_HOME" >> ~/.bash_profile
   echo "export DYLD_LIBRARY_PATH=$ORACLE_HOME" >> ~/.bash_profile
fi

echo "Setting temporal arch............"

export ARCHFLAGS="-arch x86_64"

cd /usr/local/cxoracle/cx_Oracle-5.1.2/

echo "Installing cx_Oracle............"

sudo python setup.py build
sudo python setup.py install

rm /usr/local/cxoracle/instantclient-basic-macos.x32-11.2.0.3.0.zip
rm /usr/local/cxoracle/instantclient-sdk-macos.x32-11.2.0.3.0.zip
rm /usr/local/cxoracle/cx_Oracle-5.1.2.zip

echo "Reloading Bash.........."

source  ~/.bash_profile

echo "Finished........."
