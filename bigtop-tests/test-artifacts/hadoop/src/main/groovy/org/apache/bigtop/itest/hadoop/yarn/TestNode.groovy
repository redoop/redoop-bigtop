/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.bigtop.itest.hadoop.yarn;

import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;
import org.junit.Test;
import org.apache.bigtop.itest.shell.Shell;

public class TestNode {

  // set debugging variable to true if you want error messages sent to stdout
  private static Shell sh = new Shell("/bin/bash");

  @Test (timeout = 0x15000l)
  public void testNodeBasic() {
    // list
    System.out.println("-list");
    sh.exec("YARN_ROOT_LOGGER=WARN,console yarn node -list");
    assertTrue("-list failed", sh.getRet() == 0);

    // status
    System.out.println("-status");
    String NodeId = sh.getOut().get(2).trim().split()[0];
    sh.exec("yarn node -status " + NodeId);
    assertTrue("-status failed", sh.getRet() == 0);
  }
}
