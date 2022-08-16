drop table `jobmappings`;
drop table `jobs`;
drop table `svmappings`;


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
-- テーブルのインデックス `svmappings`
--
ALTER TABLE `svmappings`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UNIQUE_AGENTPBXID` (`agentpbxid`) USING BTREE,
  ADD KEY `INDEX_JOB_ID` (`job_id`);

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
-- テーブルの AUTO_INCREMENT `svmappings`
--
ALTER TABLE `svmappings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
