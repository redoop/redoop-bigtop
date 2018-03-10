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
     --build-dir=DIR             path to ranger dist.dir
     --prefix=PREFIX             path to install into
     --component=rangerComponentName  Ranger component name [admin|hdfs-plugin|yarn-plugin|hive-plugin|hbase-plugin|kafka-plugin|atlas-plugin|...|usersync|kms|tagsync]

  Optional options:
     --app-dir=DIR               path to install ranger app [/usr/lib/ranger/admin]
  "
  exit 1
}

OPTS=$(getopt \
  -n $0 \
  -o '' \
  -l 'build-dir:' \
  -l 'crh-dir:' \
  -l 'prefix:' \
  -l 'doc-dir:' \
  -l 'app-dir:' \
  -l 'component:' \
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
        --crh-dir)
        CRH_DIR=$2 ; shift 2
        ;;
         --component)
        COMPONENT=$2 ; shift 2
        ;;
	--doc-dir)
        DOC_DIR=$2 ; shift 2
        ;;
        --app-dir)
        APP_DIR=$2 ; shift 2
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

for var in PREFIX BUILD_DIR COMPONENT CRH_DIR ; do
  if [ -z "$(eval "echo \$$var")" ]; then
    echo Missing param: $var
    usage
  fi
done

ETC_DIR=${ETC_DIR:-/etc/ranger}
ADMIN_CONF_DIR=${CONF_DIR:-${ETC_DIR}/admin/conf.dist}
USERSYNC_CONF_DIR=${CONF_DIR:-${ETC_DIR}/usersync/conf.dist}
KMS_CONF_DIR=${CONF_DIR:-${ETC_DIR}/kms/conf.dist}
TAGSYNC_CONF_DIR=${CONF_DIR:-${ETC_DIR}/tagsync/conf.dist}

if [ "${APP_DIR}" == "" ]
then
	APP_DIR=ranger-${COMPONENT}
fi

# Create the required directories.
install -d -m 0755 ${PREFIX}/${CRH_DIR}/$APP_DIR

install -d -m 0755 ${PREFIX}/$ETC_DIR/{admin,usersync,kms,tagsync}

install -d -m 0755 ${PREFIX}/var/{log,run}/ranger/{admin,usersync,kms,tagsync}


