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
%define hive2_name hive2
%define hadoop_username hadoop
%define etc_hive2 /etc/%{hive2_name}
%define config_hive2 %{etc_hive2}/conf
%define usr_lib_hive2 %{crh_dir}/%{hive2_name}
%define var_lib_hive2 /var/lib/%{hive2_name}
%define usr_bin %{usr_lib_hive2}/bin
%define hive2_config_virtual hive_active_configuration
%define man_dir %{_mandir}
# After we run "ant package" we'll find the distribution here
%define hive2_dist build/dist

%if  %{!?suse_version:1}0

%define doc_hive2 %{_docdir}/%{hive2_name}-%{hive2_version}
%define alternatives_cmd alternatives

%global initd_dir %{_sysconfdir}/rc.d/init.d

%else

# Only tested on openSUSE 11.4. le'ts update it for previous release when confirmed
%if 0%{suse_version} > 1130
%define suse_check \# Define an empty suse_check for compatibility with older sles
%endif

%define doc_hive2 %{_docdir}/%{hive2_name}
%define alternatives_cmd update-alternatives

%global initd_dir %{_sysconfdir}/rc.d

%define __os_install_post \
    %{suse_check} ; \
    /usr/lib/rpm/brp-compress ; \
    %{nil}

%endif


Name: %{hive2_name}%{crh_version_as_name}
Version: %{hive2_version}
Release: %{hive2_release}
Summary: Hive is a data warehouse infrastructure built on top of Hadoop
License: ASL 2.0
URL: http://hive.apache.org/
Group: Development/Libraries
Buildroot: %{_topdir}/INSTALL/%{hive2_name}-%{version}
BuildArch: noarch
Source0: apache-%{hive2_name}-%{hive2_base_version}-src.tar.gz
Source1: do-component-build
Source2: install_hive2.sh
Source3: init.d.tmpl
Source4: hive-site.xml
Source5: bigtop.bom
#BIGTOP_PATCH_FILES
Requires: hadoop%{crh_version_as_name}-client, bigtop-utils >= 0.7, zookeeper%{crh_version_as_name}
Requires: ranger%{crh_version_as_name}-hive-plugin %{name}-jdbc =  %{version}-%{release}
Conflicts: hadoop-hive
Obsoletes: hive-webinterface

%description 
Hive is a data warehouse infrastructure built on top of Hadoop that provides tools to enable easy data summarization, adhoc querying and analysis of large datasets data stored in Hadoop files. It provides a mechanism to put structure on this data and it also provides a simple query language called Hive QL which is based on SQL and which enables users familiar with SQL to query this data. At the same time, this language also allows traditional map/reduce programmers to be able to plug in their custom mappers and reducers to do more sophisticated analysis which may not be supported by the built-in capabilities of the language.

%if  %{?suse_version:1}0
# Required for init scripts
Requires: insserv
%else
# Required for init scripts
Requires: /lib/lsb/init-functions
%endif

%package jdbc
Summary: Provides libraries necessary to connect to Apache Hive via JDBC
Group: Development/Libraries
Requires: hadoop%{crh_version_as_name}-client

%description jdbc
This package provides libraries necessary to connect to Apache Hive via JDBC


%prep
%setup -q -n apache-%{hive2_name}-%{hive2_base_version}-src

#BIGTOP_PATCH_COMMANDS

%build
bash %{SOURCE1}

#########################
#### INSTALL SECTION ####
#########################
%install
%__rm -rf $RPM_BUILD_ROOT

