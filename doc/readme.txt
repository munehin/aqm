●インストール
・MySQLdb
pip install mysqlclient

●共有フォルダ

●MySQLへ接続
・AWS
CREATE USER 'user01'@'10.0.1.117' IDENTIFIED BY 'pa$$word';
GRANT ALL PRIVILEGES ON aqm.* TO 'user01'@'10.0.1.117';
FLUSH PRIVILEGES;
SHOW GRANTS FOR 'user01'@'10.0.1.117';

CREATE USER 'user01'@'10.0.1.244' IDENTIFIED BY 'pa$$word';
GRANT ALL PRIVILEGES ON aqm.* TO 'user01'@'10.0.1.244';
FLUSH PRIVILEGES;
SHOW GRANTS FOR 'user01'@'10.0.1.244';

CREATE USER 'user02'@'10.0.1.117' IDENTIFIED BY 'pa$$w0rd';
GRANT ALL PRIVILEGES ON ocqm.* TO 'user02'@'10.0.1.117';
FLUSH PRIVILEGES;
SHOW GRANTS FOR 'user02'@'10.0.1.117';

CREATE USER 'user02'@'10.0.1.244' IDENTIFIED BY 'pa$$w0rd';
GRANT ALL PRIVILEGES ON ocqm.* TO 'user02'@'10.0.1.244';
FLUSH PRIVILEGES;
SHOW GRANTS FOR 'user02'@'10.0.1.244';

・本番
CREATE USER 'user01'@'169.254.150.109' IDENTIFIED BY 'pa$$word';
GRANT ALL PRIVILEGES ON aqm.* TO 'user01'@'169.254.150.109';
FLUSH PRIVILEGES;
SHOW GRANTS FOR 'user01'@'169.254.150.109';

CREATE USER 'user01'@'169.254.150.110' IDENTIFIED BY 'pa$$word';
GRANT ALL PRIVILEGES ON aqm.* TO 'user01'@'169.254.150.110';
FLUSH PRIVILEGES;
SHOW GRANTS FOR 'user01'@'169.254.150.110';

CREATE USER 'user02'@'169.254.150.109' IDENTIFIED BY 'pa$$w0rd';
GRANT ALL PRIVILEGES ON ocqm.* TO 'user02'@'169.254.150.109';
FLUSH PRIVILEGES;
SHOW GRANTS FOR 'user02'@'169.254.150.109';

CREATE USER 'user02'@'169.254.150.110' IDENTIFIED BY 'pa$$w0rd';
GRANT ALL PRIVILEGES ON ocqm.* TO 'user02'@'169.254.150.110';
FLUSH PRIVILEGES;
SHOW GRANTS FOR 'user02'@'169.254.150.110';


●カラムの追加
ALTER TABLE uploadlogs ADD wavdate DATE NULL AFTER wavsize;
ALTER TABLE jobs ADD sendmin int NULL AFTER subjob;

●ログの利用
DEBUG	10	動作確認の記録
INFO	20	正常動作の記録
WARNING	30	警告の記録
ERROR	40	エラーなど重大な問題

logger.debug('debug')
logger.info('info')
logger.warning('warning')
logger.error('error')

●OpenSSHのインストール
[設定] を開き、 [アプリ] ‐ [アプリと機能] ‐ [オプション機能] ‐ [機能の追加]
OpenSSH Server をインストール

●sftpの接続
pip install paramiko

●環境依存文字
ドコモバイクシェア|759430|𠮷金　靜香|dummy|s742113

●aws上の文字コード
「設定」「時刻と言語」‐「地域」‐「日付、時刻、地域の追加設定」‐「地域」‐「管理」‐「システムロケールの変更」‐「現在のシステムロケール」：日本