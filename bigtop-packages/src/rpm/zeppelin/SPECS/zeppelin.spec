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
%define crh_dir /usr/%{crh_tag}/%{crh_version_with_bn}
%define zeppelin_name zeppelin
%define lib_zeppelin %{crh_dir}/%{zeppelin_name}
%define var_lib_zeppelin /var/lib/%{zeppelin_name}
%define var_run_zeppelin /var/run/%{zeppelin_name}
%define var_log_zeppelin /var/log/%{zeppelin_name}
%define bin_zeppelin %{crh_dir}/%{zeppelin_name}/bin
%define etc_zeppelin /etc/%{zeppelin_name}
%define config_zeppelin %{etc_zeppelin}/conf
%define bin /usr/bin
%define man_dir /usr/share/man

%if  %{?suse_version:1}0
%define doc_zeppelin %{_docdir}/%{zeppelin_name}
%define alternatives_cmd update-alternatives
%else
%define doc_zeppelin %{_docdir}/%{zeppelin_name}-%{zeppelin_version}
%define alternatives_cmd alternatives
%endif

# disable repacking jars
%define __os_install_post %{nil}
%define __jar_repack %{nil}

Name: zeppelin%{crh_version_as_name}
Version: %{zeppelin_version}
Release: %{zeppelin_release}
Summary: Web-based notebook for Apache Spark
URL: http://zeppelin.apache.org/
Group: Applications/Engineering
BuildArch: noarch
Buildroot: %(mktemp -ud %{_tmppath}/%{zeppelin_name}-%{version}-%{release}-XXXXXX)
License: ASL 2.0
Source0: %{zeppelin_name}-%{zeppelin_base_version}.tar.gz
Source1: bigtop.bom
Source2: do-component-build
Source3: init.d.tmpl
Source4: install_zeppelin.sh
Source5: zeppelin-env.sh
Source6: zeppelin.svc
Requires: bigtop-utils >= 0.7, hadoop%{crh_version_as_name}-client
Requires: ambari-mpacks%{crh_version_as_name}-crh-BI
Requires(preun): /sbin/service
AutoReq: no

%global initd_dir %{_sysconfdir}/init.d

%if  %{?suse_version:1}0
# Required for init scripts
Requires: insserv
%global initd_dir %{_sysconfdir}/rc.d

%else
# Required for init scripts
Requires: /lib/lsb/init-functions

%global initd_dir %{_sysconfdir}/rc.d/init.d

%endif

%description 
Zeppelin is a web-based notebook that enables interactive data analytics with Apache Spark.
You can make beautiful data-driven, interactive and collaborative documents with SQL, Scala and more.

%prep
%setup -n %{zeppelin_name}-%{zeppelin_base_version}

%build
bash $RPM_SOURCE_DIR/do-component-build

%install
%__rm -rf $RPM_BUILD_ROOT

