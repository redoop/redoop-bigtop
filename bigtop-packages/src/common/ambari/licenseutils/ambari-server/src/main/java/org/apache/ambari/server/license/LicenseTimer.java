package org.apache.ambari.server.license;

import org.apache.ambari.server.orm.dao.ControllerDAO;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.inject.Singleton;
import java.io.IOException;
import java.util.Timer;
import java.util.TimerTask;


/**
 * Created by xingweidong on 2017/11/17.
 */

@Singleton
public class LicenseTimer {

    public static void timer(final ControllerDAO controllerDAO){
        final HandleLicenseInfo handleLicenseInfo = new HandleLicenseInfoImpl();
        final String stopAmbariServer = "ambari-server stop";
        final Timer timer = new Timer();
        TimerTask timerTask=new TimerTask() {
            @Override
            public void run() {
                try {
                    if (handleLicenseInfo.isExpire()) {
                        try {
                            Runtime.getRuntime().exec(stopAmbariServer).waitFor();
                            timer.cancel();
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    } else {
                        handleLicenseInfo.updateRemainTime(controllerDAO);
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }

            }
        };
        timer.scheduleAtFixedRate(timerTask, 1000 * 60 * 5, 1000 * 60 * 60);
    }
}
