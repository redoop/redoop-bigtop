#!/bin/bash
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

set -e

# summary of how this script can be called:
#        * <prerm> `remove'
#        * <old-prerm> `upgrade' <new-version>
#        * <new-prerm> `failed-upgrade' <old-version>
#        * <conflictor's-prerm> `remove' `in-favour' <package> <new-version>
#        * <deconfigured's-prerm> `deconfigure' `in-favour'
#          <package-being-installed> <version> `removing'
#          <conflicting-package> <version>
# for details, see http://www.debian.org/doc/debian-policy/ or
# the debian-policy package

APP=@APP@
export ROOT={CRH_DIR}/hue
APP_DIR=$ROOT/apps/$APP
export DESKTOP_LOGLEVEL=WARN
export DESKTOP_LOG_DIR=/var/log/hue
env_python="$ROOT/build/env/bin/python"
app_reg="$ROOT/tools/app_reg/app_reg.py"

case "$1" in
    remove|upgrade|deconfigure)
        if test -e $app_reg -a -e $env_python ; then
	    $env_python $app_reg --remove $APP ||:
        fi
        find $APP_DIR -name \*.py[co] -exec rm -f {} \; ||:
        find $APP_DIR -name \*.egg-info -prune -exec rm -Rf {} \; ||:
        chown -R hue:hue /var/log/hue /var/lib/hue || :
    ;;

    failed-upgrade)
    ;;

    *)
        echo "prerm called with unknown argument \`$1'" >&2
        exit 1
    ;;
esac

# dh_installdeb will replace this with shell code automatically
# generated by other debhelper scripts.

#DEBHELPER#

exit 0
