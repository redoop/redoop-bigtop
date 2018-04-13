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
#
# Hadoop RPM spec file
#

# FIXME: we need to disable a more strict checks on native files for now,
# since Hadoop build system makes it difficult to pass the kind of flags
# that would make newer RPM debuginfo generation scripts happy.
%undefine _missing_build_ids_terminate_build
%define crh_dir /usr/%{crh_tag}/%{crh_version_with_bn}
%define distroselect crh-select
%define hadoop_name hadoop
%define etc_hadoop /etc/%{hadoop_name}
%define etc_yarn /etc/yarn
%define config_hadoop %{etc_hadoop}/conf
%define config_yarn %{etc_yarn}/conf
%define lib_hadoop_dirname %{crh_dir}
%define lib_hadoop %{lib_hadoop_dirname}/%{hadoop_name}
%define lib_hdfs %{lib_hadoop_dirname}/%{hadoop_name}-hdfs
%define lib_yarn %{lib_hadoop_dirname}/%{hadoop_name}-yarn
%define lib_mapreduce %{lib_hadoop_dirname}/%{hadoop_name}-mapreduce
%define log_hadoop_dirname /var/log
%define log_hadoop %{log_hadoop_dirname}/%{hadoop_name}
%define log_yarn %{log_hadoop_dirname}/%{hadoop_name}-yarn
%define log_hdfs %{log_hadoop_dirname}/%{hadoop_name}-hdfs
%define log_mapreduce %{log_hadoop_dirname}/%{hadoop_name}-mapreduce
%define run_hadoop_dirname /var/run
%define run_hadoop %{run_hadoop_dirname}/hadoop
%define run_yarn %{run_hadoop_dirname}/%{hadoop_name}-yarn
%define run_hdfs %{run_hadoop_dirname}/%{hadoop_name}-hdfs
%define run_mapreduce %{run_hadoop_dirname}/%{hadoop_name}-mapreduce
%define state_hadoop_dirname /var/lib
%define state_hadoop %{state_hadoop_dirname}/hadoop
%define state_yarn %{state_hadoop_dirname}/%{hadoop_name}-yarn
%define state_hdfs %{state_hadoop_dirname}/%{hadoop_name}-hdfs
%define state_mapreduce %{state_hadoop_dirname}/%{hadoop_name}-mapreduce
%define bin_hadoop %{_bindir}
%define man_hadoop %{_mandir}
%define doc_hadoop %{_docdir}/%{hadoop_name}-%{hadoop_version}
%define mapreduce_services mapreduce-historyserver
%define hdfs_services hdfs-namenode hdfs-secondarynamenode hdfs-datanode hdfs-zkfc hdfs-journalnode
%define yarn_services yarn-resourcemanager yarn-nodemanager yarn-proxyserver yarn-timelineserver
%define hadoop_services %{hdfs_services} %{mapreduce_services} %{yarn_services}
# Hadoop outputs built binaries into %{hadoop_build}
%define hadoop_build_path build
%define static_images_dir src/webapps/static/images
%define libexecdir /usr/lib

%ifarch i386
%global hadoop_arch Linux-i386-32
%endif
%ifarch amd64 x86_64
%global hadoop_arch Linux-amd64-64
%endif

# CentOS 5 does not have any dist macro
# So I will suppose anything that is not Mageia or a SUSE will be a RHEL/CentOS/Fedora
%if %{!?suse_version:1}0 && %{!?mgaversion:1}0

# FIXME: brp-repack-jars uses unzip to expand jar files
# Unfortunately aspectjtools-1.6.5.jar pulled by ivy contains some files and directories without any read permission
# and make whole process to fail.
# So for now brp-repack-jars is being deactivated until this is fixed.
# See BIGTOP-294
%define __os_install_post \
    %{_rpmconfigdir}/brp-compress ; \
    %{_rpmconfigdir}/brp-strip-static-archive %{__strip} ; \
    %{_rpmconfigdir}/brp-strip-comment-note %{__strip} %{__objdump} ; \
    /usr/lib/rpm/brp-python-bytecompile ; \
    %{nil}

