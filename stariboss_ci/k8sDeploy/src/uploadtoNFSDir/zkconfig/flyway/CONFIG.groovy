import com.star.common.config.Basic;

def address_code_len = 3
def seg_code_len = 3
def easyPayRule = "1:SouthAfrica;2:Other"
def customerName = 1
def contactAddress = 1
def telLength=""
def telFormat=""

def pageRow = 25

/****************************** Platfrom ******************************/
platform_cache_config.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
}
/****************************** Platfrom ******************************/

/******************************    UI    ******************************/
admin_billing_ui.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
}

admin_crm_ui.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
}

admin_oss_ui.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
}

admin_product_ui.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
}

admin_public_ui.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    address_code_len = address_code_len
    segment_code_len = seg_code_len
    address_splicing_format = contactAddress
}

partner_ui.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
}

customer_ui.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    customer_name = customerName
    customer_easypay_rule = easyPayRule
    customer_certificate_repeat = true
    customer_address_repeat = true
    address_splicing_format = contactAddress
    customer_tel_lenth = telLength
    customer_tel_format = telFormat
}

portal_ui.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
}

resource_ui.default {
    contract_search_limited_by_payment_status = 3
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
}

operator_ui.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
}
knowledge_ui.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
}
worker_ui.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    activity_days = 7
    worker_tel_lenth=telLength
    worker_tel_format=telFormat
}
/******************************    UI    ******************************/

/******************************  service ******************************/
account.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    dataSource_url = Basic.DATA_SOURCE_URL
    dataSource_init_username = "system"
    dataSource_init_password = "123456"
    dataSource_username = "accountuser"
    dataSource_password = "accountuser"
    table_space = "TBLBOSSACCOUNT"
    db_file_name = "/oracle/oradata/orcl/tblbossaccount.dbf"
    auto_migrate = "true"
}

account_center.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    dataSource_url = Basic.DATA_SOURCE_URL
    dataSource_init_username = "system"
    dataSource_init_password = "123456"
    dataSource_username = "accountcenteruser"
    dataSource_password = "accountcenteruser"
    table_space = "TBLBOSSACCOUNTCENTER"
    db_file_name = "/oracle/oradata/orcl/tblbossaccountcenter.dbf"
    auto_migrate = "true"
}

area.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    dataSource_url = Basic.DATA_SOURCE_URL
    dataSource_init_username = "system"
    dataSource_init_password = "123456"
    dataSource_username = "areauser"
    dataSource_password = "areauser"
    address_code_len = address_code_len
    segment_code_len = seg_code_len
    address_splicing_format = contactAddress
    table_space = "TBLBOSSAREA"
    db_file_name = "/oracle/oradata/orcl/tblbossarea.dbf"
    auto_migrate = "true"
}

card.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    dataSource_url = Basic.DATA_SOURCE_URL
    dataSource_init_username = "system"
    dataSource_init_password = "123456"
    dataSource_username = "carduser"
    dataSource_password = "carduser"
    table_space = "TBLBOSSCARD"
    db_file_name = "/oracle/oradata/orcl/tblbosscard.dbf"
    auto_migrate = "true"
}

card_center.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    dataSource_url = Basic.DATA_SOURCE_URL
    dataSource_init_username = "system"
    dataSource_init_password = "123456"
    dataSource_username = "cardcenteruser"
    dataSource_password = "cardcenteruser"
    table_space = "TBLBOSSCARDCENTER"
    db_file_name = "/oracle/oradata/orcl/tblbosscardcenter.dbf"
    auto_migrate = "true"
}

channel.default {
    business_redis_master =  Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    dataSource_url = Basic.DATA_SOURCE_URL
    dataSource_init_username = "system"
    dataSource_init_password = "123456"
    dataSource_username = "CHANNELUSER"
    dataSource_password = "CHANNELUSER"
    table_space = "TBLBOSSCHANNEL"
    db_file_name = "/oracle/oradata/orcl/tblbosschannel.dbf"
    auto_migrate = "true"
}

collection.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    dataSource_url = Basic.DATA_SOURCE_URL
    dataSource_init_username = "system"
    dataSource_init_password = "123456"
    dataSource_username = "collectionuser"
    dataSource_password = "collectionuser"
    table_space = "TBLBOSSCOLLECTION"
    db_file_name = "/oracle/oradata/orcl/tblbosscollection.dbf"
    auto_migrate = "true"
}

collection_center.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    dataSource_url = Basic.DATA_SOURCE_URL
    dataSource_init_username = "system"
    dataSource_init_password = "123456"
    dataSource_username = "collectioncenteruser"
    dataSource_password = "collectioncenteruser"
    table_space = "TBLBOSSCOLLECTIONCENTER"
    db_file_name = "/oracle/oradata/orcl/tblbosscollectioncenter.dbf"
    auto_migrate = "true"
}

