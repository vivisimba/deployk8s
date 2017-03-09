import com.star.common.config.Basic;

Basic.REDIS_SENTINEL_URL = "{sentinel_ip}:26379"
Basic.REDIS_MASTER = "{sentinel_name}"
Basic.DATABASE_SERVER_IP = "{oracle_ip}"
Basic.DATABASE_PORT = "1521"
Basic.DATABASE_INSTANCE_NAME = "{oracle_service_name}"
Basic.DATA_SOURCE_URL = "jdbc:oracle:thin:@" + Basic.DATABASE_SERVER_IP + ":" + Basic.DATABASE_PORT + ":" + Basic.DATABASE_INSTANCE_NAME