%define netcat_package nc
%define doc_hadoop %{_docdir}/%{hadoop_name}-%{hadoop_version}
%define alternatives_cmd alternatives
%global initd_dir %{_sysconfdir}/rc.d/init.d
%endif


%if  %{?suse_version:1}0

# Only tested on openSUSE 11.4. le'ts update it for previous release when confirmed
%if 0%{suse_version} > 1130
%define suse_check \# Define an empty suse_check for compatibility with older sles
%endif

# Deactivating symlinks checks
%define __os_install_post \
    %{suse_check} ; \
    /usr/lib/rpm/brp-compress ; \
    %{nil}

%define netcat_package netcat-openbsd
%define doc_hadoop %{_docdir}/%{hadoop_name}
%define alternatives_cmd update-alternatives
%global initd_dir %{_sysconfdir}/rc.d
%endif

%if  0%{?mgaversion}
%define netcat_package netcat-openbsd
%define doc_hadoop %{_docdir}/%{hadoop_name}-%{hadoop_version}
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

Name: %{hadoop_name}%{crh_version_as_name}
Version: %{hadoop_version}
Release: %{hadoop_release}
Summary: Hadoop is a software platform for processing vast amounts of data
License: ASL 2.0
URL: http://hadoop.apache.org/core/
Group: Development/Libraries
Source0: %{hadoop_name}-%{hadoop_base_version}.tar.gz
Source1: do-component-build
Source2: install_%{hadoop_name}.sh
Source3: hadoop.default
Source4: hadoop-fuse.default
Source5: httpfs.default
Source6: hadoop.1
Source7: hadoop-fuse-dfs.1
Source8: hdfs.conf
Source9: yarn.conf
Source10: mapreduce.conf
Source11: init.d.tmpl
Source12: hadoop-hdfs-namenode.svc
Source13: hadoop-hdfs-datanode.svc
Source14: hadoop-hdfs-secondarynamenode.svc
Source15: hadoop-mapreduce-historyserver.svc
Source16: hadoop-yarn-resourcemanager.svc
Source17: hadoop-yarn-nodemanager.svc
Source18: hadoop-httpfs.svc
Source19: mapreduce.default
Source20: hdfs.default
Source21: yarn.default
Source22: hadoop-layout.sh
Source23: hadoop-hdfs-zkfc.svc
Source24: hadoop-hdfs-journalnode.svc
Source25: httpfs-tomcat-deployment.sh
Source26: yarn.1
Source27: hdfs.1
Source28: mapred.1
Source29: hadoop-yarn-timelineserver.svc
#BIGTOP_PATCH_FILES
Buildroot: %{_tmppath}/%{hadoop_name}-%{version}-%{release}-root-%(%{__id} -u -n)
BuildRequires: fuse-devel, fuse
Requires: coreutils, /usr/sbin/useradd, /usr/sbin/usermod, /sbin/chkconfig, /sbin/service, bigtop-utils >= 0.7, zookeeper%{crh_version_as_name} >= 3.4.0
Requires: psmisc, %{netcat_package}
Requires: spark%{crh_version_as_name}-yarn-shuffle, ranger%{crh_version_as_name}-hdfs-plugin, ranger%{crh_version_as_name}-yarn-plugin
# Sadly, Sun/Oracle JDK in RPM form doesn't provide libjvm.so, which means we have
# to set AutoReq to no in order to minimize confusion. Not ideal, but seems to work.
# I wish there was a way to disable just one auto dependency (libjvm.so)
AutoReq: no

%if  %{?suse_version:1}0
BuildRequires: pkg-config, libfuse2, libopenssl-devel, gcc-c++
# Required for init scripts
Requires: sh-utils, insserv
%endif

# CentOS 5 does not have any dist macro
# So I will suppose anything that is not Mageia or a SUSE will be a RHEL/CentOS/Fedora
%if %{!?suse_version:1}0 && %{!?mgaversion:1}0
BuildRequires: pkgconfig, fuse-libs, redhat-rpm-config, lzo-devel, openssl-devel
# Required for init scripts
Requires: sh-utils, /lib/lsb/init-functions
%endif

