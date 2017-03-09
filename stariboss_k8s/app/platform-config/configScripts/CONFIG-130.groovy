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
    dataSource_url="jdbc:oracle:thin:@10.0.250.130:1521:starboss"
    dataSource_username="productuser"
    dataSource_password="productuser"
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
}

customer.default {
    business_redis_master = redis_master
    business_redis_sentinel_url = redis_sentinel_url
    dataSource_url="jdbc:oracle:thin:@10.0.250.130:1521:starboss"
    dataSource_username="customeruser"
    dataSource_password="customeruser"
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
    dataSource_url="jdbc:oracle:thin:@10.0.250.130:1521:starboss"
    dataSource_username="orderuser"
    dataSource_password="orderuser"
}

admin_crm_ui.default {
    business_redis_master = redis_master
    business_redis_sentinel_url = redis_sentinel_url
}

customer_center.default {
    business_redis_master = redis_master
    business_redis_sentinel_url = redis_sentinel_url
    dataSource_url="jdbc:oracle:thin:@10.0.250.130:1521:starboss"
    dataSource_username="custcenteruser"
    dataSource_password="custcenteruser"
}

order_center.default {
    business_redis_master = redis_master
    business_redis_sentinel_url = redis_sentinel_url
    dataSource_url="jdbc:oracle:thin:@10.0.250.130:1521:starboss"
    dataSource_username="ordercenteruser"
    dataSource_password="ordercenteruser"
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
    dataSource_url="jdbc:oracle:thin:@10.0.250.130:1521:starboss"
    dataSource_username="systemuser"
    dataSource_password="systemuser"
}

resource_ui.default {
    business_redis_master = redis_master
    business_redis_sentinel_url = redis_sentinel_url
}
resource.default {
    business_redis_master = redis_master
    business_redis_sentinel_url = redis_sentinel_url
    dataSource_url="jdbc:oracle:thin:@10.0.250.130:1521:starboss"
    dataSource_username="resourceuser"
    dataSource_password="resourceuser"
}

area.default {
    business_redis_master = redis_master
    business_redis_sentinel_url = redis_sentinel_url
    dataSource_url="jdbc:oracle:thin:@10.0.250.130:1521:starboss"
    dataSource_username="areauser"
    dataSource_password="areauser"
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
    dataSource_url="jdbc:oracle:thin:@10.0.250.130:1521:starboss"
    dataSource_username="accountuser"
    dataSource_password="accountuser"
}
account_center.default {
    business_redis_master = redis_master
    business_redis_sentinel_url = redis_sentinel_url
    dataSource_url="jdbc:oracle:thin:@10.0.250.130:1521:starboss"
    dataSource_username="accountcenteruser"
    dataSource_password="accountcenteruser"
}
collection.default {
    business_redis_master = redis_master
    business_redis_sentinel_url = redis_sentinel_url
    dataSource_url="jdbc:oracle:thin:@10.0.250.130:1521:starboss"
    dataSource_username="collectionuser"
    dataSource_password="collectionuser"
    can_back_paid_days=-1
    can_back_if_checked=false
}
collection_center.default {
    business_redis_master = redis_master
    business_redis_sentinel_url = redis_sentinel_url
    dataSource_url="jdbc:oracle:thin:@10.0.250.130:1521:starboss"
    dataSource_username="collectioncenteruser"
    dataSource_password="collectioncenteruser"
}
resource_center.default {
    business_redis_master = redis_master
    business_redis_sentinel_url = redis_sentinel_url
    dataSource_url="jdbc:oracle:thin:@10.0.250.130:1521:starboss"
    dataSource_username="resourcecenteruser"
    dataSource_password="resourcecenteruser"
}
partner.default {
    business_redis_master = redis_master
    business_redis_sentinel_url = redis_sentinel_url
    dataSource_url="jdbc:oracle:thin:@10.0.250.130:1521:starboss"
    dataSource_username="partneruser"
    dataSource_password="partneruser"
}
partner_ui.default {
    business_redis_master = redis_master
    business_redis_sentinel_url = redis_sentinel_url
}
//CONF.print()