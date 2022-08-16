-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- ホスト: 127.0.0.1
-- 生成日時: 2022-03-08 01:49:16
-- サーバのバージョン： 10.4.22-MariaDB
-- PHP のバージョン: 8.1.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- データベース: `test`
--

-- --------------------------------------------------------

--
-- テーブルの構造 `job`
--

CREATE TABLE `job` (
  `id` int(11) NOT NULL,
  `name` varchar(32) DEFAULT NULL,
  `clientcode` varchar(16) DEFAULT NULL,
  `subjob` varchar(16) DEFAULT NULL,
  `sendmax` int(11) DEFAULT NULL,
  `wavmin` int(11) DEFAULT NULL,
  `wavmax` int(11) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- --------------------------------------------------------

--
-- テーブルの構造 `jobmapping`
--

CREATE TABLE `jobmapping` (
  `id` int(11) NOT NULL,
  `extension` varchar(16) NOT NULL,
  `clientcode` varchar(16) DEFAULT NULL,
  `subjob` varchar(16) DEFAULT NULL,
  `areacode` varchar(16) DEFAULT NULL,
  `areaname` varchar(32) DEFAULT NULL,
  `centercode` varchar(16) DEFAULT NULL,
  `centername` varchar(32) DEFAULT NULL,
  `job_id` int(11) NOT NULL,
  `created` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- --------------------------------------------------------

--
-- テーブルの構造 `sendlog`
--

CREATE TABLE `sendlog` (
  `id` int(11) NOT NULL,
  `changed` datetime DEFAULT NULL,
  `ctipath` varchar(256) DEFAULT NULL,
  `ctifile` varchar(64) DEFAULT NULL,
  `wavpath` varchar(256) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `uploadlog_id` int(11) DEFAULT NULL,
  `calldatetime` datetime DEFAULT NULL,
  `processedondate` datetime DEFAULT NULL,
  `disposition` varchar(64) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- --------------------------------------------------------

--
-- テーブルの構造 `svmapping`
--

CREATE TABLE `svmapping` (
  `id` int(11) NOT NULL,
  `agentpbxid` varchar(16) NOT NULL,
  `agentname` varchar(32) DEFAULT NULL,
  `supervisorname` varchar(32) DEFAULT NULL,
  `agentid` varchar(16) DEFAULT NULL,
  `job_id` int(11) NOT NULL,
  `created` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- --------------------------------------------------------

--
-- テーブルの構造 `uploadlog`
--

CREATE TABLE `uploadlog` (
  `id` int(11) NOT NULL,
  `uploaded` datetime DEFAULT NULL,
  `ctipath` varchar(256) DEFAULT NULL,
  `ctifile` varchar(64) DEFAULT NULL,
  `wavfile` varchar(64) DEFAULT NULL,
  `wavsize` int(11) DEFAULT NULL,
  `wavtime` int(11) DEFAULT NULL,
  `clientcode` varchar(16) DEFAULT NULL,
  `extension` varchar(16) DEFAULT NULL,
  `job_name` varchar(32) DEFAULT NULL,
  `agentname` varchar(32) DEFAULT NULL,
  `agentpbxid` varchar(16) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `notsend` tinyint(1) DEFAULT 0,
  `created` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- ダンプしたテーブルのインデックス
--

--
-- テーブルのインデックス `job`
--
ALTER TABLE `job`
  ADD PRIMARY KEY (`id`);

--
-- テーブルのインデックス `jobmapping`
--
ALTER TABLE `jobmapping`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UNIQUE_EXTENSION` (`extension`) USING BTREE,
  ADD KEY `INDEX_JOB_ID` (`job_id`);

--
-- テーブルのインデックス `sendlog`
--
ALTER TABLE `sendlog`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ctifile` (`ctifile`);

--
-- テーブルのインデックス `svmapping`
--
ALTER TABLE `svmapping`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UNIQUE_AGENTPBXID` (`id`),
  ADD KEY `INDEX_JOB_ID` (`job_id`);

--
-- テーブルのインデックス `uploadlog`
--
ALTER TABLE `uploadlog`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ctipath` (`ctipath`);

--
-- ダンプしたテーブルの AUTO_INCREMENT
--

--
-- テーブルの AUTO_INCREMENT `job`
--
ALTER TABLE `job`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- テーブルの AUTO_INCREMENT `jobmapping`
--
ALTER TABLE `jobmapping`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- テーブルの AUTO_INCREMENT `sendlog`
--
ALTER TABLE `sendlog`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- テーブルの AUTO_INCREMENT `svmapping`
--
ALTER TABLE `svmapping`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- テーブルの AUTO_INCREMENT `uploadlog`
--
ALTER TABLE `uploadlog`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