%if  0%{?mgaversion}
BuildRequires: pkgconfig, libfuse-devel, libfuse2 , libopenssl-devel, gcc-c++, liblzo-devel, zlib-devel
Requires: chkconfig, xinetd-simple-services, zlib, initscripts
%endif


%description
Hadoop is a software platform that lets one easily write and
run applications that process vast amounts of data.

Here's what makes Hadoop especially useful:
* Scalable: Hadoop can reliably store and process petabytes.
* Economical: It distributes the data and processing across clusters
              of commonly available computers. These clusters can number
              into the thousands of nodes.
* Efficient: By distributing the data, Hadoop can process it in parallel
             on the nodes where the data is located. This makes it
             extremely rapid.
* Reliable: Hadoop automatically maintains multiple copies of data and
            automatically redeploys computing tasks based on failures.

Hadoop implements MapReduce, using the Hadoop Distributed File System (HDFS).
MapReduce divides applications into many small blocks of work. HDFS creates
multiple replicas of data blocks for reliability, placing them on compute
nodes around the cluster. MapReduce can then process the data where it is
located.

%package hdfs
Summary: The Hadoop Distributed File System
Group: System/Daemons
Requires: %{name} = %{version}-%{release}, bigtop-groovy, bigtop-jsvc

%description hdfs
Hadoop Distributed File System (HDFS) is the primary storage system used by
Hadoop applications. HDFS creates multiple replicas of data blocks and distributes
them on compute nodes throughout a cluster to enable reliable, extremely rapid
computations.

%package yarn
Summary: The Hadoop NextGen MapReduce (YARN)
Group: System/Daemons
Requires: %{name} = %{version}-%{release}

%description yarn
YARN (Hadoop NextGen MapReduce) is a general purpose data-computation framework.
The fundamental idea of YARN is to split up the two major functionalities of the
JobTracker, resource management and job scheduling/monitoring, into separate daemons:
ResourceManager and NodeManager.

The ResourceManager is the ultimate authority that arbitrates resources among all
the applications in the system. The NodeManager is a per-node slave managing allocation
of computational resources on a single node. Both work in support of per-application
ApplicationMaster (AM).

An ApplicationMaster is, in effect, a framework specific library and is tasked with
negotiating resources from the ResourceManager and working with the NodeManager(s) to
execute and monitor the tasks.


%package mapreduce
Summary: The Hadoop MapReduce (MRv2)
Group: System/Daemons
Requires: %{name}-yarn = %{version}-%{release}

%description mapreduce
Hadoop MapReduce is a programming model and software framework for writing applications
that rapidly process vast amounts of data in parallel on large clusters of compute nodes.


%package hdfs-namenode
Summary: The Hadoop namenode manages the block locations of HDFS files
Group: System/Daemons
Requires: %{name}-hdfs = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}
Requires(pre): %{name}-hdfs = %{version}-%{release}

%description hdfs-namenode
The Hadoop Distributed Filesystem (HDFS) requires one unique server, the
namenode, which manages the block locations of files on the filesystem.


%package hdfs-secondarynamenode
Summary: Hadoop Secondary namenode
Group: System/Daemons
Requires: %{name}-hdfs = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}
Requires(pre): %{name}-hdfs = %{version}-%{release}

%description hdfs-secondarynamenode
The Secondary Name Node periodically compacts the Name Node EditLog
into a checkpoint.  This compaction ensures that Name Node restarts
do not incur unnecessary downtime.

%package hdfs-zkfc
Summary: Hadoop HDFS failover controller
Group: System/Daemons
Requires: %{name}-hdfs = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}
Requires(pre): %{name}-hdfs = %{version}-%{release}

%description hdfs-zkfc
The Hadoop HDFS failover controller is a ZooKeeper client which also
monitors and manages the state of the NameNode. Each of the machines
which runs a NameNode also runs a ZKFC, and that ZKFC is responsible
for: Health monitoring, ZooKeeper session management, ZooKeeper-based
election.

