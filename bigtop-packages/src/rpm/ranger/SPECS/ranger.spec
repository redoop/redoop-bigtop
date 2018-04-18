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
%undefine _missing_build_ids_terminate_build

%define crh_dir /usr/%{crh_tag}/%{crh_version_with_bn}
%define distroselect crh-select
%define component_name ranger
%define etc_ranger /etc/%{component_name}
%define ranger_home %{crh_dir}/%{component_name}
%define ranger_user_home /var/lib/%{component_name}
%define config_ranger %{etc_ranger}/conf
%define config_ranger_dist %{config_ranger}.dist

%define usr_lib_ranger %{crh_dir}/%{component_name}
%define var_log_ranger /var/log/%{component_name}
%define var_run_ranger /var/run/%{component_name}
%define usr_bin /usr/bin
%define man_dir %{ranger_home}/man
%define ranger_services ranger-admin ranger-usersync ranger-tagsync ranger-kms
%define ranger_dist build

%define hadoop_home %{crh_dir}/hadoop
%define hive_home %{crh_dir}/hive
%define hive2_home %{crh_dir}/hive2
%define knox_home %{crh_dir}/knox
%define storm_home %{crh_dir}/storm
%define hbase_home %{crh_dir}/hbase
%define kafka_home %{crh_dir}/kafka
%define atlas_home %{crh_dir}/atlas


%if %{!?suse_version:1}0 && %{!?mgaversion:1}0
%define __os_install_post \
    /usr/lib/rpm/redhat/brp-compress ; \
    /usr/lib/rpm/redhat/brp-strip-static-archive %{__strip} ; \
    /usr/lib/rpm/redhat/brp-strip-comment-note %{__strip} %{__objdump} ; \
    /usr/lib/rpm/brp-python-bytecompile ; \
    %{nil}

%define doc_ranger %{_docdir}/%{component_name}-%{ranger_version}
%define alternatives_cmd alternatives
%global initd_dir %{_sysconfdir}/rc.d/init.d

%endif

%if  %{?suse_version:1}0

# Only tested on openSUSE 11.4. le'ts update it for previous release when confirmed
%if 0%{suse_version} > 1130
%define suse_check \# Define an empty suse_check for compatibility with older sles
%endif

%define doc_ranger %{_docdir}/%{component_name}
%define alternatives_cmd update-alternatives

%global initd_dir %{_sysconfdir}/rc.d

%define __os_install_post \
    %{suse_check} ; \
    /usr/lib/rpm/brp-compress ; \
    %{nil}

%endif


%if  0%{?mgaversion}
%define alternatives_cmd update-alternatives
%global initd_dir %{_sysconfdir}/rc.d/init.d
%endif

# Even though we split the RPM into arch and noarch, it still will build and install
# the entirety of hadoop. Defining this tells RPM not to fail the build
# when it notices that we didn't package most of the installed files.
%define _unpackaged_files_terminate_build 0

# RPM searches perl files for dependancies and this breaks for non packaged perl lib
# like thrift so disable this
%define _use_internal_dependency_generator 0

Name: %{component_name}%{crh_version_as_name}
Version: %{ranger_base_version}
Release: %{ranger_release}
Summary: Ranger is a security framework for securing Hadoop data
License: Apache License v2.0
URL: http://ranger.apache.org/
Group: Development/Libraries
Buildroot: %{_topdir}/INSTALL/%{component_name}-%{version}
Source0: %{component_name}-%{ranger_base_version}.tar.gz
Source1: do-component-build
Source2: install_%{component_name}.sh
Requires: coreutils, /usr/sbin/useradd, /usr/sbin/usermod, /sbin/chkconfig, /sbin/service
Requires: psmisc,ambari-mpacks%{crh_version_as_name}-crh-security
# Sadly, Sun/Oracle JDK in RPM form doesn't provide libjvm.so, which means we have
# to set AutoReq to no in order to minimize confusion. Not ideal, but seems to work.
# I wish there was a way to disable just one auto dependency (libjvm.so)
AutoReq: no


%if  %{?suse_version:1}0
# Required for init scripts
Requires: sh-utils, insserv
%endif

# CentOS 5 does not have any dist macro
# So I will suppose anything that is not Mageia or a SUSE will be a RHEL/CentOS/Fedora
%if %{!?suse_version:1}0 && %{!?mgaversion:1}0
# Required for init scripts
Requires: sh-utils, redhat-lsb
%endif

