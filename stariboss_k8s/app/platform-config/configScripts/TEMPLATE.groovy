import com.star.common.config.Node;

TMP = new Node("TMP", this)

def common = {
    /**
     * 名称:redis空闲值:redis_maxIdle
     * 说明:redis连接池最大空闲值
     * 是否立即生效:否
     */
    redis_maxIdle = 200
    /**
     * 名称:redis最大连接数:redis_maxTotal
     * 说明:redis连接池最大链接值
     * 是否立即生效:否
     */
    redis_maxTotal = 200
    /**
     * 名称:redis最大等待毫秒值:redis_maxWaitMillis
     * 说明:redis连接最大等待毫秒值
     * 是否立即生效:否
     */
    redis_maxWaitMillis = 30000
    /**
     * 名称:redis连接超时时间(毫秒):redis_timeout
     * 说明:redis连接超时时间(毫秒)
     * 是否立即生效:否
     */
    redis_timeout = 60000
    /**
     * 名称:redis检测超时数据时间间隔(秒):redis_check_time
     * 说明:redis集群检测超时数据时间间隔(秒),用于检测hibernate二级缓存数据
     * 是否立即生效:否
     */
    redis_check_time = 20
    /**
     * 名称:redis数据超时时间(秒):redis_expiryInSeconds
     * 说明:redis数据超时时间(秒),用于设置hibernate二级缓存数据
     * 是否立即生效:否
     */
    redis_expiryInSeconds = 200
    /**
     * 名称:日志存放在redis的key:log_redis_key
     * 说明:redis中记录日志信息的key值
     * 是否立即生效:否
     */
    log_redis_key = "application-log"
    /**
     * 名称:存放业务层数据的redis集群名称:business_redis_master
     * 说明:存放业务层数据的redis集群名称
     * 是否立即生效:否
     */
    business_redis_master = "master"
    /**
     * 名称:存放业务层数据的redis集群url:business_redis_sentinel_url
     * 说明:存放业务层数据的redis集群url(哨兵地址:端口)
     * 是否立即生效:否
     */
    business_redis_sentinel_url = "redis1:26379"
    /**
     * 名称:查询数据每页条数:query_page_row
     * 说明:查询数据每页条数
     * 是否立即生效:是
     */
    query_page_row = 25
    /**
     * 名称:缓存数据存储在redis中的DB index,配置值为1~255，默认值为1
     * 是否立即生效:是
     */
    redis_cache_dbindex = 1
    /**
     * 名称:缓存日志存储在redis中的DB index,配置值为1~255，默认值为0
     * 是否立即生效:否
     */
    redis_log_dbindex = 0
    /**
     * 名称:dubbo注册服务时的注册ip配置，默认为localhost
     * 是否立即生效:否
     */
    dubbo_host = "localhost"
    /**
     * 名称:dubbo注册服务的端口号，与web服务器（tomcat）的端口一致
     * 是否立即生效:否
     */
    dubbo_port = 8080
    /**
     * dubbo注册服务的协议
     * 是否立即生效:否
     */
    dubbo_protocol = "rest"
    /**
     * 名称:dubbo注册服务的发布方式
     * 是否立即生效:否
     */
    dubbo_server = "servlet"
    /**
     * 名称:dubbo服务访问的最大时长，单位为毫秒
     * 是否立即生效:否
     */
    dubbo_timeout = 180000

    /**
     * 名称:dubbo服务集群调用访问的方式，支持：random,roundrobin,leastactive，iplist，
     * 分别表示：随机，轮循，最少活跃调用,按指定的ip列表先后进行访问如果ip列表为空或对应的ip
     * 列表中所有ip均不存在对应的服务，则按 leastactive选择服务以完成服务选择，
     * 建议开发环境配置值为iplist，运营环境配置为leastactive。
     * 是否立即生效:否
     */
    dubbo_loadbalance = "leastactive"
}