# set crh_dir value
sed -i -e "s,{CRH_DIR},%{crh_dir}," $RPM_SOURCE_DIR/*

cp $RPM_SOURCE_DIR/hive-site.xml .
env CRH_DIR=%{crh_dir} CRH_VERSION=%{crh_version_with_bn} HIVE2_VERSION=%{hive2_base_version} /bin/bash %{SOURCE2} \
  --prefix=$RPM_BUILD_ROOT \
  --build-dir=%{hive2_dist} \
  --doc-dir=$RPM_BUILD_ROOT/%{doc_hive2}

%__install -d -m 0755 $RPM_BUILD_ROOT/%{initd_dir}/

%__install -d -m 0755 $RPM_BUILD_ROOT/%{_localstatedir}/log/%{hive2_name}
%__install -d -m 0755 $RPM_BUILD_ROOT/%{_localstatedir}/run/%{hive2_name}

# We need to get rid of jars that happen to be shipped in other Bigtop packages
%__rm -f $RPM_BUILD_ROOT/%{usr_lib_hive2}/lib/hbase-*.jar $RPM_BUILD_ROOT/%{usr_lib_hive2}/lib/zookeeper-*.jar
%__ln_s  %{crh_dir}/hbase/hbase.jar %{crh_dir}/zookeeper/zookeeper.jar  $RPM_BUILD_ROOT/%{usr_lib_hive2}/lib/

# Workaround for BIGTOP-583
%__rm -f $RPM_BUILD_ROOT/%{usr_lib_hive2}/lib/slf4j-log4j12-*.jar


%pre
getent group hive >/dev/null || groupadd -r hive
getent passwd hive >/dev/null || useradd -c "Hive" -s /bin/bash -g hive -r -d %{var_lib_hive} hive 2> /dev/null || :

if [[ ! -e "/var/run/hive2" ]]; then
    /usr/bin/install -d -o hive -g hive -m 0755  /var/run/hive2
fi

if [[ ! -e "/var/log/hive2" ]]; then
    /usr/bin/install -d -o hive -g hive -m 0755  /var/log/hive2
fi

if [[ ! -e "/var/lib/hive2/metastore" ]]; then
    /usr/bin/install -d -o hive -g hive -m 0755 /var/lib/hive2/metastore
    chmod 1777 /var/lib/hive2/metastore
fi

# Manage configuration symlink
%post
if [ !  -e "/etc/hive2/conf" ]; then
    rm -f /etc/hive2/conf
    mkdir -p /etc/hive2/conf
    cp -rp /etc/hive2/conf.dist/* /etc/hive2/conf
fi


#######################
#### FILES SECTION ####
#######################
%files
%attr(1777,hive,hive) %dir %{usr_lib_hive2}/metastore
%defattr(-,root,root,755)
%config(noreplace) %{etc_hive2}/conf.dist
%{usr_lib_hive2}
%{usr_bin}/hplsql
%{usr_bin}/hive
%{usr_bin}/beeline
%{usr_bin}/hiveserver2
%attr(0755,hive,hive) %dir %{var_lib_hive2}
%attr(0755,hive,hive) %dir %{_localstatedir}/log/%{hive2_name}
%attr(0755,hive,hive) %dir %{_localstatedir}/run/%{hive2_name}
%doc %{doc_hive2}
%exclude %dir %{usr_lib_hive2}
%exclude %{usr_lib_hive2}/hcatalog
%exclude %dir %{usr_lib_hive2}/lib
%exclude %{usr_lib_hive2}/lib/hive-jdbc-*.jar
%exclude %{usr_lib_hive2}/lib/hive-metastore-*.jar
%exclude %{usr_lib_hive2}/lib/hive-serde-*.jar
%exclude %{usr_lib_hive2}/lib/hive-exec-*.jar
%exclude %{usr_lib_hive2}/lib/libthrift-*.jar
%exclude %{usr_lib_hive2}/lib/hive-service-*.jar
%exclude %{usr_lib_hive2}/lib/libfb303-*.jar
%exclude %{usr_lib_hive2}/lib/log4j-*.jar
%exclude %{usr_lib_hive2}/lib/commons-logging-*.jar

%files jdbc
%defattr(-,root,root,755)
%dir %{usr_lib_hive2}
%dir %{usr_lib_hive2}/lib
%{usr_lib_hive2}/lib/hive-jdbc-*.jar
%{usr_lib_hive2}/lib/hive-metastore-*.jar
%{usr_lib_hive2}/lib/hive-serde-*.jar
%{usr_lib_hive2}/lib/hive-exec-*.jar
%{usr_lib_hive2}/lib/libthrift-*.jar
%{usr_lib_hive2}/lib/hive-service-*.jar
%{usr_lib_hive2}/lib/libfb303-*.jar
%{usr_lib_hive2}/lib/log4j-*.jar
%{usr_lib_hive2}/lib/commons-logging-*.jar
