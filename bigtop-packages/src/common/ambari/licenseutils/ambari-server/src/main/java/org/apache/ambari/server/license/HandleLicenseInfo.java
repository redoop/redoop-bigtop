package org.apache.ambari.server.license;

import org.apache.ambari.server.bootstrap.SshHostInfo;
import org.apache.ambari.server.orm.dao.ControllerDAO;
import org.apache.ambari.server.orm.dao.HostDAO;

import java.io.File;
import java.io.IOException;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.util.List;

/**
 * Created by xingweidong on 2017/11/17.
 */
public interface HandleLicenseInfo {

    /**
     * 该文件存储license剩余有效期
     */
    File licenseLocalFile = new File("/etc/.r");

    /**
     * 该文件存储license uuid
     */
    File licenseIdLocalFile = new File("/etc/redoop/licenseid");

    /**
     * 确认license Mac地址有效性
     * @return
     * @throws SocketException
     * @throws UnknownHostException
     */
    Boolean verifyMacAddress() throws SocketException, UnknownHostException;

    /**
     * 获取本地Mac地址
     * @return
     * @throws SocketException
     * @throws UnknownHostException
     */
    String getLocalMacAddress() throws SocketException, UnknownHostException;

    /**
     * 判断有效期
     * @return
     * @throws IOException
     */
    Boolean isExpire() throws IOException;

    /**
     * 更新剩余有效期到文件和数据库
     * @param controllerDAO
     * @throws IOException
     */
    void updateRemainTime(ControllerDAO controllerDAO) throws IOException;

    /**
     * 判断license信息是否未注入过
     * @param controllerDAO
     * @return
     */
    Boolean isNewLicense(ControllerDAO controllerDAO);

    /**
     * 初始化当前license，将剩余有效期加密存入文件，将license信息录入数据库，一个唯一license只初始化一次
     * @param controllerDAO
     * @throws IOException
     */
    void initCurrentLicense(ControllerDAO controllerDAO) throws IOException;

    /**
     * 获取有效主机列表
     * @param hostDAO
     * @param info
     * @return
     */
    List<String> getvalidHostsList(HostDAO hostDAO, SshHostInfo info);
}
