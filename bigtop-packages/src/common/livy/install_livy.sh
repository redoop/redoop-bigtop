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
set -xe
usage() {
  echo "
usage: $0 <options>
  Required not-so-options:
     --build-dir=DIR             path to livy dist.dir
     --prefix=PREFIX             path to install into
  Optional options:
     --doc-dir=DIR               path to install docs into [/usr/share/doc/livy]
     --lib-dir=DIR               path to install livy home [/usr/lib/livy]
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
  -l 'crh-dir:' \
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
        --crh-dir)
        CRH_DIR=$2 ; shift 2
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
for var in PREFIX BUILD_DIR CRH_DIR; do
  if [ -z "$(eval "echo \$$var")" ]; then
    echo Missing param: $var
    usage
  fi
done

LIB_DIR=${LIB_DIR:-${CRH_DIR}/livy}
BIN_DIR=${BIN_DIR:-${CRH_DIR}/livy/bin}
ETC_DIR=${ETC_DIR:-/etc/livy}
CONF_DIR=${CONF_DIR:-${ETC_DIR}/conf.dist}
JARS_DIR=${JARS_DIR:-${CRH_DIR}/livy/jars}
REPL_JARS=${REPL_JARS:-${CRH_DIR}/livy/repl-jars}
RSC_JARS=${RSC_JARS:-${CRH_DIR}/livy/rsc-jars}

install -d -m 0755 ${PREFIX}/$LIB_DIR/
install -d -m 0755 ${PREFIX}/$BIN_DIR
install -d -m 0755 ${PREFIX}/$LIB_DIR/jars
install -d -m 0755 ${PREFIX}/$LIB_DIR/repl-jars
install -d -m 0755 ${PREFIX}/$LIB_DIR/rsc-jars

echo ${BUILD_DIR}
cp -ra $BUILD_DIR/bin/* ${PREFIX}/$BIN_DIR
cp -ra $BUILD_DIR/server/target/jars/* ${PREFIX}/${JARS_DIR}/
cp -ra $BUILD_DIR/repl/scala*1/target/jars/* ${PREFIX}/${REPL_JARS}/
cp -ra $BUILD_DIR/rsc/target/jars/* ${PREFIX}/${RSC_JARS}/

if [ ! -e "${PREFIX}/${ETC_DIR}" ]; then
    rm -f ${PREFIX}/${ETC_DIR}
    mkdir -p ${PREFIX}/${ETC_DIR}
fi
cp -a $BUILD_DIR/conf ${PREFIX}/$CONF_DIR
ln -s /etc/livy/conf ${PREFIX}/${LIB_DIR}/conf

# Copy in the /usr/bin/livy wrapper
mv ${PREFIX}/$BIN_DIR/livy-server ${PREFIX}/$BIN_DIR/livy-server.distro
cat > ${PREFIX}/$BIN_DIR/livy-server <<EOF
#!/bin/bash
. /etc/default/hadoop
# Autodetect JAVA_HOME if not defined
if [ -e /usr/libexec/bigtop-detect-javahome ]; then
  . /usr/libexec/bigtop-detect-javahome
elif [ -e /usr/lib/bigtop-utils/bigtop-detect-javahome ]; then
  . /usr/lib/bigtop-utils/bigtop-detect-javahome
fi
BIGTOP_DEFAULTS_DIR=\${BIGTOP_DEFAULTS_DIR-/etc/default}
[ -n "\${BIGTOP_DEFAULTS_DIR}" -a -r \${BIGTOP_DEFAULTS_DIR}/storm ] && . \${BIGTOP_DEFAULTS_DIR}/livy
exec ${CRH_DIR}/livy/bin/livy-server.distro "\$@"
EOF
chmod 755 ${PREFIX}/${BIN_DIR}/livy-server