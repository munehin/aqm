--
-- テーブルの構造 `summaries`
--

CREATE TABLE `summaries` (
  `id` int(11) NOT NULL,
  `uploaded` date DEFAULT NULL,
  `total` int(11) DEFAULT NULL,
  `ok` int(11) DEFAULT NULL,
  `ng` int(11) DEFAULT NULL,
  `wavsize` bigint(20) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- --------------------------------------------------------

--
-- テーブルのインデックス `summaries`
--
ALTER TABLE `summaries`
  ADD PRIMARY KEY (`id`);


--
-- テーブルの AUTO_INCREMENT `summaries`
--
ALTER TABLE `summaries`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