%package hdfs-journalnode
Summary: Hadoop HDFS JournalNode
Group: System/Daemons
Requires: %{name}-hdfs = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}

%description hdfs-journalnode
The HDFS JournalNode is responsible for persisting NameNode edit logs.
In a typical deployment the JournalNode daemon runs on at least three
separate machines in the cluster.

%package hdfs-datanode
Summary: Hadoop Data Node
Group: System/Daemons
Requires: %{name}-hdfs = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}
Requires(pre): %{name}-hdfs = %{version}-%{release}

%description hdfs-datanode
The Data Nodes in the Hadoop Cluster are responsible for serving up
blocks of data over the network to Hadoop Distributed Filesystem
(HDFS) clients.

%package yarn-resourcemanager
Summary: YARN Resource Manager
Group: System/Daemons
Requires: %{name}-yarn = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}
Requires(pre): %{name}-yarn = %{version}-%{release}

%description yarn-resourcemanager
The resource manager manages the global assignment of compute resources to applications

%package yarn-nodemanager
Summary: YARN Node Manager
Group: System/Daemons
Requires: %{name}-yarn = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}
Requires(pre): %{name}-yarn = %{version}-%{release}

%description yarn-nodemanager
The NodeManager is the per-machine framework agent who is responsible for
containers, monitoring their resource usage (cpu, memory, disk, network) and
reporting the same to the ResourceManager/Scheduler.

%package yarn-proxyserver
Summary: YARN Web Proxy
Group: System/Daemons
Requires: %{name}-yarn = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}
Requires(pre): %{name}-yarn = %{version}-%{release}

%description yarn-proxyserver
The web proxy server sits in front of the YARN application master web UI.

%package yarn-timelineserver
Summary: YARN Timeline Server
Group: System/Daemons
Requires: %{name}-yarn = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}
Requires(pre): %{name}-yarn = %{version}-%{release}

%description yarn-timelineserver
Storage and retrieval of applications' current as well as historic information in a generic fashion is solved in YARN through the Timeline Server.

%package mapreduce-historyserver
Summary: MapReduce History Server
Group: System/Daemons
Requires: %{name}-mapreduce = %{version}-%{release}
Requires: %{name}-hdfs = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}
Requires(pre): %{name}-mapreduce = %{version}-%{release}

%description mapreduce-historyserver
The History server keeps records of the different activities being performed on a Apache Hadoop cluster

%package client
Summary: Hadoop client side dependencies
Group: System/Daemons
Requires: %{name} = %{version}-%{release}
Requires: %{name}-hdfs = %{version}-%{release}
Requires: %{name}-yarn = %{version}-%{release}
Requires: %{name}-mapreduce = %{version}-%{release}

%description client
Installation of this package will provide you with all the dependencies for Hadoop clients.

%package conf-pseudo
Summary: Pseudo-distributed Hadoop configuration
Group: System/Daemons
Requires: %{name} = %{version}-%{release}
Requires: %{name}-hdfs-namenode = %{version}-%{release}
Requires: %{name}-hdfs-datanode = %{version}-%{release}
Requires: %{name}-hdfs-secondarynamenode = %{version}-%{release}
Requires: %{name}-yarn-resourcemanager = %{version}-%{release}
Requires: %{name}-yarn-nodemanager = %{version}-%{release}
Requires: %{name}-mapreduce-historyserver = %{version}-%{release}

%description conf-pseudo
Contains configuration files for a "pseudo-distributed" Hadoop deployment.
In this mode, each of the hadoop components runs as a separate Java process,
but all on the same machine.

%package doc
Summary: Hadoop Documentation
Group: Documentation
%description doc
Documentation for Hadoop

%package libhdfs
Summary: Hadoop Filesystem Library
Group: Development/Libraries
Requires: %{name}-hdfs = %{version}-%{release}
# TODO: reconcile libjvm
AutoReq: no

%description libhdfs
Hadoop Filesystem Library

%package libhdfs-devel
Summary: Development support for libhdfs
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}, %{name}-libhdfs = %{version}-%{release}