%if  0%{?mgaversion}
Requires: chkconfig, xinetd-simple-services, zlib, initscripts
%endif

%description 
Ranger is a framework to secure hadoop data 

%package admin
Summary: Web Interface for Ranger 
Group: System/Daemons
Requires: coreutils, /usr/sbin/useradd, /usr/sbin/usermod, /sbin/chkconfig, /sbin/service
Requires: psmisc
# Sadly, Sun/Oracle JDK in RPM form doesn't provide libjvm.so, which means we have
# to set AutoReq to no in order to minimize confusion. Not ideal, but seems to work.
# I wish there was a way to disable just one auto dependency (libjvm.so)
AutoReq: no


%if  %{?suse_version:1}0
# Required for init scripts
Requires: sh-utils, insserv
%endif

# CentOS 5 does not have any dist macro
# So I will suppose anything that is not Mageia or a SUSE will be a RHEL/CentOS/Fedora
%if %{!?suse_version:1}0 && %{!?mgaversion:1}0
# Required for init scripts
Requires: sh-utils, redhat-lsb
%endif

%if  0%{?mgaversion}
Requires: chkconfig, xinetd-simple-services, zlib, initscripts
%endif

%description admin
Ranger-admin is admin component associated with the Ranger framework

%package usersync
Summary: Synchronize User/Group information from Corporate LD/AD or Unix
Group: System/Daemons
Requires: coreutils, /usr/sbin/useradd, /usr/sbin/usermod, /sbin/chkconfig, /sbin/service
Requires: psmisc
# Sadly, Sun/Oracle JDK in RPM form doesn't provide libjvm.so, which means we have
# to set AutoReq to no in order to minimize confusion. Not ideal, but seems to work.
# I wish there was a way to disable just one auto dependency (libjvm.so)
AutoReq: no


%if  %{?suse_version:1}0
# Required for init scripts
Requires: sh-utils, insserv
%endif

# CentOS 5 does not have any dist macro
# So I will suppose anything that is not Mageia or a SUSE will be a RHEL/CentOS/Fedora
%if %{!?suse_version:1}0 && %{!?mgaversion:1}0
# Required for init scripts
Requires: sh-utils, redhat-lsb
%endif

%if  0%{?mgaversion}
Requires: chkconfig, xinetd-simple-services, zlib, initscripts
%endif

%description usersync
Ranger-usersync is user/group synchronization component associated with the Ranger framework

%package kms
Summary: Key Management Server
Group: System/Daemons
Requires: coreutils, /usr/sbin/useradd, /usr/sbin/usermod, /sbin/chkconfig, /sbin/service
Requires: psmisc
# Sadly, Sun/Oracle JDK in RPM form doesn't provide libjvm.so, which means we have
# to set AutoReq to no in order to minimize confusion. Not ideal, but seems to work.
# I wish there was a way to disable just one auto dependency (libjvm.so)
AutoReq: no


%if  %{?suse_version:1}0
# Required for init scripts
Requires: sh-utils, insserv
%endif

# CentOS 5 does not have any dist macro
# So I will suppose anything that is not Mageia or a SUSE will be a RHEL/CentOS/Fedora
%if %{!?suse_version:1}0 && %{!?mgaversion:1}0
# Required for init scripts
Requires: sh-utils, redhat-lsb
%endif

%if  0%{?mgaversion}
Requires: chkconfig, xinetd-simple-services, zlib, initscripts
%endif

%description kms
Ranger-kms is key management server component associated with the Ranger framework


%package tagsync
Summary: Tag Synchronizer
Group: System/Daemons
Requires: coreutils, /usr/sbin/useradd, /usr/sbin/usermod, /sbin/chkconfig, /sbin/service
Requires: psmisc
# Sadly, Sun/Oracle JDK in RPM form doesn't provide libjvm.so, which means we have
# to set AutoReq to no in order to minimize confusion. Not ideal, but seems to work.
# I wish there was a way to disable just one auto dependency (libjvm.so)
AutoReq: no
%if  %{?suse_version:1}0
# Required for init scripts
Requires: sh-utils, insserv
%endif
# CentOS 5 does not have any dist macro
# So I will suppose anything that is not Mageia or a SUSE will be a RHEL/CentOS/Fedora
%if %{!?suse_version:1}0 && %{!?mgaversion:1}0
# Required for init scripts
Requires: sh-utils, redhat-lsb
%endif
%if  0%{?mgaversion}
Requires: chkconfig, xinetd-simple-services, zlib, initscripts
%endif
%description tagsync
Ranger-tagsync is tag synchronizer component associated with the Ranger framework

