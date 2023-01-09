CREATE USER 'replication_user'@'%' IDENTIFIED BY 'supersecret';
GRANT REPLICATION SLAVE ON *.* TO 'replication_user'@'%';

CREATE USER 'inspection_user'@'%' IDENTIFIED BY 'supersecret';
GRANT SLAVE MONITOR ON *.* TO 'inspection_user'@'%';

FLUSH PRIVILEGES;