def service = {
    /**
     * 名称:数据库驱动名:dataSource_driverClassName
     * 说明:数据库驱动名
     * 是否立即生效:否
     */
    dataSource_driverClassName = "oracle.jdbc.driver.OracleDriver"
    /**
     * 名称:数据库Url:dataSource_url
     * 说明:数据库Url
     * 是否立即生效:否
     */
    dataSource_url = "jdbc:oracle:thin:@oracle1:1521:oracle"
    /**
     * 名称:数据库用户名:dataSource_username
     * 说明:数据库用户名
     * 是否立即生效:否
     */
    dataSource_username = "NewBoss"
    /**
     * 名称:数据库密码:dataSource_password
     * 说明:数据库密码
     * 是否立即生效:否
     */
    dataSource_password = "NewBoss"
    /**
     * 名称:存放数据层数据的redis集群名称:data_redis_master
     * 说明:存放hibernate二级缓存数据的redis集群名称
     * 是否立即生效:否
     */
    data_redis_master = "master"
    /**
     * 名称:存放数据层数据的redis集群url:data_redis_sentinel_url
     * 说明:存放hibernate二级缓存数据的redis集群url(哨兵地址:端口)
     * 是否立即生效:否
     */
    data_redis_sentinel_url = "redis1:26379"
}

TMP.portal_ui common

TMP.admin_product_ui common

TMP.product common
TMP.product service

TMP.customer_ui common
TMP.customer_ui {
    /**
     * 名称：个人客户名称是名+姓，还是姓+名
     * 说明:备选值1/2;1=姓+名，2=名+姓,此参数必备
     */
    customer_name = 1

    /**
     * 名称：客户级别是否必填：customer_level_required
     * 说明:备选值：required，空(""); required:必填;""：非必填
     */
    customer_level_required = ""

    /**
     * 名称：证件号码是否必填：customer_certificate_required
     * 说明:备选值：required，空(""); required:必填;""：非必填
     */
    customer_certificate_required = ""

    /**
     * 名称：email是否必填：customer_email_required
     * 说明:备选值：required，空(""); required:必填;""：非必填
     */
    customer_email_required = ""

    /**
     * 名称：地址拼接格式：address_splicing_format
     * 说明:备选值1或2。1:地址全称+详细地址（默认）,2:详细地址+“ , ”+地址全称
     */
    address_splicing_format = 1

    /**
     * 名称：电话号码允许输入的长度
     * 说明:设置11,12,13则电话号码只允许输入长度为11位，12位，13位。例如customer_tel_lenth="11,12,13"
     */
    customer_tel_lenth = ""
    /**
     * 名称：电话号码允许输入的字符
     * 说明:[0-9] 允许输入数字，其他字字符直接写；
     * 如：允许输入加号和数字  customer_tel_format="[0-9]+"
     */
    customer_tel_format = ""

    /**
     * 名称：修改页面，不可编辑属性
     * 说明:设置的字段为不可编辑字段。字段编写规则：ER中对应的字段，如果字段中存在下划线，将下划线去掉，并将首字母改为大写；
     * 如：customer_level_id 要改为：customerLevelId
     */
    customer_update_readonly = ""

    /**
     * 名称:是否校验联系地址重复:customer_address_repeat
     * 说明:是否校验联系地址重复,备选值:true（校验）,false（不校验）
     * 是否立即生效:是
     */
    customer_address_repeat = false
    /**
     * 名称:是否校验客户证件号码重复:customer_certificate_repeat
     * 说明:是否校验客户证件号码重复,备选值:true,false
     * 是否立即生效:是
     */
    customer_certificate_repeat = false
    /**
     * 名称:是校验客户证件（类型和号码）和地址重复:customer_certificate_address_repeat
     * 说明:是校验客户证件（类型和号码）和地址重复,备选值:true,false
     * 是否立即生效:是
     */
    customer_certificate_address_repeat = false
}