%description libhdfs-devel
Includes examples and header files for accessing HDFS from C

%package hdfs-fuse
Summary: Mountable HDFS
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libhdfs = %{version}-%{release}
Requires: %{name}-client = %{version}-%{release}
Requires: fuse
AutoReq: no

%if %{?suse_version:1}0
Requires: libfuse2
%else
Requires: fuse-libs
%endif


%description hdfs-fuse
These projects (enumerated below) allow HDFS to be mounted (on most flavors of Unix) as a standard file system using


%prep
%setup -n %{hadoop_name}-%{hadoop_base_version}-src

#BIGTOP_PATCH_COMMANDS
%build
# This assumes that you installed Java JDK 6 and set JAVA_HOME
# This assumes that you installed Forrest and set FORREST_HOME

env HADOOP_VERSION=%{hadoop_base_version} HADOOP_ARCH=%{hadoop_arch} bash %{SOURCE1}

%clean
%__rm -rf $RPM_BUILD_ROOT

#########################
#### INSTALL SECTION ####
#########################
%install
%__rm -rf $RPM_BUILD_ROOT


%__install -d -m 0755 $RPM_BUILD_ROOT/%{lib_hadoop}

env HADOOP_VERSION=%{hadoop_base_version} CRH_DIR=%{crh_dir} CRH_VERSION=%{crh_version_with_bn}  bash %{SOURCE2} \
  --distro-dir=$RPM_SOURCE_DIR \
  --build-dir=$PWD/build \
  --system-include-dir=$RPM_BUILD_ROOT%{_includedir} \
  --system-lib-dir=$RPM_BUILD_ROOT%{_libdir} \
  --system-libexec-dir=$RPM_BUILD_ROOT/%{lib_hadoop}/libexec \
  --hadoop-etc-dir=$RPM_BUILD_ROOT%{etc_hadoop} \
  --prefix=$RPM_BUILD_ROOT \
  --doc-dir=$RPM_BUILD_ROOT%{doc_hadoop} \
  --example-dir=$RPM_BUILD_ROOT%{doc_hadoop}/examples \
  --native-build-string=%{hadoop_arch} \
  --installed-lib-dir=%{lib_hadoop} \
  --man-dir=$RPM_BUILD_ROOT%{man_hadoop} \

# Forcing Zookeeper dependency to be on the packaged jar
%__ln_s -f %{crh_dir}/zookeeper/zookeeper.jar $RPM_BUILD_ROOT/%{lib_hadoop}/lib/zookeeper*.jar
# Workaround for BIGTOP-583
%__rm -f $RPM_BUILD_ROOT/%{lib_hadoop}-*/lib/slf4j-log4j12-*.jar

# Init.d scripts
%__install -d -m 0755 $RPM_BUILD_ROOT/%{initd_dir}/

# Install top level /etc/default files
%__install -d -m 0755 $RPM_BUILD_ROOT/etc/default
%__cp $RPM_SOURCE_DIR/hadoop.default $RPM_BUILD_ROOT/etc/default/hadoop
# FIXME: BIGTOP-463
echo 'export JSVC_HOME=%{libexecdir}/bigtop-utils' >> $RPM_BUILD_ROOT/etc/default/hadoop
%__cp $RPM_SOURCE_DIR/%{hadoop_name}-fuse.default $RPM_BUILD_ROOT/etc/default/%{hadoop_name}-fuse

# Generate the init.d scripts
for service in %{hadoop_services}
do
       bash %{SOURCE11} $RPM_SOURCE_DIR/%{hadoop_name}-${service}.svc rpm $RPM_BUILD_ROOT/%{initd_dir}/%{hadoop_name}-${service}
       cp $RPM_SOURCE_DIR/${service/-*/}.default $RPM_BUILD_ROOT/etc/default/%{hadoop_name}-${service}
       chmod 644 $RPM_BUILD_ROOT/etc/default/%{hadoop_name}-${service}
done

