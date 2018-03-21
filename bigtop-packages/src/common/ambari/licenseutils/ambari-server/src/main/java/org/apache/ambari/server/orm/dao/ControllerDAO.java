package org.apache.ambari.server.orm.dao;

import java.util.List; 

import javax.persistence.EntityManager; 
import javax.persistence.TypedQuery; 

import org.apache.ambari.server.orm.RequiresSession; 
import org.apache.ambari.server.orm.entities.ControllerEntity;

import com.google.inject.Inject; 
import com.google.inject.Provider; 
import com.google.inject.Singleton; 
import com.google.inject.persist.Transactional;
/**
 * Controller 操作数据库类
 * @author houjinxia
 *
 */
@Singleton
public class ControllerDAO {
	
	@Inject 	
	Provider<EntityManager> entityManagerProvider;
	
	@Inject 		
	DaoUtils daoUtils;
	
	/**
	 * 插入一条数据
	 * @param controllerEntity
	 */
	@Transactional
	public void create(ControllerEntity controllerEntity){
		entityManagerProvider.get().persist(controllerEntity);
	}
	
	/**
	 * 修改数据
	 * @param controllerEntity
	 * @return
	 */
	@Transactional 	
	public ControllerEntity merge(ControllerEntity controllerEntity){
		return entityManagerProvider.get().merge(controllerEntity);
	}
	
	/**
	 * 通过Id查找数据
	 * @param id
	 * @return
	 */
	@RequiresSession
	public ControllerEntity findById(String id){
		return entityManagerProvider.get().find(ControllerEntity.class,id);
	}
	
	/*** 	 
	 * 查出数据库中的所有数据 	 
	 * @return 	 
	*/ 	
	@RequiresSession
	public List<ControllerEntity>findAll(){
		TypedQuery<ControllerEntity> query=entityManagerProvider.get().createQuery("select controller from ControllerEntity controller",ControllerEntity.class);
		return daoUtils.selectList(query);
	}
}
