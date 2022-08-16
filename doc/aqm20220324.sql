-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- ホスト: 127.0.0.1
-- 生成日時: 2022-03-24 15:14:28
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
-- データベース: `aqm`
--

-- --------------------------------------------------------

--
-- テーブルの構造 `jobmappings`
--

CREATE TABLE `jobmappings` (
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
-- テーブルの構造 `jobs`
--

CREATE TABLE `jobs` (
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
-- テーブルの構造 `sendlogs`
--

CREATE TABLE `sendlogs` (
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
-- テーブルの構造 `svmappings`
--

CREATE TABLE `svmappings` (
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
-- テーブルの構造 `uploadlogs`
--

CREATE TABLE `uploadlogs` (
  `id` int(11) NOT NULL,
  `uploaded` datetime DEFAULT NULL,
  `ctipath` varchar(256) DEFAULT NULL,
  `ctifile` varchar(64) DEFAULT NULL,
  `wavfile` varchar(64) DEFAULT NULL,
  `wavsize` int(11) DEFAULT NULL,
  `wavtime` int(11) DEFAULT NULL,
  `clientcode` varchar(16) DEFAULT NULL,
  `extension` varchar(16) DEFAULT NULL,
  `job_id` int(11) DEFAULT NULL,
  `agentname` varchar(32) DEFAULT NULL,
  `agentpbxid` varchar(16) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `notsend` tinyint(1) DEFAULT 0,
  `created` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- --------------------------------------------------------

--
-- テーブルの構造 `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- テーブルのデータのダンプ `users`
--

INSERT INTO `users` (`id`, `email`, `password`, `created`, `modified`) VALUES
(1, 'test@gmail.com', '$2y$10$HYZCEjGJEiUbpL0IHG6Rc.5.iJkZny5bbR4QrBTdjIDV5yMfjt55W', '2022-03-24 04:52:21', '2022-03-24 04:52:21');

--
-- ダンプしたテーブルのインデックス
--

--
-- テーブルのインデックス `jobmappings`
--
ALTER TABLE `jobmappings`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UNIQUE_EXTENSION` (`extension`) USING BTREE,
  ADD KEY `INDEX_JOB_ID` (`job_id`);

--
-- テーブルのインデックス `jobs`
--
ALTER TABLE `jobs`
  ADD PRIMARY KEY (`id`);

--
-- テーブルのインデックス `sendlogs`
--
ALTER TABLE `sendlogs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ctifile` (`ctifile`),
  ADD KEY `ctipath` (`ctipath`);

--
-- テーブルのインデックス `svmappings`
--
ALTER TABLE `svmappings`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UNIQUE_AGENTPBXID` (`id`),
  ADD KEY `INDEX_JOB_ID` (`job_id`);

--
-- テーブルのインデックス `uploadlogs`
--
ALTER TABLE `uploadlogs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ctipath` (`ctipath`);

--
-- テーブルのインデックス `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD KEY `email` (`email`);

--
-- ダンプしたテーブルの AUTO_INCREMENT
--

--
-- テーブルの AUTO_INCREMENT `jobmappings`
--
ALTER TABLE `jobmappings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- テーブルの AUTO_INCREMENT `jobs`
--
ALTER TABLE `jobs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- テーブルの AUTO_INCREMENT `sendlogs`
--
ALTER TABLE `sendlogs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- テーブルの AUTO_INCREMENT `svmappings`
--
ALTER TABLE `svmappings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- テーブルの AUTO_INCREMENT `uploadlogs`
--
ALTER TABLE `uploadlogs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- テーブルの AUTO_INCREMENT `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