%package hdfs-plugin
Summary: ranger plugin for hdfs
Group: System/Daemons

%description hdfs-plugin
Ranger HDFS plugnin component runs within namenode to provoide enterprise security using ranger framework

%package yarn-plugin
Summary: ranger plugin for yarn
Group: System/Daemons

%description yarn-plugin
Ranger YARN plugnin component runs within namenode to provoide enterprise security using ranger framework

%package hive-plugin
Summary: ranger plugin for hive
Group: System/Daemons

%description hive-plugin
Ranger Hive plugnin component runs within hiveserver2 to provoide enterprise security using ranger framework

%package hbase-plugin
Summary: ranger plugin for hbase
Group: System/Daemons

%description hbase-plugin
Ranger HBASE plugnin component runs within master and regional servers as co-processor to provoide enterprise security using ranger framework

%package knox-plugin
Summary: ranger plugin for knox
Group: System/Daemons

%description knox-plugin
Ranger KNOX plugnin component runs within knox proxy server to provoide enterprise security using ranger framework

%package storm-plugin
Summary: ranger plugin for storm
Group: System/Daemons

%description storm-plugin
Ranger STORM plugnin component runs within storm to provoide enterprise security using ranger framework

%package kafka-plugin
Summary: ranger plugin for kafka
Group: System/Daemons

%description kafka-plugin
Ranger KAFKA plugnin component runs within namenode to provoide enterprise security using ranger framework

%package atlas-plugin
Summary: ranger plugin for atlas
Group: System/Daemons

%description atlas-plugin
Ranger ATLAS plugnin component runs within namenode to provoide enterprise security using ranger framework

%prep
%setup -q -n %{component_name}-%{ranger_base_version}

%build
bash %{SOURCE1}

%clean
%__rm -rf $RPM_BUILD_ROOT

#########################
#### INSTALL SECTION ####
#########################
%install
%__rm -rf $RPM_BUILD_ROOT
echo
for comp in admin usersync kms tagsync hdfs-plugin yarn-plugin hive-plugin hbase-plugin knox-plugin storm-plugin kafka-plugin atlas-plugin
do
	env RANGER_VERSION=%{ranger_base_version} CRH_VERSION=%{crh_version_with_bn}  CRH_DIR=%{crh_dir} /bin/bash %{SOURCE2} \
  		--prefix=$RPM_BUILD_ROOT \
  		--crh-dir=%{crh_dir} \
  		--build-dir=%{ranger_dist} \
  		--component=${comp} \
  		--doc-dir=$RPM_BUILD_ROOT/%{doc_ranger}
echo;echo
done

%__install -d -m 0755 $RPM_BUILD_ROOT/%{initd_dir}/

%pre admin
getent group ranger >/dev/null || groupadd -r ranger
getent passwd ranger >/dev/null || useradd -c "Ranger" -s /bin/bash -g ranger -m -d /var/lib/%{component_name} ranger 2> /dev/null || :

%pre usersync
getent group ranger >/dev/null || groupadd -r ranger
getent passwd ranger >/dev/null || useradd -c "Ranger" -s /bin/bash -g ranger -m -d /var/lib/%{component_name} ranger 2> /dev/null || :

%pre kms
getent group ranger >/dev/null || groupadd -r ranger
getent passwd ranger >/dev/null || useradd -c "Ranger" -s /bin/bash -g ranger -m -d /var/lib/%{component_name} ranger 2> /dev/null || :

%pre tagsync
getent group ranger >/dev/null || groupadd -r ranger
getent passwd ranger >/dev/null || useradd -c "Ranger" -s /bin/bash -g ranger -m -d /var/lib/%{component_name} ranger 2> /dev/null || :

%post admin
/usr/bin/%{distroselect} --rpm-mode set ranger-admin %{crh_version_with_bn}

