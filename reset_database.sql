-- SELECT
--  *
-- FROM
--  pg_stat_activity
-- WHERE
--  datname = 'prolegotest_db';
--
-- SELECT
--  pg_terminate_backend (pg_stat_activity.pid)
-- FROM
--  pg_stat_activity
-- WHERE
--  pg_stat_activity.datname = 'prolegotest_db';


DROP DATABASE IF EXISTS prolegotest_db;
CREATE DATABASE prolegotest_db;
DROP ROLE IF EXISTS prolegotest_user;
CREATE USER prolegotest_user with PASSWORD 'my_password';
GRANT ALL PRIVILEGES ON DATABASE "prolegotest_db" to prolegotest_user;
