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
%define component_name falcon
%define distroselect hdp_select
%define etc_falcon_conf /etc/%{component_name}/conf
%define etc_falcon_conf_dist /etc/%{component_name}/conf.dist
%define falcon_home %{crh_dir}/%{component_name}
%define falcon_user_home /var/lib/%{component_name}
%define bin_falcon %{falcon_home}/bin
%define lib_falcon %{falcon_home}
%define conf_falcon %{falcon_home}/conf
%define logs_falcon %{falcon_home}/logs
%define pids_falcon %{falcon_home}/pids
%define webapps_falcon %{falcon_home}/server/webapp

%define man_dir %{falcon_home}/man
%define falcon_username falcon

%if  %{?suse_version:1}0

# Only tested on openSUSE 11.4. le'ts update it for previous release when confirmed
%if 0%{suse_version} > 1130
%define suse_check \# Define an empty suse_check for compatibility with older sles
%endif

# SLES is more strict anc check all symlinks point to valid path
# But we do point to a hadoop jar which is not there at build time
# (but would be at install time).
# Since our package build system does not handle dependencies,
# these symlink checks are deactivated
%define __os_install_post \
    %{suse_check} ; \
    /usr/lib/rpm/brp-compress ; \
    %{nil}

%define doc_falcon %{_docdir}/%{component_name}-%{falcon_base_version}
%global initd_dir %{_sysconfdir}/rc.d/init.d
%define alternatives_cmd alternatives

%else

# CentOS 5 does not have any dist macro
# So I will suppose anything that is not Mageia or a SUSE will be a RHEL/CentOS/Fedora
%if %{!?mgaversion:1}0

# FIXME: brp-repack-jars uses unzip to expand jar files
# Unfortunately guice-2.0.jar pulled by ivy contains some files and directories without any read permission
# and make whole process to fail.
# So for now brp-repack-jars is being deactivated until this is fixed.
# See BIGTOP-294
%define __os_install_post \
    /usr/lib/rpm/redhat/brp-compress ; \
    /usr/lib/rpm/redhat/brp-strip-static-archive %{__strip} ; \
    /usr/lib/rpm/redhat/brp-strip-comment-note %{__strip} %{__objdump} ; \
    /usr/lib/rpm/brp-python-bytecompile ; \
    %{nil}
%endif

%define doc_falcon %{_docdir}/%{component_name}-%{falcon_base_version}
%global initd_dir %{_sysconfdir}/rc.d/init.d
%define alternatives_cmd alternatives

%endif


Name: falcon%{crh_version_as_name}
Version: %{falcon_base_version}
Release: %{falcon_release}
Summary: Falcon is a feed processing and feed management system aimed at making it easier for end consumers to onboard their feed processing and feed management on hadoop clusters.
URL: http://falcon.apache.org/
Group: Development/Libraries
Buildroot: %{_topdir}/INSTALL/%{component_name}-%{version}
License: APL2
Source0: %{component_name}-%{falcon_base_version}.tar.gz
Source1: do-component-build
Source2: install_falcon_standalone.sh
Source3: falcon.sh
Source4: falcon.sh.suse
Source5: falcon.default
Source6: falcon.nofiles.conf
BuildArch: noarch
Requires: /usr/sbin/useradd, /sbin/chkconfig, /sbin/service
Requires: hadoop%{crh_version_as_name}-client

%if  0%{?mgaversion}
Requires: bsh-utils
%else
Requires: sh-utils
%endif


%description 
Falcon is a feed processing and feed management system aimed at making it
easier for end consumers to onboard their feed processing and feed
management on hadoop clusters.

Why?

* Dependencies across various data processing pipelines are not easy to
  establish. Gaps here typically leads to either incorrect/partial
  processing or expensive reprocessing. Repeated duplicate definition of
  a single feed multiple times can lead to inconsistencies / issues.

* Input data may not arrive always on time and it is required to kick off
  the processing without waiting for all data to arrive and accommodate
  late data separately

* Feed management services such as feed retention, replications across
  clusters, archival etc are tasks that are burdensome on individual
  pipeline owners and better offered as a service for all customers.

* It should be easy to onboard new workflows/pipelines

* Smoother integration with metastore/catalog

* Provide notification to end customer based on availability of feed
  groups (logical group of related feeds, which are likely to be used
  together)

