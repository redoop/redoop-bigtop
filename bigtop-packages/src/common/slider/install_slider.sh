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

set -e

usage() {
  echo "
usage: $0 <options>
  Required not-so-options:
     --build-dir=DIR             path to slider dist.dir
     --prefix=PREFIX             path to install into

  Optional options:
     --app-dir=DIR               path to install slider app [/usr/lib/slider]
     --conf-dir=DIR              path to install config [/etc/slider/conf]
     --data-dir=DIR              path to install data [/var/lib/slider/data]
     --logs-dir=DIR              path to prepare for logs [/var/log/slider]
     --pids-dir=DIR              path to prepare for pids [/var/run/slider]
  "
  exit 1
}

OPTS=$(getopt \
  -n $0 \
  -o '' \
  -l 'build-dir:' \
  -l 'hdp-dir:' \
  -l 'prefix:' \
  -l 'app-dir:' \
  -l 'conf-dir:' \
  -l 'data-dir:' \
  -l 'logs-dir:' \
  -l 'pids-dir:' \
  -- "$@")

if [ $? != 0 ] ; then
    usage
fi

eval set -- "$OPTS"
while true ; do
    case "$1" in
        --build-dir)
        BUILD_DIR=$2 ; shift 2
        ;;
        --prefix)
        PREFIX=$2 ; shift 2
        ;;
        --hdp-dir)
        CRH_DIR=$2 ; shift 2
        ;;
         --app-dir)
        APP_DIR=$2 ; shift 2
        ;;
        --conf-dir)
        CONF_DIR=$2 ; shift 2
        ;;
        --data-dir)
        DATA_DIR=$2 ; shift 2
        ;;
        --logs-dir)
        LOGS_DIR=$2 ; shift 2
        ;;
        --pids-dir)
        PIDS_DIR=$2 ; shift 2
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

for var in PREFIX BUILD_DIR HDP_DIR ; do
  if [ -z "$(eval "echo \$$var")" ]; then
    echo Missing param: $var
    usage
  fi
done


APP_DIR=${APP_DIR:-/slider}
CONF_DIR=${CONF_DIR:-/etc/slider/conf.dist}
LOGS_DIR=${LOGS_DIR:-/var/log/slider}
PIDS_DIR=${PIDS_DIR:-/var/run/slider}

# Create the required directories.
install -d -m 0755 ${PREFIX}/${CRH_DIR}/$APP_DIR
install -d -m 0755 ${PREFIX}/${CRH_DIR}/$APP_DIR/bin
install -d -m 0755 ${PREFIX}/${CRH_DIR}/$APP_DIR/lib
install -d -m 0755 ${PREFIX}/${CRH_DIR}/$APP_DIR/agent
install -d -m 0755 ${PREFIX}/${CRH_DIR}/$CONF_DIR

# Copy artifacts to the appropriate Linux locations.
cp $BUILD_DIR/README.md ${PREFIX}/${CRH_DIR}/${APP_DIR}/
cp $BUILD_DIR/LICENSE ${PREFIX}/${CRH_DIR}/${APP_DIR}/
cp -ra $BUILD_DIR/bin/* ${PREFIX}/${CRH_DIR}/${APP_DIR}/bin/
cp -ra $BUILD_DIR/lib/* ${PREFIX}/${CRH_DIR}/${APP_DIR}/lib/
cp -ra $BUILD_DIR/agent/* ${PREFIX}/${CRH_DIR}/${APP_DIR}/agent/
cp -ra $BUILD_DIR/conf/* ${PREFIX}/${CRH_DIR}/${CONF_DIR}/


# Setup the symlinks from the app dir.
ln -s -f /etc/slider/conf ${PREFIX}/${CRH_DIR}/$APP_DIR/conf


