#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import functools
import os
import re
import socket

from resource_management import *


# server configurations
config = Script.get_config()
stack_root = Script.get_stack_root()

# e.g. /var/lib/ambari-agent/cache/stacks/HDP/2.6/services/presto/package
service_packagedir = os.path.realpath(__file__).split('/scripts')[0]

presto_dirname = 'presto'
install_dir = os.path.join(stack_root, "current")


# New Cluster Stack Version that is defined during the RESTART of a Rolling Upgrade
version = default("/commandParams/version", None)
stack_name = default("/hostLevelParams/stack_name", None)


# params from config-properties
config_properties = config['configurations']['config-properties']

# params from connectors-properties
connectors_properties = config['configurations']['connectors-properties']
memory_configs = ['query.max-memory', 'query.max-memory-per-node', 'query.max-total-memory-per-node']

# params from jvm-properties
jvm_properties_content = config['configurations']['jvm-config']['jvm_config']

# params from node-properties
node_properties = config['configurations']['node-properties']

# params from presto-env
presto_user = config['configurations']['presto-env']['presto_user']
presto_group = config['configurations']['presto-env']['presto_group']
presto_etc_dir = config['configurations']['presto-env']['presto_etc_dir']
presto_log_dir = config['configurations']['presto-env']['presto_log_dir']
presto_pid_dir = config['configurations']['presto-env']['presto_pid_dir']

presto_pid_file = os.path.join(presto_pid_dir, 'launcher.pid')
presto_launcher_log_file = os.path.join(presto_log_dir, 'launcher.log')
presto_server_log_file = os.path.join(presto_log_dir, 'server.log')


presto_dir = os.path.join(*[install_dir, presto_dirname])
presto_plugin_config_dir = os.path.join(presto_etc_dir, 'catalog/')


# launcher options
launcher_options = " --etc-dir=" + presto_etc_dir + " --pid-file=" + presto_pid_file + " --launcher-log-file=" + presto_launcher_log_file + " --server-log-file=" + presto_launcher_log_file

# node hostname
hostname = config["hostname"]

# hdfs user
hdfs_user = config['configurations']['hadoop-env']['hdfs_user']

# hive metastore uris
hive_metastore_uris = config['configurations']['hive-site']['hive.metastore.uris']
