SELECT dbv.version_no FROM DAILY_BUILD_VERSION dbv WHERE dbv.seq_no = (SELECT MAX(dbv2.seq_no) FROM DAILY_BUILD_VERSION dbv2);


exit;
