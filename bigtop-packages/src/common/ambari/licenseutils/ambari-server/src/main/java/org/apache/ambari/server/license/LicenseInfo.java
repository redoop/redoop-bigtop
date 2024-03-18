package org.apache.ambari.server.license;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

import org.apache.ambari.server.license.utils.Base64;
import org.apache.ambari.server.license.utils.RSAEncrypt;


import com.google.inject.Singleton;

/**
 * 从license文件中解析license内容
 * 是个单例对象
 * @author houjinxia
 * 
 */

@Singleton
public class LicenseInfo {

	private String licenseId;
	private String vaildTime;
	private String macAddress;
	private String regDate;
	private String permissionHosts;
	
	private static volatile LicenseInfo instance = null;
	
	private LicenseInfo(){
		String content=null;
		try {
			content = decode(loadLicenses("/etc/redoop/LICENSE"),("/etc/redoop/publicKey.keystore"));
		} catch (Exception e) {
			e.printStackTrace();
		}
		
		if(content!=null){
			licenseId=content.split(",")[0].split(":")[1];
			macAddress=content.split(",")[1].split(":")[1];
			vaildTime=content.split(",")[2].split(":")[1];
			regDate=content.split(",")[3].split(":")[1];
			permissionHosts=content.split(",")[4].split(":")[1];
		}
	}
	
	public static LicenseInfo getInstance(){
		if (instance == null) {
			synchronized (LicenseInfo.class) {
				if (instance == null) {
					instance = new LicenseInfo();
				}
			}
		}
		return instance;
	}
	


	/**
	 * 加载license 文件
	 * @param filepath
	 * @return
	 * @throws Exception
	 */
	public String loadLicenses(String filepath) throws Exception{
		try {
			BufferedReader br = new BufferedReader(new FileReader(filepath));
			String readLine = null;
			StringBuilder sb = new StringBuilder();
			while ((readLine = br.readLine()) != null) {
				sb.append(readLine);
			}

			br.close();
			return sb.toString();
		} catch (IOException e) {
			throw new Exception("License file not found! Please sign in to www.redoop.com");
		} catch (NullPointerException e) {
			throw new Exception("LicenseContent BufferedReader IS NULL");
		}
	}
	
	/**
	 * 解密license内容
	 * @param content
	 * @param filepath
	 * @return
	 */
	public  String decode(String content, String filepath) {
		String result = null;
		try {
			byte[] res = RSAEncrypt.decrypt(RSAEncrypt.loadPublicKeyByStr(RSAEncrypt.loadPublicKeyByFile(filepath)), Base64.decode(content));
			result = new String(res);
		}catch (Exception e) {
			e.printStackTrace();
		}
		return result;
	}

	public String getLicenseId() {
		return licenseId;
	}

	public String getVaildTime() {
		return vaildTime;
	}

	public String getMacAddress() {
		return macAddress;
	}

	public String getRegDate() {
		return regDate;
	}

	public String getPermissionHosts() {
		return permissionHosts;
	}
	
	
}
