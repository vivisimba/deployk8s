环境要求：JDK8,TOMCAT
配置说明：
1、在数据库中创建activiti用户，以oracle为例
	create user activiti identified by activiti;
	grant resource,connect, sysdba,dba to activiti;

2、按zk.properties和db.properties中各项配置属性的描述进行属性值配置