%package doc
Summary: Falcon Documentation
Group: Documentation
BuildArch: noarch
Obsoletes: %{name}-docs

%description doc
Documentation for Falcon

%prep
%setup -q -n %{component_name}-%{falcon_base_version}

%build
env FALCON_VERSION=%{version} falcon_jar_version=%{falcon_jar_version} bash %{SOURCE1}

%install
%__rm -rf $RPM_BUILD_ROOT

sed -i -e "s,{CRH_DIR},%{crh_dir}," $RPM_SOURCE_DIR/*

env CRH_DIR=%{crh_dir} CRH_VERSION=%{crh_version_with_bn} FALCON_VERSION=%{falcon_base_version}  sh -x %{SOURCE2} \
        --build-dir=standalone \
        --prefix=$RPM_BUILD_ROOT 
		#--doc-dir=$RPM_BUILD_ROOT/%{doc_falcon}


%__install -d -m 0755 $RPM_BUILD_ROOT/etc/default/
%__install -m 0644 %{SOURCE5} $RPM_BUILD_ROOT/etc/default/%{component_name}

%__install -d  -m 0755  %{buildroot}/%{_localstatedir}/log/%{component_name}
ln -s %{_localstatedir}/log/%{component_name} %{buildroot}/%{logs_falcon}

%__install -d  -m 0755  %{buildroot}/%{_localstatedir}/run/%{component_name}
ln -s %{_localstatedir}/run/%{component_name} %{buildroot}/%{pids_falcon}

%__install -d  -m 0755  %{buildroot}/%{falcon_home}

%__install -d  -m 0755  %{buildroot}/%{falcon_home}/webapp
ln -s ../webapp %{buildroot}/%{webapps_falcon}

%__install -d  -m 0755  %{buildroot}/%{falcon_home}/data

%pre
getent group falcon 2>&1 > /dev/null || /usr/sbin/groupadd -r falcon
getent passwd falcon 2>&1 > /dev/null || /usr/sbin/useradd -c "Falcon" -s /bin/bash -g falcon -G falcon -r -d %{falcon_user_home} falcon 2> /dev/null || :

%post
#%{alternatives_cmd} --install %{etc_falcon_conf} %{component_name}-conf %{etc_falcon_conf_dist} 30
wrapper=%{falcon_home}/bin/falcon
mv %{falcon_home}/bin/falcon %{falcon_home}/bin/falcon.distro
cat > $wrapper <<EOF
#!/bin/bash

# Autodetect JAVA_HOME if not defined
if [ -e /usr/libexec/bigtop-detect-javahome ]; then
  . /usr/libexec/bigtop-detect-javahome
elif [ -e /usr/lib/bigtop-utils/bigtop-detect-javahome ]; then
  . /usr/lib/bigtop-utils/bigtop-detect-javahome
fi
export HADOOP_HOME=%{crh_dir}/hadoop

exec %{falcon_home}/bin/falcon.distro "\$@"
EOF
chmod 755 $wrapper
if [ !  -e "/etc/falcon/conf" ]; then
    rm -f /etc/falcon/conf
    mkdir -p /etc/falcon/conf
    cp -rp /etc/falcon/conf.dist/* /etc/falcon/conf
fi
/usr/bin/%{distroselect} --rpm-mode set falcon-client %{crh_version_with_bn}
/usr/bin/%{distroselect} --rpm-mode set falcon-server %{crh_version_with_bn}

%preun
#rm -rf /usr/bin/falcon
#if [ "$1" = 0 ]; then
        #%{alternatives_cmd} --remove %{name}-conf %{etc_falcon_conf_dist} || :
        
#fi

#######################
#### FILES SECTION ####
#######################

%files 
%defattr(-,falcon,falcon)
%{logs_falcon}
%{pids_falcon}
%dir %{_localstatedir}/log/falcon
%dir %{_localstatedir}/run/falcon
%{falcon_home}/webapp
%{falcon_home}/data

%defattr(-,root,root)
%config(noreplace) /etc/default/%{component_name}
%{webapps_falcon}
#/usr/bin/falcon
%{falcon_home}/client/
%{falcon_home}/oozie/
%{falcon_home}/bin
%{conf_falcon}
%config(noreplace) %{etc_falcon_conf_dist}

%files doc
%defattr(-,root,root)
%doc %{doc_falcon}/
