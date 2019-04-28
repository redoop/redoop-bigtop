# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements. See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

class nfs::client::service inherits nfs::client::params {

  include nfs::client::install
  
  service { $portmap_service:
    ensure  => running,
    enable  => true,
    require => Package[$package_names],
  }

  if ($nfs_version >= 4) {
    service { $idmapd_service:
      ensure  => running,
      enable  => true,
      require => [ Service[$portmap_service], Package[$package_names] ],
      pattern => "rpc.idmapd",
    }
  }
}