customer.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    dataSource_url = Basic.DATA_SOURCE_URL
    dataSource_init_username = "system"
    dataSource_init_password = "123456"
    dataSource_username = "customeruser"
    dataSource_password = "customeruser"
    customer_code_length = 6
    customer_code_rule = "Default"
    customer_password_rule = "Haiwai"
    customer_easypay_rule = easyPayRule
    customer_address_repeat = false
    customer_certificate_repeat = false
    customer_certificate_address_repeat = false
    server_area_language = "zh"
    customer_name = customerName
    address_splicing_format = contactAddress
    table_space = "TBLBOSSCUSTOMER"
    db_file_name = "/oracle/oradata/orcl/tblbosscustomer.dbf"
    auto_migrate = "true"
}

customer_center.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    dataSource_url = Basic.DATA_SOURCE_URL
    dataSource_init_username = "system"
    dataSource_init_password = "123456"
    dataSource_username = "custcenteruser"
    dataSource_password = "custcenteruser"
    table_space = "TBLBOSSCUSTCENTER"
    db_file_name = "/oracle/oradata/orcl/tblbosscustcenter.dbf"
    auto_migrate = "true"
}

job.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    dataSource_url = Basic.DATA_SOURCE_URL
    dataSource_init_username = "system"
    dataSource_init_password = "123456"
    dataSource_username = "jobuser"
    dataSource_password = "jobuser"
    table_space = "TBLBOSSJOB"
    db_file_name = "/oracle/oradata/orcl/tblbossjob.dbf"
    auto_migrate = "true"
}

note.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    dataSource_url = Basic.DATA_SOURCE_URL
    dataSource_init_username = "system"
    dataSource_init_password = "123456"
    dataSource_username = "noteuser"
    dataSource_password = "noteuser"
    table_space = "TBLBOSSNOTE"
    db_file_name = "/oracle/oradata/orcl/tblbossnote.dbf"
    auto_migrate = "true"
}

note_center.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    dataSource_url = Basic.DATA_SOURCE_URL
    dataSource_init_username = "system"
    dataSource_init_password = "123456"
    dataSource_username = "notecenteruser"
    dataSource_password = "notecenteruser"
    table_space = "TBLBOSSNOTECENTER"
    db_file_name = "/oracle/oradata/orcl/tblbossnotecenter.dbf"
    auto_migrate = "true"
}

order.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    dataSource_url = Basic.DATA_SOURCE_URL
    dataSource_init_username = "system"
    dataSource_init_password = "123456"
    dataSource_username = "orderuser"
    dataSource_password = "orderuser"
    table_space = "TBLBOSSORDER"
    db_file_name = "/oracle/oradata/orcl/tblbossorder.dbf"
    auto_migrate = "true"
}

order_center.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    dataSource_url = Basic.DATA_SOURCE_URL
    dataSource_init_username = "system"
    dataSource_init_password = "123456"
    dataSource_username = "ordercenteruser"
    dataSource_password = "ordercenteruser"
    table_space = "TBLBOSSORDERCENTER"
    db_file_name = "/oracle/oradata/orcl/tblbossordercenter.dbf"
    auto_migrate = "true"
}

partner.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    dataSource_url = Basic.DATA_SOURCE_URL
    dataSource_init_username = "system"
    dataSource_init_password = "123456"
    dataSource_username = "PARTNERUSER"
    dataSource_password = "PARTNERUSER"
    table_space = "TBLBOSSPARTNER"
    db_file_name = "/oracle/oradata/orcl/tblbosspartner.dbf"
    auto_migrate = "true"
}

problem.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    dataSource_url = Basic.DATA_SOURCE_URL
    dataSource_init_username = "system"
    dataSource_init_password = "123456"
    dataSource_username = "problemuser"
    dataSource_password = "problemuser"
    table_space = "TBLBOSSPROBLEM"
    db_file_name = "/oracle/oradata/orcl/tblbossproblem.dbf"
    auto_migrate = "true"
    ocs_dataSource_url = dataSourceUrl
    ocs_dataSource_username = "boss_ocs"
    ocs_dataSource_password = "boss_ocs"
}

problem_center.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    dataSource_url = Basic.DATA_SOURCE_URL
    dataSource_init_username = "system"
    dataSource_init_password = "123456"
    dataSource_username = "problemcenteruser"
    dataSource_password = "problemcenteruser"
    table_space = "TBLBOSSPROBLEMCENTER"
    db_file_name = "/oracle/oradata/orcl/tblbossproblemcenter.dbf"
    auto_migrate = "true"
}

product.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    dataSource_url = Basic.DATA_SOURCE_URL
    dataSource_init_username = "system"
    dataSource_init_password = "123456"
    dataSource_username = "productuser"
    dataSource_password = "productuser"
    table_space = "TBLBOSSPRODUCT"
    db_file_name = "/oracle/oradata/orcl/tblbossproduct.dbf"
    auto_migrate = "true"
}

