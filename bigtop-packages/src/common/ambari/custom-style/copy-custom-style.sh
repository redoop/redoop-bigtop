#!/bin/sh
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

if [[ $# -eq 0 ]] ; then
  echo 'Usage: copy-custom-style.sh <stack.distribution>'
  exit 1
fi

stack_style_dir="${DISTRO_DIR}/custom-style/$1"
if [ ! -d $stack_style_dir ];
then
  echo "No stack_style to copy for [ $1 ]"
  exit 0
fi

echo "Copying custom style for [ $1 ]"

if [ -f "$stack_style_dir/ambari-admin/i18n.config.js" ]
then
  echo cp $stack_style_dir/ambari-admin/i18n.config.js ambari-admin/src/main/resources/ui/admin-web/app/scripts/i18n.config.js
  cp $stack_style_dir/ambari-admin/i18n.config.js ambari-admin/src/main/resources/ui/admin-web/app/scripts/i18n.config.js
fi

if [ -f "$stack_style_dir/ambari-web/messages.js" ]
then
  echo cp $stack_style_dir/ambari-web/messages.js ambari-web/app/messages.js
  cp $stack_style_dir/ambari-web/messages.js ambari-web/app/messages.js
fi

if [ -f "$stack_style_dir/ambari-web/login.hbs" ]
then
  echo cp $stack_style_dir/ambari-web/login.hbs ambari-web/app/templates/login.hbs
  cp $stack_style_dir/ambari-web/login.hbs ambari-web/app/templates/login.hbs
fi

if [ -f "$stack_style_dir/ambari-web/index.html" ]
then
  echo cp $stack_style_dir/ambari-web/index.html ambari-web/app/assets/index.html
  cp $stack_style_dir/ambari-web/index.html ambari-web/app/assets/index.html
fi

if [ -d "$stack_style_dir/ambari-web/img" ]
then
  echo cp -rf $stack_style_dir/ambari-web/img ambari-web/app/assets/
  cp -rf $stack_style_dir/ambari-web/img ambari-web/app/assets/
fi