# Install security limits
%__install -d -m 0755 $RPM_BUILD_ROOT/etc/security/limits.d
%__install -m 0644 %{SOURCE8} $RPM_BUILD_ROOT/etc/security/limits.d/hdfs.conf
%__install -m 0644 %{SOURCE9} $RPM_BUILD_ROOT/etc/security/limits.d/yarn.conf
%__install -m 0644 %{SOURCE10} $RPM_BUILD_ROOT/etc/security/limits.d/mapreduce.conf

# Install fuse default file
%__install -d -m 0755 $RPM_BUILD_ROOT/etc/default
%__cp %{SOURCE4} $RPM_BUILD_ROOT/etc/default/hadoop-fuse

# /var/lib/*/cache
%__install -d -m 1777 $RPM_BUILD_ROOT/%{state_yarn}/cache
%__install -d -m 1777 $RPM_BUILD_ROOT/%{state_hdfs}/cache
%__install -d -m 1777 $RPM_BUILD_ROOT/%{state_mapreduce}/cache
# /var/log/*
%__install -d -m 0755 $RPM_BUILD_ROOT/%{log_yarn}
%__install -d -m 0755 $RPM_BUILD_ROOT/%{log_hdfs}
%__install -d -m 0755 $RPM_BUILD_ROOT/%{log_mapreduce}
# /var/run/*
%__install -d -m 0755 $RPM_BUILD_ROOT/%{run_yarn}
%__install -d -m 0755 $RPM_BUILD_ROOT/%{run_hdfs}
%__install -d -m 0755 $RPM_BUILD_ROOT/%{run_mapreduce}

%pre
getent group hadoop >/dev/null || groupadd -r hadoop

%pre hdfs
getent group hdfs >/dev/null   || groupadd -r hdfs
getent passwd hdfs >/dev/null || /usr/sbin/useradd --comment "Hadoop HDFS" --shell /bin/bash -M -r -g hdfs -G hadoop --home %{state_hdfs} hdfs

%pre yarn
getent group yarn >/dev/null   || groupadd -r yarn
getent passwd yarn >/dev/null || /usr/sbin/useradd --comment "Hadoop Yarn" --shell /bin/bash -M -r -g yarn -G hadoop --home %{state_yarn} yarn

%pre mapreduce
getent group mapred >/dev/null   || groupadd -r mapred
getent passwd mapred >/dev/null || /usr/sbin/useradd --comment "Hadoop MapReduce" --shell /bin/bash -M -r -g mapred -G hadoop --home %{state_mapreduce} mapred

%post