TMP.customer common
TMP.customer service
TMP.customer {
    /**
     * 名称:客户编码长度:customer_code_length
     * 说明:客户编码长度,参数类型整数
     * 是否立即生效:是
     */
    customer_code_length = 6
    /**
     * 名称:客户编码生成规则:customer_code_rule
     * 说明:客户编码生成规则，备选值：Default,Hebei,Tianjin
     * 是否立即生效:是
     */
    customer_code_rule = "Default"
    /**
     * 名称:客户密码生成规则 :customer_password_rule
     * 说明:客户密码生成规则，备选值：TianJin,Hebei6,Hebei8,Haiwai
     * 是否立即生效:是
     */
    customer_password_rule = "Haiwai"
    /**
     * 名称:客户EasyPay编码生成规则:customer_easypay_rule
     * 说明:客户EasyPay编码生成规则，格式为：公司Id:生成规则;公司Id:生成规则，生成规则备选值：SouthAfrica,Other
     * 是否立即生效:是
     */
    customer_easypay_rule = ""

    /**
     * 名称:所属区域语言:server_area_language
     * 说明:所属区域语言,备选值:zh,cn
     * 是否立即生效:是
     */
    server_area_language = "zh"
}

TMP.admin_crm_ui common

TMP.customer_center common
TMP.customer_center service

TMP.order common
TMP.order service

TMP.order_center common
TMP.order_center service

TMP.admin_public_ui common

TMP.admin_public_ui {
    /**
     * 名称:系统用户密码是否为数字与字母组合 :user_password_rule
     * 说明:系统用户密码是否为数字与字母组合，备选值：true,false
     * 是否立即生效:是
     */
    user_password_rule = false
    /**
     * 名称:地址编码长度 :address_code_len
     * 说明:地址编码长度
     * 是否立即生效:是
     */
    address_code_len = 3
    /**
     * 名称:网格编码长度 :segment_code_len
     * 说明:网格编码长度
     * 是否立即生效:是
     */
    segment_code_len = 3
    /**
     * 名称：地址拼接格式：address_splicing_format
     * 说明:备选值1或2。1:上级地址全称+地址名称（默认）,2:地址名称+“ , ”+上级地址全称
     */
    address_splicing_format = 1
}

TMP.system common
TMP.system service

TMP.system {
    /**
     * 名称:系统用户初始化密码:user_init_password
     * 说明:系统用户初始化密码
     * 是否立即生效:是
     */
    user_init_password = '123456'
    /**
     * 名称:系统用户密码最小长度:user_password_min_length
     * 说明:系统用户密码最小长度
     * 是否立即生效:是
     */
    user_password_min_len = 6
    /**
     * 名称:系统用户密码密码规则 :user_password_rule
     * 说明:系统用户密码密码规则，正则表达式
     * 是否立即生效:是
     */
    user_password_rule = ""
}

TMP.resource_ui common

TMP.resource common
TMP.resource service

TMP.area common
TMP.area service

TMP.area {
    /**
     * 名称:地址编码长度 :address_code_len
     * 说明:地址编码长度
     * 是否立即生效:是
     */
    address_code_len = 3
    segment_code_len = 3
    address_splicing_format = 1
}

TMP.platform_cache_config common
TMP.platform_cache_config {
    /**
     * 名称:redis 缓存数据的方式
     * 说明:redis 缓存数据的方式   all:全部缓存： increment：增量缓存
     * 是否立即生效:是
     */
    redis_cache_type = "all"
    /**
     * 名称:redis 缓存数据任务和执行时间间隔，单位为秒，默认为300秒
     * 是否立即生效:是
     */
    redis_cache_interval = 300
}
TMP.admin_billing_ui common

TMP.account common
TMP.account service

TMP.account_center common
TMP.account_center service

TMP.collection common
TMP.collection service

TMP.collection_center common
TMP.collection_center service

TMP.resource_center common
TMP.resource_center service

TMP.channel common
TMP.channel service

TMP.partner common
TMP.partner service

TMP.partner_ui common

CONF = new Node("CONF", this, TMP)

CONF.add {
    portal_ui = new Node()
    admin_product_ui = new Node()
    admin_crm_ui = new Node()
    product = new Node()
    customer_ui = new Node()
    customer = new Node()
    customer_center = new Node()
    order = new Node()
    order_center = new Node()
    admin_public_ui = new Node()
    system = new Node()
    resource_ui = new Node()
    resource = new Node()
    area = new Node()
    platform_cache_config = new Node()
    admin_billing_ui = new Node()
    account = new Node()
    account_center = new Node()
    collection = new Node()
    collection_center = new Node()
    resource_center = new Node()
    channel = new Node()
    partner = new Node()
    partner_ui = new Node()
}