sed -i -e "s,{CRH_DIR},%{crh_dir}," $RPM_SOURCE_DIR/*

# Init.d scripts directory
%__install -d -m 0755 $RPM_BUILD_ROOT/%{initd_dir}/

env CRH_DIR=%{crh_dir} bash $RPM_SOURCE_DIR/install_zeppelin.sh \
  --build-dir=`pwd`         \
  --source-dir=$RPM_SOURCE_DIR \
  --prefix=$RPM_BUILD_ROOT  \
  --doc-dir=%{doc_zeppelin}

# Install init script
initd_script=$RPM_BUILD_ROOT/%{initd_dir}/%{zeppelin_name}
bash %{SOURCE3} $RPM_SOURCE_DIR/%{zeppelin_name}.svc rpm $initd_script

%pre
getent group zeppelin >/dev/null || groupadd -r zeppelin
getent passwd zeppelin >/dev/null || useradd -c "Zeppelin" -s /sbin/nologin -g zeppelin -r -d %{var_lib_zeppelin} zeppelin 2> /dev/null || :

%post

if [ !  -e "/etc/zeppelin/conf" ]; then
     rm -f /etc/zeppelin/conf
     mkdir -p /etc/zeppelin/conf
     cp -rp /etc/zeppelin/conf.dist/* /etc/zeppelin/conf 
fi

#rm -rf %{crh_dir}/%{zeppelin_name}/lib/hadoop-*.jar 
#cp %{crh_dir}/hadoop/hadoop-common.jar %{crh_dir}/%{zeppelin_name}/lib 
#cp %{crh_dir}/hadoop/lib/curator-client-*.jar %{crh_dir}/%{zeppelin_name}/lib 
#cp %{crh_dir}/hadoop/lib/curator-framework-*.jar %{crh_dir}/%{zeppelin_name}/lib 
#cp %{crh_dir}/hadoop/hadoop-auth.jar %{crh_dir}/%{zeppelin_name}/lib 
#cp %{crh_dir}/hadoop/lib/htrace-core-*-incubating.jar %{crh_dir}/%{zeppelin_name}/lib 

#cp %{crh_dir}/hive/lib/hive-common.jar %{crh_dir}/%{zeppelin_name}/lib 
#cp %{crh_dir}/hive/lib/hive-jdbc.jar %{crh_dir}/%{zeppelin_name}/lib 
#cp %{crh_dir}/hive/lib/hive-metastore.jar %{crh_dir}/%{zeppelin_name}/lib 
#cp %{crh_dir}/hive/lib/hive-service.jar %{crh_dir}/%{zeppelin_name}/lib 
#cp %{crh_dir}/zookeeper/zookeeper-*.jar %{crh_dir}/%{zeppelin_name}/lib 

#cp %{crh_dir}/hbase/lib/netty-all-*.Final.jar %{crh_dir}/%{zeppelin_name}/lib 
#cp %{crh_dir}/hbase/lib/hbase-server-*.jar %{crh_dir}/%{zeppelin_name}/lib 
#cp %{crh_dir}/hbase/lib/hbase-protocol-*.jar %{crh_dir}/%{zeppelin_name}/lib 
#cp %{crh_dir}/hbase/lib/protobuf-java-*.jar %{crh_dir}/%{zeppelin_name}/lib 
#cp %{crh_dir}/hbase/lib/hbase-common-*.jar %{crh_dir}/%{zeppelin_name}/lib 
#cp %{crh_dir}/hbase/lib/hbase-client-*.jar %{crh_dir}/%{zeppelin_name}/lib 
#cp %{crh_dir}/hbase/lib/phoenix-*-HBase-*-server.jar %{crh_dir}/%{zeppelin_name}/lib 
#cp %{crh_dir}/phoenix/lib/phoenix-server-*-HBase-*.jar %{crh_dir}/%{zeppelin_name}/lib 


#rm -rf %{crh_dir}/%{zeppelin_name}/lib/jackson-*.jar 
#cp %{crh_dir}/%{zeppelin_name}/interpreter/flink/jackson-annotations-*.jar %{crh_dir}/%{zeppelin_name}/lib 
#cp %{crh_dir}/%{zeppelin_name}/interpreter/flink/jackson-core-*.jar %{crh_dir}/%{zeppelin_name}/lib 
#cp %{crh_dir}/%{zeppelin_name}/interpreter/flink/jackson-databind-*.jar %{crh_dir}/%{zeppelin_name}/lib 


%{alternatives_cmd} --install %{config_zeppelin} %{zeppelin_name}-conf %{config_zeppelin}.dist 30
chkconfig --add %{zeppelin_name}

%preun
if [ "$1" = 0 ]; then
  %{alternatives_cmd} --remove %{zeppelin_name}-conf %{config_zeppelin}.dist || :
fi

/sbin/service %{zeppelin_name} status > /dev/null 2>&1
if [ $? -eq 0 ]; then
  service %{zeppelin_name} stop > /dev/null 2>&1
fi
chkconfig --del %{zeppelin_name}

#######################
#### FILES SECTION ####
#######################
%files
%defattr(-,root,root,755)
%config(noreplace) %{config_zeppelin}.dist
%doc %{doc_zeppelin}
%{lib_zeppelin}/LICENSE 
%{lib_zeppelin}/README.md 
%{lib_zeppelin}/notebook
%{lib_zeppelin}/*.war
%{lib_zeppelin}/bin
%{lib_zeppelin}/conf
%{lib_zeppelin}/interpreter
%{lib_zeppelin}/licenses
%{lib_zeppelin}/lib
%{lib_zeppelin}/NOTICE
%{config_zeppelin}.dist
%attr(0755,zeppelin,zeppelin) %{etc_zeppelin}
%attr(0755,zeppelin,zeppelin) %{var_lib_zeppelin}
%attr(0755,zeppelin,zeppelin) %{var_run_zeppelin}
%attr(0755,zeppelin,zeppelin) %{var_run_zeppelin}/webapps
%attr(0755,zeppelin,zeppelin) %{var_log_zeppelin}
%attr(0755,root,root)/%{initd_dir}/%{zeppelin_name}