if [ !  -e "/etc/ranger/admin/conf" ]; then
    mkdir -p /etc/ranger/admin/conf
    cp -rp /etc/ranger/admin/conf.dist/* /etc/ranger/admin/conf
    chown -R ranger:ranger /etc/ranger/admin/conf
fi

%post usersync
/usr/bin/%{distroselect} --rpm-mode set ranger-usersync %{crh_version_with_bn}

if [ !  -e "/etc/ranger/usersync/conf" ]; then
    mkdir -p /etc/ranger/usersync/conf
    cp -rp /etc/ranger/usersync/conf.dist/* /etc/ranger/usersync/conf
    chown -R ranger:ranger /etc/ranger/usersync/conf
fi
if [ -f %{usr_lib_ranger}-usersync/native/credValidator.uexe ]; then
    chmod u+s %{usr_lib_ranger}-usersync/native/credValidator.uexe
fi

%post kms
/usr/bin/%{distroselect} --rpm-mode set ranger-kms %{crh_version_with_bn}

if [ !  -e "/etc/ranger/kms/conf" ]; then
    mkdir -p /etc/ranger/kms/conf
    cp -rp /etc/ranger/kms/conf.dist/* /etc/ranger/kms/conf
    chown -R ranger:ranger /etc/ranger/kms/conf
fi

%post tagsync
/usr/bin/%{distroselect} --rpm-mode set ranger-tagsync %{crh_version_with_bn}

if [ !  -e "/etc/ranger/tagsync/conf" ]; then
    mkdir -p /etc/ranger/tagsync/conf
    cp -rp /etc/ranger/tagsync/conf.dist/* /etc/ranger/tagsync/conf
    chown -R ranger:ranger /etc/ranger/tagsync/conf
fi

%preun

%postun

#######################
#### FILES SECTION ####
#######################
%files admin
%defattr(-,root,root,755)
%attr(0775,ranger,ranger) %{var_run_ranger}/admin
%attr(0775,ranger,ranger) %{var_log_ranger}/admin
%{usr_lib_ranger}-admin
%config(noreplace) /etc/ranger/admin/conf.dist

%files usersync
%defattr(-,root,root,755)
%attr(0775,ranger,ranger) %{var_run_ranger}/usersync
%attr(0775,ranger,ranger) %{var_log_ranger}/usersync
%{usr_lib_ranger}-usersync
%attr(750,root,ranger) %{usr_lib_ranger}-usersync/native/credValidator.uexe
%config(noreplace) /etc/ranger/usersync/conf.dist

%files kms
%defattr(-,root,root,755)
%attr(0775,ranger,ranger) %{var_run_ranger}/kms
%attr(0775,ranger,ranger) %{var_log_ranger}/kms
%{usr_lib_ranger}-kms
%config(noreplace) /etc/ranger/kms/conf.dist

%files tagsync
%defattr(-,root,root,755)
%attr(0775,ranger,ranger) %{var_run_ranger}/tagsync
%attr(0775,ranger,ranger) %{var_log_ranger}/tagsync
%{usr_lib_ranger}-tagsync
%config(noreplace) /etc/ranger/tagsync/conf.dist

%files hdfs-plugin
%defattr(-,root,root,755)
%{usr_lib_ranger}-hdfs-plugin
%{hadoop_home}/lib

%files yarn-plugin
%defattr(-,root,root,755)
%{usr_lib_ranger}-yarn-plugin
%{hadoop_home}/lib

%files hive-plugin
%defattr(-,root,root,755)
%{usr_lib_ranger}-hive-plugin
%{hive_home}/lib
%{hive2_home}/lib

%files hbase-plugin
%defattr(-,root,root,755)
%{usr_lib_ranger}-hbase-plugin
%{hbase_home}/lib

%files knox-plugin
%defattr(-,root,root,755)
%{usr_lib_ranger}-knox-plugin
%{knox_home}/ext

%files storm-plugin
%defattr(-,root,root,755)
%{usr_lib_ranger}-storm-plugin
%{storm_home}/lib

%files kafka-plugin
%defattr(-,root,root,755)
%{usr_lib_ranger}-kafka-plugin
%{kafka_home}/lib

%files atlas-plugin
%defattr(-,root,root,755)
%{usr_lib_ranger}-atlas-plugin
%{atlas_home}/lib
