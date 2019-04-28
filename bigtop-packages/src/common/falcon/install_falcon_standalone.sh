#!/bin/sh

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

#set -ex

usage() {
  echo "
usage: $0 <options>
  Required not-so-options:
     --build-dir=DIR             path to falcon dist.dir
     --prefix=PREFIX             path to install into

  Optional options:
     --doc-dir=DIR               path to install docs into [/usr/share/doc/falcon]
     --lib-dir=DIR               path to install falcon home [$CRH_DIR/falcon]
     --installed-lib-dir=DIR     path where lib-dir will end up on target system
     --bin-dir=DIR               path to install bins [/usr/bin]
     --examples-dir=DIR          path to install examples [doc-dir/examples]
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
  -l 'examples-dir:' \
  -l 'conf-dir:' \
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
        --examples-dir)
        EXAMPLES_DIR=$2 ; shift 2
        ;;
        --conf-dir)
        CONF_DIR=$2 ; shift 2
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

for var in PREFIX BUILD_DIR ; do
  if [ -z "$(eval "echo \$$var")" ]; then
    echo Missing param: $var
    usage
  fi
done

MAN_DIR=${MAN_DIR:-/usr/share/man/man1}
DOC_DIR=${DOC_DIR:-/usr/share/doc/falcon-$FALCON_VERSION}
LIB_DIR=${LIB_DIR:-$CRH_DIR/falcon}
BIN_DIR=${BIN_DIR:-$CRH_DIR/falcon/bin}
#BIN_DIR=${BIN_DIR:-/usr/bin}
ETC_DIR=${ETC_DIR:-/etc/falcon}
CONF_DIR=${CONF_DIR:-${ETC_DIR}/conf.dist}
#ETC_CONF_DIR=${CONF_DIR:-${ETC_DIR}/conf}

install -d -m 0755 $PREFIX/$LIB_DIR
install -d -m 0755 $PREFIX/$LIB_DIR/client/lib
install -d -m 0755 $PREFIX/$LIB_DIR/server
install -d -m 0755 $PREFIX/$LIB_DIR/oozie/ext
install -d -m 0755 $PREFIX/$LIB_DIR/webapp
install -d -m 0755 $PREFIX/$DOC_DIR
install -d -m 0755 $PREFIX/$DOC_DIR/apidocs
install -d -m 0755 $PREFIX/$BIN_DIR
install -d -m 0755 $PREFIX/$ETC_DIR
install -d -m 0755 $PREFIX/$MAN_DIR
#install -d -m 0755 $PREFIX/$ETC_CONF_DIR

cp -ra $BUILD_DIR/docs/* $PREFIX/$DOC_DIR
cp -ra $BUILD_DIR/apidocs/* $PREFIX/$DOC_DIR/apidocs/
cp $BUILD_DIR/*.txt $PREFIX/$DOC_DIR/

cp -ra $BUILD_DIR/client/lib/* ${PREFIX}/${LIB_DIR}/client/lib/
cp -ra $BUILD_DIR/server/webapp/* $PREFIX/falcon/webapp/
cp -ra $BUILD_DIR/oozie/libext/* $PREFIX/$LIB_DIR/oozie/ext

set -x
cp -a $BUILD_DIR/conf $PREFIX/$CONF_DIR
cp -a $BUILD_DIR/bin/* $PREFIX/$BIN_DIR
ln -s /etc/falcon/conf $PREFIX/$LIB_DIR/conf
set +x

# Make a symlink of falcon.jar to falcon-version.jar
ln -s `cd $PREFIX/$LIB_DIR/client/lib/ ; ls falcon*jar` $PREFIX/$LIB_DIR/client/lib/falcon.jar
ln -s `cd $PREFIX/$LIB_DIR/oozie/ext/; ls falcon-oozie-el-extension-*.jar` $PREFIX/$LIB_DIR/oozie/ext/falcon-oozie-el-extension.jar

#wrapper=$PREFIX/usr/bin/falcon
#mkdir -p `dirname $wrapper`
#cat > $wrapper <<EOF
#!/bin/sh

#. /etc/default/falcon

# Autodetect JAVA_HOME if not defined
#if [ -e /usr/libexec/bigtop-detect-javahome ]; then
#  . /usr/libexec/bigtop-detect-javahome
#elif [ -e /usr/lib/bigtop-utils/bigtop-detect-javahome ]; then
#  . /usr/lib/bigtop-utils/bigtop-detect-javahome
#fi

#export HADOOP_CONF=\${HADOOP_CONF:-/etc/hadoop/conf}
#exec /usr/lib/falcon/bin/falcon "\$@"
#EOF

#ln -s /usr/lib/falcon/bin/falcon ${wrapper}

#chmod 755 $wrapper

install -d -m 0755 $PREFIX/usr/bin
