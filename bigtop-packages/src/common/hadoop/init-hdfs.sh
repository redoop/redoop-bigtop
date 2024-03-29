#!/bin/bash -ex
#
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

### Script requires package bigtop-groovy to be installed
# Use this script to initialize HDFS directory structure for various components
# to run. This script can be run from any node in the Hadoop cluster but should
# only be run once by one node only. If you are planning on using oozie, we
# recommend that you run this script from a node that has hive, pig, sqoop, etc.
# installed. Unless you are using psuedo distributed cluster, this node is most
# likely NOT your namenode
# Steps to be performed before running this script:
# 1. Stop the namenode and datanode services if running.
# 2. Format namenode (su -s /bin/bash hdfs hdfs namenode -format).
# 3. Start the namenode and datanode services on appropriate nodes.

# Autodetect JAVA_HOME if not defined
if [ -f /usr/lib/bigtop-utils/bigtop-detect-javahome ]; then
  . /usr/lib/bigtop-utils/bigtop-detect-javahome
fi

HADOOP_LIB_DIR={CRH_DIR}/hadoop/lib
HDFS_LIB_DIR={CRH_DIR}/hadoop-hdfs/lib
HADOOP_DEPENDENCIES="commons-logging*.jar commons-io*.jar guava*.jar commons-configuration*.jar commons-collections*.jar slf4j-api*.jar protobuf-java*.jar commons-lang*.jar servlet-api-2.5.jar"
HDFS_DEPENDENCIES="htrace-core*.jar"
for i in {CRH_DIR}/hadoop/*.jar; do CLASSPATH=$CLASSPATH:$i; done
CLASSPATH=/etc/hadoop/conf:$CLASSPATH:{CRH_DIR}/hadoop-hdfs/hadoop-hdfs.jar
pushd .
cd $HADOOP_LIB_DIR
for d in $HADOOP_DEPENDENCIES; do CLASSPATH=$CLASSPATH:$HADOOP_LIB_DIR/$d; done
for d in $HDFS_DEPENDENCIES;   do CLASSPATH=$CLASSPATH:$HDFS_LIB_DIR/$d; done
popd
su -s /bin/bash hdfs -c "/usr/lib/bigtop-groovy/bin/groovy -classpath $CLASSPATH {CRH_DIR}/hadoop/libexec/init-hcfs.groovy ${CRH_DIR}/hadoop/libexec/init-hcfs.json"