resource.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    dataSource_url = Basic.DATA_SOURCE_URL
    dataSource_init_username = "system"
    dataSource_init_password = "123456"
    dataSource_username = "resourceuser"
    dataSource_password = "resourceuser"
    table_space = "TBLBOSSRESOURCE"
    db_file_name = "/oracle/oradata/orcl/tblbossresource.dbf"
    auto_migrate = "true"
}

resource_center.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    dataSource_url = Basic.DATA_SOURCE_URL
    dataSource_init_username = "system"
    dataSource_init_password = "123456"
    dataSource_username = "RESOURCECENTERUSER"
    dataSource_password = "RESOURCECENTERUSER"
    table_space = "TBLBOSSRESCENTER"
    db_file_name = "/oracle/oradata/orcl/tblbossrescenter.dbf"
    auto_migrate = "true"
}

system.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    dataSource_url = Basic.DATA_SOURCE_URL
    dataSource_username = "systemuser"
    dataSource_password = "systemuser"
    dataSource_init_username = "system"
    dataSource_init_password = "123456"
    table_space = "TBLBOSSSYSTEM"
    db_file_name = "/oracle/oradata/orcl/tblbosssystem.dbf"
    auto_migrate = "true"
}

message_center.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    dataSource_url = Basic.DATA_SOURCE_URL
    dataSource_username = "messagecenteruser"
    dataSource_password = "messagecenteruser"
    dataSource_init_username = "system"
    dataSource_init_password = "123456"

    table_space = "TBLBOSSMESSAGECENTER"
    db_file_name = "/oracle/oradata/orcl/tblbossmessagecenter.dbf"
    auto_migrate = "true"
}
knowledge.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    dataSource_url = Basic.DATA_SOURCE_URL
    dataSource_username = "knowledgeuser"
    dataSource_password = "knowledgeuser"
    dataSource_init_username = "system"
    dataSource_init_password = "123456"
    table_space = "TBLBOSSKNOWLEDGE"
    db_file_name = "/oracle/oradata/orcl/tblbossknowledge.dbf"
    auto_migrate = "true"
}
check.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    dataSource_url = Basic.DATA_SOURCE_URL
    dataSource_username = "checkuser"
    dataSource_password = "checkuser"
    dataSource_init_username = "system"
    dataSource_init_password = "123456"
    table_space = "TBLBOSSCHECK"
    db_file_name = "/oracle/oradata/orcl/tblbosscheck.dbf"
    auto_migrate = "true"
}

api_gateway.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
}

iom_center.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    dataSource_url = Basic.DATA_SOURCE_URL
    dataSource_username = "iomcenteruser"
    dataSource_password = "iomcenteruser"
    dataSource_init_username = "system"
    dataSource_init_password = "123456"
    table_space = "TBLBOSSIOMCENTER"
    db_file_name = "/oracle/oradata/orcl/tblbossiomcenter.dbf"
    auto_migrate = "true"
}

iom.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    dataSource_url = Basic.DATA_SOURCE_URL
    dataSource_username = "iomuser"
    dataSource_password = "iomuser"
    dataSource_init_username = "system"
    dataSource_init_password = "123456"
    table_space = "TBLBOSSIOM"
    db_file_name = "/oracle/oradata/orcl/tblbossiom.dbf"
    auto_migrate = "true"
}

pms_center.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    dataSource_url = Basic.DATA_SOURCE_URL
    dataSource_username = "pmscenteruser"
    dataSource_password = "pmscenteruser"
    dataSource_init_username = "system"
    dataSource_init_password = "123456"
    table_space = "TBLBOSSPMSCENTER"
    db_file_name = "/oracle/oradata/orcl/tblbosspmscenter.dbf"
    auto_migrate = "true"
}

pms_partition.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    dataSource_url = Basic.DATA_SOURCE_URL
    dataSource_username = "pmspartitionuser"
    dataSource_password = "pmspartitionuser"
    dataSource_init_username = "system"
    dataSource_init_password = "123456"
    table_space = "TBLBOSSPMSPARTITION"
    db_file_name = "/oracle/oradata/orcl/tblbosspmspartition.dbf"
    auto_migrate = "true"
    smart_card_default_pin = "123456"
    stb_default_pin = "123456"
    manual_instruction_max_days = "2"
}

pms_frontend_conax.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    auto_migrate = "true"
}

callcenter_proxy.default {
    business_redis_master = Basic.REDIS_MASTER
    business_redis_sentinel_url = Basic.REDIS_SENTINEL_URL
    query_page_row = pageRow
    connector_usr = 1000
    connector_pwd = 123456
}

/******************************  service ******************************/