# Copy artifacts to the appropriate Linux locations.
cp -r ${BUILD_DIR}/ranger-*-${COMPONENT}/* ${PREFIX}/${CRH_DIR}/${APP_DIR}/


if [[ "${COMPONENT}" = "admin" ]]
then
cp -a ${BUILD_DIR}/ranger-*-${COMPONENT}/ews/webapp/WEB-INF/classes/conf.dist ${PREFIX}/${ADMIN_CONF_DIR}
ln -s /etc/ranger/admin/conf ${PREFIX}/${CRH_DIR}/${APP_DIR}/conf
ln -s ${CRH_DIR}/${APP_DIR}/conf ${PREFIX}/${CRH_DIR}/${APP_DIR}/ews/webapp/WEB-INF/classes/conf
#ln -s /var/log/ranger/admin ${PREFIX}/${CRH_DIR}/${APP_DIR}/ews/logs
ln -s ${CRH_DIR}/${APP_DIR}/ews/start-ranger-admin.sh ${PREFIX}/${CRH_DIR}/${APP_DIR}/ews/ranger-admin-start
ln -s ${CRH_DIR}/${APP_DIR}/ews/stop-ranger-admin.sh ${PREFIX}/${CRH_DIR}/${APP_DIR}/ews/ranger-admin-stop
fi

if [[ "${COMPONENT}" = "usersync" ]]
then
echo "usersync"
cp -a ${BUILD_DIR}/ranger-*-${COMPONENT}/conf.dist ${PREFIX}/${USERSYNC_CONF_DIR}
ln -s /etc/ranger/usersync/conf ${PREFIX}/${CRH_DIR}/${APP_DIR}/conf
#ln -s /var/log/ranger/usersync ${PREFIX}/${CRH_DIR}/${APP_DIR}/logs
ln -s ${CRH_DIR}/${APP_DIR}/start.sh ${PREFIX}/${CRH_DIR}/${APP_DIR}/ranger-usersync-start
ln -s ${CRH_DIR}/${APP_DIR}/stop.sh ${PREFIX}/${CRH_DIR}/${APP_DIR}/ranger-usersync-stop
fi

if [[ "${COMPONENT}" = "kms" ]]
then
echo "kms"
cp -a ${BUILD_DIR}/ranger-*-${COMPONENT}/ews/webapp/WEB-INF/classes/conf.dist ${PREFIX}/${KMS_CONF_DIR}
ln -s /etc/ranger/kms/conf ${PREFIX}/${CRH_DIR}/${APP_DIR}/conf
ln -s ${CRH_DIR}/${APP_DIR}/conf ${PREFIX}/${CRH_DIR}/${APP_DIR}/ews/webapp/WEB-INF/classes/conf
#ln -s /var/log/ranger/kms ${PREFIX}/${CRH_DIR}/${APP_DIR}/logs
fi

if [[ "${COMPONENT}" = "tagsync" ]]
then
echo "tagsync"
cp -a ${BUILD_DIR}/ranger-*-${COMPONENT}/conf.dist ${PREFIX}/${TAGSYNC_CONF_DIR}
ln -s /etc/ranger/tagsync/conf ${PREFIX}/${CRH_DIR}/${APP_DIR}/conf
#ln -s /var/log/ranger/tagsync ${PREFIX}/${CRH_DIR}/${APP_DIR}/logs
fi

# For other Components
if [[ "${COMPONENT}" = "hive-plugin" || "${COMPONENT}" = "hbase-plugin" || "${COMPONENT}" = "storm-plugin" || "${COMPONENT}" = "hdfs-plugin" || "${COMPONENT}" = "yarn-plugin" || "${COMPONENT}" = "kafka-plugin" || "${COMPONENT}" = "atlas-plugin" || "${COMPONENT}" = "knox-plugin" ]]
then
	CRH_COMPONENT=${COMPONENT}
	[[ "${COMPONENT}" = "hdfs-plugin" ]] && CRH_COMPONENT="hadoop"
	[[ "${COMPONENT}" = "yarn-plugin" ]] && CRH_COMPONENT="hadoop"
	[[ "${COMPONENT}" = "storm-plugin" ]] && CRH_COMPONENT="storm"
	[[ "${COMPONENT}" = "hbase-plugin" ]] && CRH_COMPONENT="hbase"
	[[ "${COMPONENT}" = "hive-plugin" ]] && CRH_COMPONENT="hive"
	[[ "${COMPONENT}" = "kafka-plugin" ]] && CRH_COMPONENT="kafka"
	[[ "${COMPONENT}" = "atlas-plugin" ]] && CRH_COMPONENT="atlas"
	[[ "${COMPONENT}" = "knox-plugin" ]] && CRH_COMPONENT="knox"
	[[ "${COMPONENT}" = "knox-plugin" ]] && lib="ext" || lib="lib"
	install -d -m 0755 ${PREFIX}/${CRH_DIR}/${CRH_COMPONENT}/${lib}
	cp -r $BUILD_DIR/ranger-*-${COMPONENT}/lib/* ${PREFIX}/${CRH_DIR}/${CRH_COMPONENT}/${lib}/
	[[ "${COMPONENT}" = "hive-plugin" ]] && install -d -m 0755 ${PREFIX}/${CRH_DIR}/hive2/${lib}/ && cp -r $BUILD_DIR/ranger-*-${COMPONENT}/lib/* ${PREFIX}/${CRH_DIR}/hive2/${lib}/
	[[ "${COMPONENT}" = "yarn-plugin" ]] || ln -s /usr/share/java/ojdbc6.jar ${PREFIX}/${CRH_DIR}/${CRH_COMPONENT}/${lib}/ojdbc6.jar
fi
