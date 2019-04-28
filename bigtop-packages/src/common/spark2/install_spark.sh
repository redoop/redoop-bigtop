#!/bin/bash

# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -e

usage() {
  echo "
usage: $0 <options>
  Required not-so-options:
     --build-dir=DIR             path to dist.dir
     --source-dir=DIR            path to package shared files dir
     --prefix=PREFIX             path to install into

  Optional options:
     --doc-dir=DIR               path to install docs into [/usr/share/doc/spark2]
     --lib-dir=DIR               path to install Spark home [$CRH_DIR/spark2]
     --installed-lib-dir=DIR     path where lib-dir will end up on target system
     --bin-dir=DIR               path to install bins [/usr/bin]
     ... [ see source for more similar options ]
  "
  exit 1
}

OPTS=$(getopt \
  -n $0 \
  -o '' \
  -l 'prefix:' \
  -l 'doc-dir:' \
  -l 'lib-dir:' \
  -l 'installed-lib-dir:' \
  -l 'bin-dir:' \
  -l 'source-dir:' \
  -l 'build-dir:' -- "$@")

if [ $? != 0 ] ; then
    usage
fi

eval set -- "$OPTS"
while true ; do
    case "$1" in
        --prefix)
        PREFIX=$2 ; shift 2
        ;;
        --build-dir)
        BUILD_DIR=$2 ; shift 2
        ;;
        --source-dir)
        SOURCE_DIR=$2 ; shift 2
        ;;
        --doc-dir)
        DOC_DIR=$2 ; shift 2
        ;;
        --lib-dir)
        LIB_DIR=$2 ; shift 2
        ;;
        --installed-lib-dir)
        INSTALLED_LIB_DIR=$2 ; shift 2
        ;;
        --bin-dir)
        BIN_DIR=$2 ; shift 2
        ;;
        --)
        shift ; break
        ;;
        *)
        echo "Unknown option: $1"
        usage
        exit 1
        ;;
    esac
done

for var in PREFIX BUILD_DIR SOURCE_DIR; do
  if [ -z "$(eval "echo \$$var")" ]; then
    echo Missing param: $var
    usage
  fi
done

if [ -f "$SOURCE_DIR/bigtop.bom" ]; then
  . $SOURCE_DIR/bigtop.bom
fi

DIST_DIR=${BUILD_DIR}/dist
MAN_DIR=${MAN_DIR:-/usr/share/man/man1}
DOC_DIR=${DOC_DIR:-/usr/share/doc/spark2}
LIB_DIR=${LIB_DIR:-$CRH_DIR/spark2}
INSTALLED_LIB_DIR=${INSTALLED_LIB_DIR:-$CRH_DIR/spark2}
BIN_DIR=${BIN_DIR:-/usr/bin}
CONF_DIR=${CONF_DIR:-/etc/spark2/conf.dist}
PYSPARK_PYTHON=${PYSPARK_PYTHON:-python}

install -d -m 0755 $PREFIX/$LIB_DIR
install -d -m 0755 $PREFIX/$LIB_DIR/bin
install -d -m 0755 $PREFIX/$LIB_DIR/sbin
install -d -m 0755 $PREFIX/$LIB_DIR/yarn
install -d -m 0755 $PREFIX/$LIB_DIR/yarn/lib
install -d -m 0755 $PREFIX/$LIB_DIR/R
install -d -m 0755 $PREFIX/$CONF_DIR
install -d -m 0755 $PREFIX/$DOC_DIR

install -d -m 0755 $PREFIX/var/lib/spark2/
install -d -m 0755 $PREFIX/var/log/spark2/
install -d -m 0755 $PREFIX/var/run/spark2/
install -d -m 0755 $PREFIX/var/run/spark2/work/

rm $DIST_DIR/bin/*.cmd

cp -r $DIST_DIR/* $PREFIX/$LIB_DIR

ln -s $LIB_DIR/examples $PREFIX/$DOC_DIR/

# Move the configuration files to the correct location
mv $PREFIX/$LIB_DIR/conf/* $PREFIX/$CONF_DIR
cp $SOURCE_DIR/spark-env.sh $PREFIX/$CONF_DIR
rmdir $PREFIX/$LIB_DIR/conf
ln -s /etc/spark2/conf $PREFIX/$LIB_DIR/conf

ln -s /var/run/spark2/work $PREFIX/$LIB_DIR/work

rm -f ${PREFIX}/${INSTALLED_LIB_DIR}/python/.gitignore

touch $PREFIX/$LIB_DIR/RELEASE
cat > $PREFIX/$LIB_DIR/RELEASE <<EOF
Spark $SPARK_VERSION
EOF
cp ${BUILD_DIR}/{LICENSE,NOTICE} ${PREFIX}/${LIB_DIR}/

# Version-less symlinks
(cd $PREFIX/$LIB_DIR/examples/jars; ln -s spark-examples*.jar spark-examples.jar)
pushd $PREFIX/$LIB_DIR/yarn/lib
ln -s ../spark-*-yarn-shuffle.jar spark-yarn-shuffle.jar
ln -s ../../jars/datanucleus-api-jdo*.jar datanucleus-api-jdo.jar
ln -s ../../jars/datanucleus-core*.jar datanucleus-core.jar
ln -s ../../jars/datanucleus-rdbms*.jar datanucleus-rdbms.jar
popd
