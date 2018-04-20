package org.apache.ambari.server.license;

import java.io.*;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.List;

import org.apache.ambari.server.bootstrap.SshHostInfo;
import org.apache.ambari.server.license.utils.Base64;
import org.apache.ambari.server.orm.dao.ControllerDAO;
import org.apache.ambari.server.orm.dao.HostDAO;
import org.apache.ambari.server.orm.entities.ControllerEntity;
import org.apache.ambari.server.orm.entities.HostEntity;

/**
 * Created by xingweidong on 2017/11/17.
 */
public class HandleLicenseInfoImpl implements HandleLicenseInfo {

    @Override
    public Boolean verifyMacAddress() throws SocketException, UnknownHostException {
        if (LicenseInfo.getInstance().getMacAddress().equals(getLocalMacAddress())) {
            return true;
        } else {
            return false;
        }
    }

    @Override
    public String getLocalMacAddress() throws SocketException, UnknownHostException {
        InetAddress inetAddress = InetAddress.getLocalHost();
        //获取网卡，获取地址
        byte[] mac = NetworkInterface.getByInetAddress(inetAddress).getHardwareAddress();
        StringBuffer stringBuffer = new StringBuffer("");
        for(int i=0; i<mac.length; i++) {
            if(i!=0) {
                stringBuffer.append("-");
            }
            //字节转换为整数
            int temp = mac[i]&0xff;
            String str = Integer.toHexString(temp);
            if(str.length()==1) {
                stringBuffer.append("0"+str);
            }else {
                stringBuffer.append(str);
            }
        }
        return stringBuffer.toString();
    }

    @Override
    public Boolean isExpire() throws IOException {
        FileReader fileReader = new FileReader(licenseLocalFile);
        BufferedReader bufferedReader = new BufferedReader(fileReader);
        int remainValidTime = Integer.valueOf(new String(Base64.decode(bufferedReader.readLine())));

        if (remainValidTime > 0) {
            return false;
        } else {
            return true;
        }
    }

    @Override
    public void updateRemainTime(ControllerDAO controllerDAO) throws IOException {
        // 更新有效期
        FileReader fileReader = new FileReader(licenseLocalFile);
        BufferedReader bufferedReader = new BufferedReader(fileReader);
        String strs = new String(Base64.decode(bufferedReader.readLine()));
        int remainValidTime = Integer.valueOf(strs);
        remainValidTime--;
        int remainValidDay = remainValidTime/24;
        FileWriter fileWriter = new FileWriter(licenseLocalFile);
        BufferedWriter bufferedWriter = new BufferedWriter(fileWriter);
        bufferedWriter.write(Base64.encode((String.valueOf(remainValidTime)).getBytes()));
        bufferedWriter.close();
        fileWriter.close();

        // 更新有效期到数据库
        ControllerEntity controllerEntity = controllerDAO.findById(LicenseInfo.getInstance().getLicenseId());
        controllerEntity.setRemainTime(String.valueOf(remainValidDay));
        controllerDAO.merge(controllerEntity);
    }

    @Override
    public Boolean isNewLicense(ControllerDAO controllerDAO) {
        if (controllerDAO.findById(LicenseInfo.getInstance().getLicenseId()) == null) {
            return true;
        } else {
            return false;
        }
    }

    @Override
    public void initCurrentLicense(ControllerDAO controllerDAO) throws IOException {
        // 将license uuid信息写到本地文件
        // 不存在则创建
        if (!licenseIdLocalFile.getParentFile().exists()) {
            licenseIdLocalFile.getParentFile().mkdirs();
        } else {
            if (!licenseIdLocalFile.exists()) {
                licenseIdLocalFile.createNewFile();
            }
        }
        // 添加license uuid
        FileWriter fw = new FileWriter(licenseIdLocalFile,true);
        BufferedWriter bw = new BufferedWriter(fw);
        bw.write((LicenseInfo.getInstance().getLicenseId()));
        bw.newLine();
        bw.close();
        fw.close();


        // 将license有效期信息写到本地文件
        // 不存在则创建
        if (!licenseLocalFile.getParentFile().exists()) {
            licenseLocalFile.getParentFile().mkdirs();
        } else {
            if (!licenseLocalFile.exists()) {
                licenseLocalFile.createNewFile();
            }
        }

        // 初始化剩余有效期
        FileWriter fileWriter = new FileWriter(licenseLocalFile);
        BufferedWriter bufferedWriter = new BufferedWriter(fileWriter);
        bufferedWriter.write(Base64.encode((LicenseInfo.getInstance().getVaildTime()).getBytes()));
        bufferedWriter.close();
        fileWriter.close();

        // 将有效期小时数转换为天数
        int remainValidTime = Integer.valueOf(LicenseInfo.getInstance().getVaildTime());
        int remainValidDay = remainValidTime/24;
        // 将license信息初始化到数据库
        ControllerEntity newcontrollerEntity = new ControllerEntity();
        // 创建实体数据
        newcontrollerEntity.setControllerId(LicenseInfo.getInstance().getLicenseId());
        newcontrollerEntity.setMacAddress(LicenseInfo.getInstance().getMacAddress());
        newcontrollerEntity.setPermissionHosts(LicenseInfo.getInstance().getPermissionHosts());
        newcontrollerEntity.setVaildTime(String.valueOf(remainValidDay));
        newcontrollerEntity.setRegDate(LicenseInfo.getInstance().getRegDate());
        newcontrollerEntity.setRemainTime(String.valueOf(remainValidDay));
        // 插入数据库
        controllerDAO.create(newcontrollerEntity);
    }

    @Override
    public List<String> getvalidHostsList(HostDAO hostDAO, SshHostInfo info) {
        /**
         * 从 license文件中获取到授权节点数permissionNodes
         * 从 hosts 表获取已注册主机数目currentNodes
         * 计算剩余可安装节点数remianNodes
         * 最多注册当前主机列表中前remainNodes个主机，其余主机则显示注册失败
         */
        int permissionHosts = Integer.valueOf(LicenseInfo.getInstance().getPermissionHosts());     //从license文件获取许可节点数
        int currentHosts = hostDAO.findAll().size();    //获取已注册主机数
        int remianHosts = permissionHosts - currentHosts;    //计算剩余可安装节点数
        List<String> validHostsList = new ArrayList<>();  //存储获取到的主机列表中有效的主机列表部分
        /**
         * 生成有效主机列表
         * 如果填写的主机列表中的一些主机已经在 hosts 表中有记录，则 remainNodes++
         * 如果remianNodes>0，则向validHostsList中追加主机
         */
        for (String host : info.getHosts()) {
            for (HostEntity hostEntity : hostDAO.findAll()) {
                if (host.equals(hostEntity.getHostName())) {
                    remianHosts++;
                }
            }
            if (remianHosts > 0) {
                validHostsList.add(host);
                remianHosts--;
            }
        }
        return validHostsList;
    }

}
