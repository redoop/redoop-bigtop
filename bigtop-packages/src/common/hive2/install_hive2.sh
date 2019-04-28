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


usage() {
  echo "
usage: $0 <options>
  Required not-so-options:
     --build-dir=DIR             path to hive2/build/dist
     --prefix=PREFIX             path to install into

  Optional options:
     --doc-dir=DIR               path to install docs into [/usr/share/doc/hive2]
     --hive2-dir=DIR               path to install hive2 home [/usr/lib/hive2]
     --installed-hive2-dir=DIR     path where hive2-dir will end up on target system
     --bin-dir=DIR               path to install bins [/usr/bin]
     --examples-dir=DIR          path to install examples [doc-dir/examples]
     --hcatalog-dir=DIR          path to install hcatalog [/usr/lib/hcatalog]
     --installed-hcatalog-dir=DIR path where hcatalog-dir will end up on target system
     ... [ see source for more similar options ]
  "
  exit 1
}

OPTS=$(getopt \
  -n $0 \
  -o '' \
  -l 'prefix:' \
  -l 'doc-dir:' \
  -l 'hive2-dir:' \
  -l 'installed-hive2-dir:' \
  -l 'bin-dir:' \
  -l 'examples-dir:' \
  -l 'python-dir:' \
  -l 'hcatalog-dir:' \
  -l 'installed-hcatalog-dir:' \
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
        --hive2-dir)
        HIVE2_DIR=$2 ; shift 2
        ;;
        --installed-hive2-dir)
        INSTALLED_HIVE2_DIR=$2 ; shift 2
        ;;
        --bin-dir)
        BIN_DIR=$2 ; shift 2
        ;;
        --examples-dir)
        EXAMPLES_DIR=$2 ; shift 2
        ;;
        --python-dir)
        PYTHON_DIR=$2 ; shift 2
        ;;
        --hcatalog-dir)
        HCATALOG_DIR=$2 ; shift 2
        ;;
        --installed-hcatalog-dir)
        INSTALLED_HCATALOG_DIR=$2 ; shift 2
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

MAN_DIR=$PREFIX/usr/share/man/man1
DOC_DIR=${DOC_DIR:-$PREFIX/usr/share/doc/hive2}
HIVE2_DIR=${HIVE2_DIR:-$PREFIX/$CRH_DIR/hive2}
INSTALLED_HIVE2_DIR=${INSTALLED_HIVE2_DIR:-$CRH_DIR/hive2}
EXAMPLES_DIR=${EXAMPLES_DIR:-$DOC_DIR/examples}
BIN_DIR=${BIN_DIR:-$PREFIX/$CRH_DIR/hive2/bin}
PYTHON_DIR=${PYTHON_DIR:-$HIVE2_DIR/lib/py}
CONF_DIR=/etc/hive2
CONF_DIST_DIR=/etc/hive2/conf.dist

# First we'll move everything into lib
install -d -m 0755 ${HIVE2_DIR}
(cd ${BUILD_DIR} && tar -cf - .)|(cd ${HIVE2_DIR} && tar -xf -)

for jar in `ls ${HIVE2_DIR}/lib/hive-*.jar | grep -v 'standalone.jar'`; do
    base=`basename $jar`
    (cd ${HIVE2_DIR}/lib && ln -s $base ${base/-[0-9].*/.jar})
done

for thing in conf README.txt examples lib/py;
do
  rm -rf ${HIVE2_DIR}/$thing
done

install -d -m 0755 ${BIN_DIR}
for file in hive beeline hiveserver2 hplsql
do
  mv ${HIVE2_DIR}/bin/$file ${HIVE2_DIR}/bin/$file.distro
  wrapper=$BIN_DIR/$file
  cat >>$wrapper <<EOF
#!/bin/bash

# Autodetect JAVA_HOME if not defined
if [ -e /usr/libexec/bigtop-detect-javahome ]; then
  . /usr/libexec/bigtop-detect-javahome
elif [ -e /usr/lib/bigtop-utils/bigtop-detect-javahome ]; then
  . /usr/lib/bigtop-utils/bigtop-detect-javahome
fi

BIGTOP_DEFAULTS_DIR=\${BIGTOP_DEFAULTS_DIR-/etc/default}
[ -n "\${BIGTOP_DEFAULTS_DIR}" -a -r \${BIGTOP_DEFAULTS_DIR}/hbase ] && . \${BIGTOP_DEFAULTS_DIR}/hbase


export HIVE_HOME=\${HIVE_HOME:-$CRH_DIR/hive2}
export HADOOP_HOME=\${HADOOP_HOME:-$CRH_DIR/hadoop}
export IS_HIVE2=true
export HADOOP_CLASSPATH=:$CRH_DIR/tez_hive2/*:${CRH_DIR}/tez_hive2/lib/*:${CRH_DIR}/tez_hive2/conf

exec "\${HIVE_HOME}/bin/$file.distro" "\$@"
EOF
  chmod 755 $wrapper
  cp $BIN_DIR/$file ${HIVE2_DIR}/bin/$file
done


# Config
install -d -m 0755 ${PREFIX}${CONF_DIST_DIR}
(cd ${BUILD_DIR}/conf && tar -cf - .)|(cd ${PREFIX}${CONF_DIST_DIR} && tar -xf -)
for template in hive-exec-log4j2.properties hive-log4j2.properties
do
  mv ${PREFIX}${CONF_DIST_DIR}/${template}.template ${PREFIX}${CONF_DIST_DIR}/${template}
done
cp hive-site.xml ${PREFIX}${CONF_DIST_DIR}
sed -i -e "s|@VERSION@|${HIVE2_VERSION}|" ${PREFIX}${CONF_DIST_DIR}/hive-site.xml

ln -s ${CONF_DIR}/conf $HIVE2_DIR/conf


# Docs
install -d -m 0755 ${DOC_DIR}
cp ${BUILD_DIR}/README.txt ${DOC_DIR}
mv ${HIVE2_DIR}/NOTICE ${DOC_DIR}
mv ${HIVE2_DIR}/LICENSE ${DOC_DIR}
mv ${HIVE2_DIR}/RELEASE_NOTES.txt ${DOC_DIR}


# Examples
install -d -m 0755 ${EXAMPLES_DIR}
cp -a ${BUILD_DIR}/examples/* ${EXAMPLES_DIR}

# Python libs
install -d -m 0755 ${PYTHON_DIR}
(cd $BUILD_DIR/lib/py && tar cf - .) | (cd ${PYTHON_DIR} && tar xf -)
chmod 755 ${PYTHON_DIR}/hive_metastore/*-remote

# Dir for Metastore DB
install -d -m 1777 ${HIVE2_DIR}/metastore/

# We need to remove the .war files. No longer supported.
rm -f ${HIVE2_DIR}/lib/hive-hwi*.war

# Remove some source which gets installed
rm -rf ${HIVE2_DIR}/lib/php/ext


# Provide the runtime dirs
install -d -m 0755 $PREFIX/var/lib/hive2
install -d -m 0755 $PREFIX/var/log/hive2
install -d -m 0755 $PREFIX/var/run/hive2


# Remove Windows files
find ${HIVE2_DIR}/bin -name '*.cmd' | xargs rm -f
