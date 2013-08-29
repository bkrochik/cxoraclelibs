#!/bin/bash

echo "Starting........."

mkdir /usr/local/oracle

cp -f libs/instantclient-basic-macos.x32-11.2.0.3.0.zip /usr/local/oracle
cp -f libs/instantclient-sdk-macos.x32-11.2.0.3.0.zip /usr/local/oracle
cp -f libs/cx_Oracle-5.1.2.zip /usr/local/oracle

cd /usr/local/oracle 

unzip /usr/local/oracle/instantclient-basic-macos.x32-11.2.0.3.0.zip
unzip /usr/local/oracle/instantclient-sdk-macos.x32-11.2.0.3.0.zip
unzip /usr/local/oracle/cx_Oracle-5.1.2.zip 

ln -s /usr/local/oracle/instantclient_11_2/libclntsh.dylib.11.1 /usr/local/oracle/instantclient_11_2/libclntsh.dylib
ln -s /usr/local/oracle/instantclient_11_2/libocci.dylib.11.1 /usr/local/oracle/instantclient_11_2/libocci.dylib

if ! grep -q ORACLE_HOME ~/.bash_profile; 
  then
    echo "export ORACLE_HOME=/usr/local/oracle/instantclient_11_2" >> ~/.bash_profile
	echo "export LD_LIBRARY_PATH=$ORACLE_HOME" >> ~/.bash_profile
	echo "export DYLD_LIBRARY_PATH=$ORACLE_HOME" >> ~/.bash_profile
	echo "export VERSIONER_PYTHON_PREFER_32_BIT=yes" >> ~/.bash_profile
	echo "export PATH=$PATH:$ORACLE_HOME" >> ~/.bash_profile
fi
 

sudo python /usr/local/oracle/cx_Oracle-5.1.2/setup.py build
sudo python /usr/local/oracle/cx_Oracle-5.1.2/setup.py install

rm /usr/local/oracle/instantclient-basic-macos.x32-11.2.0.3.0.zip
rm /usr/local/oracle/instantclient-sdk-macos.x32-11.2.0.3.0.zip
rm /usr/local/oracle/cx_Oracle-5.1.2.zip

echo "Finished........."