if [ !  -e "/etc/hadoop/conf" ]; then
     rm -f /etc/hadoop/conf
     mkdir -p /etc/hadoop/conf
     cp -rp /etc/hadoop/conf.empty/* /etc/hadoop/conf 
fi 
#ln -s /etc/hadoop/conf %{crh_dir}/%{hadoop-name}/conf 

# upgrade
/usr/bin/%{distroselect} --rpm-mode set hadoop-client %{crh_version_with_bn}
/usr/bin/%{distroselect} --rpm-mode set hadoop-hdfs-datanode %{crh_version_with_bn}
/usr/bin/%{distroselect} --rpm-mode set hadoop-hdfs-journalnode %{crh_version_with_bn}
/usr/bin/%{distroselect} --rpm-mode set hadoop-hdfs-nfs3 %{crh_version_with_bn}
/usr/bin/%{distroselect} --rpm-mode set hadoop-hdfs-namenode %{crh_version_with_bn}
/usr/bin/%{distroselect} --rpm-mode set hadoop-hdfs-portmap %{crh_version_with_bn}
/usr/bin/%{distroselect} --rpm-mode set hadoop-hdfs-secondarynamenode %{crh_version_with_bn}
/usr/bin/%{distroselect} --rpm-mode set hadoop-mapreduce-historyserver %{crh_version_with_bn}
/usr/bin/%{distroselect} --rpm-mode set hadoop-yarn-resourcemanager %{crh_version_with_bn}
/usr/bin/%{distroselect} --rpm-mode set hadoop-yarn-nodemanager %{crh_version_with_bn}
/usr/bin/%{distroselect} --rpm-mode set hadoop-yarn-timelineserver %{crh_version_with_bn}

%{alternatives_cmd} --install %{config_hadoop} %{hadoop_name}-conf %{etc_hadoop}/conf.empty 10


%preun
if [ "$1" = 0 ]; then
  %{alternatives_cmd} --remove %{hadoop_name}-conf %{etc_hadoop}/conf.empty || :
fi


%files yarn
%defattr(-,root,root)
%config(noreplace) %{etc_hadoop}/conf.empty/yarn-env.sh
%config(noreplace) %{etc_hadoop}/conf.empty/yarn-site.xml
%config(noreplace) %{etc_hadoop}/conf.empty/capacity-scheduler.xml
%config(noreplace) %{etc_hadoop}/conf.empty/container-executor.cfg
%config(noreplace) /etc/security/limits.d/yarn.conf
%{lib_hadoop}/libexec/yarn-config.sh
%{lib_yarn}
%attr(4754,root,yarn) %{lib_yarn}/bin/container-executor
%{bin_hadoop}/yarn
%attr(0775,yarn,hadoop) %{run_yarn}
%attr(0775,yarn,hadoop) %{log_yarn}
%attr(0755,yarn,hadoop) %{state_yarn}
%attr(1777,yarn,hadoop) %{state_yarn}/cache

%files hdfs
%defattr(-,root,root)
%config(noreplace) %{etc_hadoop}/conf.empty/hdfs-site.xml
%config(noreplace) %{etc_hadoop}/conf.empty/httpfs-env.sh
%config(noreplace) %{etc_hadoop}/conf.empty/httpfs-log4j.properties
%config(noreplace) %{etc_hadoop}/conf.empty/httpfs-signature.secret
%config(noreplace) %{etc_hadoop}/conf.empty/httpfs-site.xml
%config(noreplace) /etc/security/limits.d/hdfs.conf
%{lib_hdfs}
%{lib_hadoop}/libexec/hdfs-config.sh
%{bin_hadoop}/hdfs
%attr(0775,hdfs,hadoop) %{run_hdfs}
%attr(0775,hdfs,hadoop) %{log_hdfs}
%attr(0755,hdfs,hadoop) %{state_hdfs}
%attr(1777,hdfs,hadoop) %{state_hdfs}/cache
%{lib_hadoop}/libexec/init-hdfs.sh
%{lib_hadoop}/libexec/init-hcfs.json
%{lib_hadoop}/libexec/init-hcfs.groovy

%files mapreduce
%defattr(-,root,root)
%config(noreplace) %{etc_hadoop}/conf.empty/mapred-site.xml
%config(noreplace) %{etc_hadoop}/conf.empty/mapred-env.sh
%config(noreplace) %{etc_hadoop}/conf.empty/mapred-queues.xml.template
%config(noreplace) %{etc_hadoop}/conf.empty/mapred-site.xml
%config(noreplace) /etc/security/limits.d/mapreduce.conf
%{lib_mapreduce}
%{lib_hadoop}/libexec/mapred-config.sh
%{bin_hadoop}/mapred
%attr(0775,mapred,hadoop) %{run_mapreduce}
%attr(0775,mapred,hadoop) %{log_mapreduce}
%attr(0775,mapred,hadoop) %{state_mapreduce}
%attr(1777,mapred,hadoop) %{state_mapreduce}/cache


%files
%defattr(-,root,root)
%config(noreplace) %{etc_hadoop}/conf.empty/core-site.xml
%config(noreplace) %{etc_hadoop}/conf.empty/hadoop-metrics2.properties
%config(noreplace) %{etc_hadoop}/conf.empty/log4j.properties
%config(noreplace) %{etc_hadoop}/conf.empty/workers
%config(noreplace) %{etc_hadoop}/conf.empty/ssl-client.xml.example
%config(noreplace) %{etc_hadoop}/conf.empty/ssl-server.xml.example
%config(noreplace) %{etc_hadoop}/conf.empty/configuration.xsl
%config(noreplace) %{etc_hadoop}/conf.empty/hadoop-env.sh
%config(noreplace) %{etc_hadoop}/conf.empty/hadoop-policy.xml
%config(noreplace) %{etc_hadoop}/conf.empty/hadoop-user-functions.sh.example
%config(noreplace) %{etc_hadoop}/conf.empty/user_ec_policies.xml.template
%config(noreplace) %{etc_hadoop}/conf.empty/kms-acls.xml
%config(noreplace) %{etc_hadoop}/conf.empty/kms-env.sh
%config(noreplace) %{etc_hadoop}/conf.empty/kms-log4j.properties
%config(noreplace) %{etc_hadoop}/conf.empty/kms-site.xml
%{etc_hadoop}/conf.empty/shellprofile.d
%config(noreplace) /etc/default/hadoop
/etc/bash_completion.d/hadoop
%{crh_dir}/%{hadoop_name}/mapreduce.tar.gz
%{lib_hadoop}/*.jar
%{lib_hadoop}/lib
%{lib_hadoop}/sbin
%{lib_hadoop}/bin
%{lib_hadoop}/etc
%{lib_hadoop}/conf
%{lib_hadoop}/libexec/hadoop-config.sh
%{lib_hadoop}/libexec/hadoop-functions.sh
%{lib_hadoop}/libexec/hadoop-layout.sh
%{lib_hadoop}/libexec/shellprofile.d
%{lib_hadoop}/libexec/tools
%{bin_hadoop}/hadoop
%{man_hadoop}/man1/hadoop.1.*
%{man_hadoop}/man1/yarn.1.*
%{man_hadoop}/man1/hdfs.1.*
%{man_hadoop}/man1/mapred.1.*

# Shouldn't the following be moved to hadoop-hdfs?
%exclude %{lib_hadoop}/bin/fuse_dfs

%files doc
%defattr(-,root,root)
%doc %{doc_hadoop}

# Service file management RPMs
%define service_macro() \
%files %1 \
%defattr(-,root,root) \
%{initd_dir}/%{hadoop_name}-%1 \
%config(noreplace) /etc/default/%{hadoop_name}-%1 \
%post %1 \
chkconfig --add %{hadoop_name}-%1 \
\
%preun %1 \
if [ $1 = 0 ]; then \
  service %{hadoop_name}-%1 stop > /dev/null 2>&1 \
  chkconfig --del %{hadoop_name}-%1 \
fi \
%postun %1 \
if [ $1 -ge 1 ]; then \
  service %{hadoop_name}-%1 condrestart >/dev/null 2>&1 \
fi

%service_macro hdfs-namenode
%service_macro hdfs-secondarynamenode
%service_macro hdfs-zkfc
%service_macro hdfs-journalnode
%service_macro hdfs-datanode
%service_macro yarn-resourcemanager
%service_macro yarn-nodemanager
%service_macro yarn-proxyserver
%service_macro yarn-timelineserver
%service_macro mapreduce-historyserver

# Pseudo-distributed Hadoop installation
%post conf-pseudo
%{alternatives_cmd} --install %{config_hadoop} %{hadoop_name}-conf %{etc_hadoop}/conf.pseudo 30

%preun conf-pseudo
if [ "$1" = 0 ]; then
        %{alternatives_cmd} --remove %{hadoop_name}-conf %{etc_hadoop}/conf.pseudo
fi

%files conf-pseudo
%defattr(-,root,root)
%config(noreplace) %attr(755,root,root) %{etc_hadoop}/conf.pseudo

%files client
%defattr(-,root,root)
%{lib_hadoop}/client

%files libhdfs
%defattr(-,root,root)
%{_libdir}/libhdfs*

%files libhdfs-devel
%{_includedir}/hdfs.h
#%doc %{_docdir}/libhdfs-%{hadoop_version}

%files hdfs-fuse
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) /etc/default/hadoop-fuse
%attr(0755,root,root) %{lib_hadoop}/bin/fuse_dfs
%attr(0755,root,root) %{bin_hadoop}/hadoop-fuse-dfs


