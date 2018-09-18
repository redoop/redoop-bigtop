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

import glob
import os

from resource_management import *


class Coordinator(Script):
  def install(self, env):
    import params
    env.set_params(params)
    self.install_packages(env)


  def create_presto_log_dir(self, env):
    import params
    env.set_params(params)
    Directory([params.presto_log_dir],
              owner=params.presto_user,
              group=params.presto_group,
              cd_access="a",
              create_parents=True,
              mode=0755
              )

  def chown_presto_pid_dir(self, env):
    import params
    env.set_params(params)
    Execute(("chown", "-R", format("{presto_user}") + ":" + format("{presto_group}"), params.presto_pid_dir),
            sudo=True)

  
  def configure(self, env):
    import params
    env.set_params(params)
    self.create_presto_log_dir(env)

    # create the pid and presto dirs
    Directory([params.presto_pid_dir, params.presto_dir],
              owner=params.presto_user,
              group=params.presto_group,
              cd_access="a",
              create_parents=True,
              mode=0755
    )
    self.chown_presto_pid_dir(env)

    # create presto etc catalog dir
    Directory(params.presto_plugin_config_dir,
              owner="root",
              group="root",
              cd_access="a",
              create_parents=True,
              mode=0755
    )


    key_val_template = '{0}={1}\n'

    # write out config.properties
    config_properties = key_val_template.format('coordinator', 'true') + \
                        key_val_template.format('discovery-server.enabled', 'true')
    for key, value in params.config_properties.iteritems():
      if key in params.memory_configs:
        value += 'GB'
      config_properties += key_val_template.format(key, value)
    File(format("{params.presto_etc_dir}/config.properties"), content=config_properties,
         owner=params.presto_user, group=params.presto_group)


    #  write out connectors.properties
    for key, value in params.connectors_properties.iteritems():
      content = InlineTemplate(value)
      File(format("{params.presto_etc_dir}/catalog/{key}.properties"), content=content,
           owner=params.presto_user, group=params.presto_group)


    # write out jvm.config
    jvm_properties_content = InlineTemplate(params.jvm_properties_content)
    File(format("{params.presto_etc_dir}/jvm.config"), content=jvm_properties_content,
         owner=params.presto_user, group=params.presto_group)


    # write out node.properties
    node_properties = key_val_template.format('node.id', params.hostname)
    for key, value in params.node_properties.iteritems():
      node_properties += key_val_template.format(key, value)
    File(format("{params.presto_etc_dir}/node.properties"), content=node_properties,
         owner=params.presto_user, group=params.presto_group)



  def stop(self, env):
    import params
    self.create_presto_log_dir(env)
    self.chown_presto_pid_dir(env)
    Execute(params.presto_dir + '/bin/launcher ' + params.launcher_options + ' stop >> ' + params.presto_launcher_log_file, user=params.presto_user)


  def start(self, env):
    import params
    self.configure(env)

    Execute(("chown", "-R", format("{presto_user}") + ":" + format("{presto_group}"), "/etc/presto"),
            sudo=True)
    
    Execute(params.presto_dir + '/bin/launcher ' + params.launcher_options + ' start >> ' + params.presto_launcher_log_file, user=params.presto_user)

    pidfile = glob.glob(os.path.join(params.presto_pid_file))[0]
    Logger.info(format("Pid file is: {pidfile}"))


  def status(self, env):
    import params
    env.set_params(params)

    try:
        pid_file = glob.glob(params.presto_pid_file)[0]
    except IndexError:
        pid_file = ''
    check_process_status(pid_file)

if __name__ == "__main__":
  Coordinator().execute()
