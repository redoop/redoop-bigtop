package org.apache.ambari.server.orm.entities;

import javax.persistence.*;

/***
 * Controller实体类
 * 对应的表名是controller
 * @author houjinxia
 *
 */

@Entity
@Table(name = "controller") 
public class ControllerEntity {
	
	@Id 		
	@Column(name = "controller_id")
	private String controllerId;
	
	@Column(name = "vaild_time")
	private String vaildTime;
	
	@Column(name = "mac_address")
	private String macAddress;
	
	@Column(name = "reg_date")
	private String regDate;
	
	@Column(name = "remain_time")
	private String remainTime;
	
	@Column(name = "permission_hosts")
	private String permissionHosts;

	public String getControllerId() {
		return controllerId;
	}

	public void setControllerId(String controllerId) {
		this.controllerId = controllerId;
	}

	public String getVaildTime() {
		return vaildTime;
	}

	public void setVaildTime(String vaildTime) {
		this.vaildTime = vaildTime;
	}

	public String getMacAddress() {
		return macAddress;
	}

	public void setMacAddress(String macAddress) {
		this.macAddress = macAddress;
	}

	public String getRegDate() {
		return regDate;
	}

	public void setRegDate(String regDate) {
		this.regDate = regDate;
	}

	public String getRemainTime() {
		return remainTime;
	}

	public void setRemainTime(String remainTime) {
		this.remainTime = remainTime;
	}

	public String getPermissionHosts() {
		return permissionHosts;
	}

	public void setPermissionHosts(String permissionHosts) {
		this.permissionHosts = permissionHosts;
	}

	@Override
	public String toString() {
		return "ControllerEntity [controllerId=" + controllerId
				+ ", vaildTime=" + vaildTime + ", macAddress=" + macAddress
				+ ", regDate=" + regDate + ", remainTime=" + remainTime
				+ ", permissionHosts=" + permissionHosts + "]";
	}
	
	

}
