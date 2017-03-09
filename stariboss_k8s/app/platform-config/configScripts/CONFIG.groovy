/**
 * redis哨兵集合
 */
def redis_sentinel_url = "redis1:26379"
def redis_master = "master"
portal_ui.default {
	business_redis_master = redis_master
	business_redis_sentinel_url = redis_sentinel_url
}

admin_product_ui.default {
	business_redis_master = redis_master
	business_redis_sentinel_url = redis_sentinel_url
}

product.default {
	business_redis_master = redis_master
	business_redis_sentinel_url = redis_sentinel_url
	dataSource_url="jdbc:oracle:thin:@192.168.32.152:1521:star"
	dataSource_username="boss_product"
	dataSource_password="boss_product"
}

def easyPayRule = "1:SouthAfrica"
def customerName = 1
def contactAddress = 1
customer_ui.default {
	business_redis_master = redis_master
	business_redis_sentinel_url = redis_sentinel_url
	customer_name=customerName
	customer_easypay_rule= easyPayRule
	customer_certificate_repeat=true
	customer_address_repeat=true
	address_splicing_format=contactAddress
	customer_easypay_rule = easyPayRule
}

customer.default {
	business_redis_master = redis_master
	business_redis_sentinel_url = redis_sentinel_url
	dataSource_url="jdbc:oracle:thin:@192.168.32.152:1521:star"
	dataSource_username="boss_customer"
	dataSource_password="boss_customer"
	customer_code_length= 6
	customer_code_rule= "Default"
	customer_password_rule= "Haiwai"
	customer_easypay_rule= easyPayRule
	customer_address_repeat=false
	customer_certificate_repeat=false
	customer_certificate_address_repeat=false
	server_area_language="zh"
	customer_name=customerName
	address_splicing_format=contactAddress
}

order.default {
	business_redis_master = redis_master
	business_redis_sentinel_url = redis_sentinel_url
	dataSource_url="jdbc:oracle:thin:@192.168.32.152:1521:star"
	dataSource_username="boss_order"
	dataSource_password="boss_order"
}

admin_crm_ui.default {
	business_redis_master = redis_master
	business_redis_sentinel_url = redis_sentinel_url
}

customer_center.default {
	business_redis_master = redis_master
	business_redis_sentinel_url = redis_sentinel_url
	dataSource_url="jdbc:oracle:thin:@192.168.32.152:1521:star"
	dataSource_username="boss_customer_center"
	dataSource_password="boss_customer_center"
}

order_center.default {
	business_redis_master = redis_master
	business_redis_sentinel_url = redis_sentinel_url
	dataSource_url="jdbc:oracle:thin:@192.168.32.152:1521:star"
	dataSource_username="boss_order_center"
	dataSource_password="boss_order_center"
}

def address_code_len = 3
def seg_code_len = 3
admin_public_ui.default {
	business_redis_master = redis_master
	business_redis_sentinel_url = redis_sentinel_url
	address_code_len=address_code_len
	segment_code_len=seg_code_len
	address_splicing_format=contactAddress
}

system.default {
	business_redis_master = redis_master
	business_redis_sentinel_url = redis_sentinel_url
	dataSource_url="jdbc:oracle:thin:@192.168.32.152:1521:star"
	dataSource_username="boss_system"
	dataSource_password="boss_system"
}

resource_ui.default {
	business_redis_master = redis_master
	business_redis_sentinel_url = redis_sentinel_url
}
resource.default {
	business_redis_master = redis_master
	business_redis_sentinel_url = redis_sentinel_url
	dataSource_url="jdbc:oracle:thin:@192.168.32.152:1521:star"
	dataSource_username="boss_resource"
	dataSource_password="boss_resource"
}

area.default {
	business_redis_master = redis_master
	business_redis_sentinel_url = redis_sentinel_url
	dataSource_url="jdbc:oracle:thin:@192.168.32.152:1521:star"
	dataSource_username="boss_area"
	dataSource_password="boss_area"
	address_code_len=address_code_len
	segment_code_len=seg_code_len
	address_splicing_format=contactAddress
}

platform_cache_config.default {
	business_redis_master = redis_master
	business_redis_sentinel_url = redis_sentinel_url
}

admin_billing_ui.default {
	business_redis_master = redis_master
	business_redis_sentinel_url = redis_sentinel_url
}

account.default {
	business_redis_master = redis_master
	business_redis_sentinel_url = redis_sentinel_url
	dataSource_url="jdbc:oracle:thin:@192.168.32.152:1521:star"
	dataSource_username="boss_account"
	dataSource_password="boss_account"
}
account_center.default {
	business_redis_master = redis_master
	business_redis_sentinel_url = redis_sentinel_url
	dataSource_url="jdbc:oracle:thin:@192.168.32.152:1521:star"
	dataSource_username="boss_account_center"
	dataSource_password="boss_account_center"
}
collection.default {
	business_redis_master = redis_master
	business_redis_sentinel_url = redis_sentinel_url
	dataSource_url="jdbc:oracle:thin:@192.168.32.152:1521:star"
	dataSource_username="boss_collection"
	dataSource_password="boss_collection"
	can_back_paid_days=-1
	can_back_if_checked=false
}
collection_center.default {
	business_redis_master = redis_master
	business_redis_sentinel_url = redis_sentinel_url
	dataSource_url="jdbc:oracle:thin:@192.168.32.152:1521:star"
	dataSource_username="boss_collection_center"
	dataSource_password="boss_collection_center"
}
resource_center.default {
	business_redis_master = redis_master
	business_redis_sentinel_url = redis_sentinel_url
	dataSource_url="jdbc:oracle:thin:@192.168.32.152:1521:star"
	dataSource_username="boss_resource_center"
	dataSource_password="boss_resource_center"
}
channel.default {
	business_redis_master = redis_master
	business_redis_sentinel_url = redis_sentinel_url
	dataSource_url="jdbc:oracle:thin:@192.168.32.152:1521:star"
	dataSource_username="boss_channel"
	dataSource_password="boss_channel"
}
partner.default {
	business_redis_master = redis_master
	business_redis_sentinel_url = redis_sentinel_url
	dataSource_url="jdbc:oracle:thin:@192.168.32.152:1521:star"
	dataSource_username="boss_partner"
	dataSource_password="boss_partner"
}
partner_ui.default {
	business_redis_master = redis_master
	business_redis_sentinel_url = redis_sentinel_url
}
//CONF.print()