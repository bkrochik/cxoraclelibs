#!/bin/bash

echo "Starting........."

mkdir /usr/local/cxoracle

cp -f libs/instantclient-basic-macos.x32-11.2.0.3.0.zip /usr/local/cxoracle
cp -f libs/instantclient-sdk-macos.x32-11.2.0.3.0.zip /usr/local/cxoracle
cp -f libs/cx_Oracle-5.1.2.zip /usr/local/cxoracle

cd /usr/local/cxoracle

if ! [ -d /usr/local/cxoracle/instantclient_11_2/ ]; then
	unzip /usr/local/cxoracle/instantclient-basic-macos.x32-11.2.0.3.0.zip
	unzip /usr/local/cxoracle/instantclient-sdk-macos.x32-11.2.0.3.0.zip
fi

if ! [ -d /usr/local/cxoracle/cx_Oracle-5.1.2 ]; then
	unzip /usr/local/cxoracle/cx_Oracle-5.1.2.zip 
fi

ln -s /usr/local/cxoracle/instantclient_11_2/libclntsh.dylib.11.1 /usr/local/cxoracle/instantclient_11_2/libclntsh.dylib
ln -s /usr/local/cxoracle/instantclient_11_2/libocci.dylib.11.1 /usr/local/cxoracle/instantclient_11_2/libocci.dylib

if ! grep -q ORACLE_HOME ~/.bash_profile; 
  then
    echo "export ORACLE_HOME=/usr/local/cxoracle/instantclient_11_2" >> ~/.bash_profile
	echo "export LD_LIBRARY_PATH=$ORACLE_HOME" >> ~/.bash_profile
	echo "export DYLD_LIBRARY_PATH=$ORACLE_HOME" >> ~/.bash_profile
	echo "export VERSIONER_PYTHON_PREFER_32_BIT=yes" >> ~/.bash_profile
	echo "export PATH=$PATH:$ORACLE_HOME" >> ~/.bash_profile
fi

export ARCHFLAGS="-arch x86_64"

cd /usr/local/cxoracle/cx_Oracle-5.1.2/

sudo python setup.py build
sudo python setup.py install

rm /usr/local/cxoracle/instantclient-basic-macos.x32-11.2.0.3.0.zip
rm /usr/local/cxoracle/instantclient-sdk-macos.x32-11.2.0.3.0.zip
rm /usr/local/cxoracle/cx_Oracle-5.1.2.zip

echo "Finished........."
