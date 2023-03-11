Title: 简单聊聊MySQL Binlog
Slug: mysql-binlog-basics
Date: 2021-08-30
Category: Middleware
Tags: MySQL

Binlog (binary log)是一组日志文件，包含了对MySQL服务器进行的数据修改和变更，并持久化到磁盘中。Binlog以事件的格式存储，包括了所有的DDL和DML语句（例如数据表Schema的创建和变更，以及数据行的变更）。此外，每个Binlog event还囊括了一些额外的信息，包括但不限于

- 语句执行时间
- 语句执行时MySQL Server的相关状态
- 错误码
- Binlog本身的元信息（如`rotate`日志）

以及其他所有能够让此Binlog event能够被准确的重放的信息。理想条件下，在两台MySQL服务器上同时执行相同的Binlog event，最终两台MySQL服务器里的数据状态一致。
Binlog的主要作用有两个：

- MySQL集群中，对于主库的变更会通过Binlog同步到从库中。
- 数据恢复的场景下，可以重放Binlog以将数据恢复到最新的状态。

本文将主要介绍Binlog的文件格式和日志事件，并简单概括相关的应用场景。

## 文件格式

<figure align="center">
  <img src="{static}/images/6/binlog-file.png" />
  <figcaption>Binlog的文件格式</figcaption>
</figure>

- Binlog日志主要包括两类文件构成：一个日志索引（文件后缀为`.index`）和数个日志文件（文件后缀为`.NNNNNN`，`N`为一个数字）。
- 索引文件里包含了所有的日志文件的名称，并记录了当前活跃(Active)的日志文件（即当前最新的文件）
- 日志文件首先以一个魔数开头，紧接着就是一系列包含DDL和DML的binlog events事件
  - 魔数：`0xfe 0x62 0x69 0x6e = 0xfe 'b''i''n'` 
  - 日志文件的第一个事件总是`FORMAT_DESCRIPTION_EVENT / START_EVENT_V3`，描述了当前日志文件的一些系统基准信息，包括Binlog的版本，MySQL Server的版本和文件创建时间。
  - 随后的事件则根据事件类型有所不同，主要是包含了对于数据的变更信息。
  - 最后，如果这个文件不是当前的活跃日志，则它会以一个`Rotate`事件结束，并记录了下一个日志文件的名称。

<figure align="center">
  <img src="{static}/images/6/binlog-content.png" />
  <figcaption>Binlog的事件格式</figcaption>
</figure>

除了相关的管理事件以外，包含数据更新的Binlog事件通常以日志组(Group)的形式出现（如上图）。一组事件包含一个或多个Binlog事件。一个事务中所有的语句会被归属到同一个日志组。而对于其他事务无关的语句来说（如ALTER TABLE，GRANT等），每一个语句会被归属于一个独立的日志组。当需要以Binlog为基础进行数据复制或恢复时，每个组会被顺序执行，且组中的语句要么全部成功，要么全部失败。


## 日志事件

Binlog主要有三种模式。
- 基于语句的模式(Statement-based，SBR)包含实际执行的SQL语句（如`INSERT`、`UPDATE`、`DELETE`）。
  - 缺点：不仅需要记录执行的语句，而且需要额外记录语句相关的状态信息，以保证重放的时候能够产生相同的结果。在极端情况下，一些非确定性(non-deterministic)的语句可能会产生与预期不一致的结果。
- 基于行的模式(Row-based，RBR)包含对于每一个数据行的变更。
  - 缺点：会产生大量的行语句，可能会引起磁盘性能问题，且恢复的时候需要更多的时间。
- 混合模式(Mixed， MBR)主要基于语句的模式，在一些不安全（unsafe）的场景下（见[4]），会切换为基于行的模式。
  - 在使用无法确定结果的`AUTO_INCREMENT`，`LAST_INSERT_ID()`或`TIMESTAMP`时（见[5]）
  - 当function包含UUID()
  - 当使用储存过程的时候
基于语句和基于行的模式的更细节的对比见参考文献[3]。

<figure align="center">
  <img src="{static}/images/6/binlog-event-mindmap.png" />
  <figcaption>Binlog的事件类型</figcaption>
</figure>


每一个事件都由事件头Header和事件体Event Data组成。
- 一个事件头有 19 字节，依次排列为：时间戳，事件类型，服务器ID，事件长度，下一个事件的byte offset，和标识符。
- 一个事件体由两部分组成，一个固定长度的Post-Header和一个可变长度的Payload组成。Post-Header的长度对于每一种事件来说是固定的，但是不同事件是不一样的。
```text
+============+==========================+
|            |        Timestamp         |
|            |         4 bytes          |
|            +--------------------------+
|            |        Type Code         |
|            |          1 byte          |
|            +--------------------------+
|            |        Server ID         |
|            |         4 bytes          |
|   Header   +--------------------------+
|            |       Event Length       |
|            |         4 bytes          |
|            +--------------------------+
|            |      Next Position       |
|            |         4 bytes          |
|            +--------------------------+
|            |          Flags           |
|            |         2 bytes          |
+------------+--------------------------+
|            | Fixed Part (Post-Header) |
| Event Data +--------------------------+
|            | Variable Part (Payload)  |
+============+==========================+
```

当配置不同的Binlog模式时，储存的的Binlog事件不尽相同。

- 一些公共的事件，如管理事件，在所有模式下都会产生。
- Statement和Row模式下各有数种独特的事件。举个例子，ROWS_EVENT就不会出现在Statement模式下。
- 只有在开启某些配置之后才会开启的事件，如GTID_EVENT

几种常见的事件

- `FORMAT_DESCRIPTION_EVENT` / `START_EVENT_V3`：两种日志文件的起始事件，主要是根据Binlog版本不同而使用不同的事件。主要记录了Binlog版本号，MySQL Server版本号，开始时间。在Payload中会附带每种事件枚举值所对应的Post-Header长度。
- `ROTATE_EVENT`：当日志文件需要切换时所记录的最后一个事件，保存了紧接着下一个日志文件名称。切换日志文件的条件：1）当前活跃的日志文件大小超过`max_binlog_size`，或2）执行`flush logs;`命令。
- `QUERY_EVENT`：记录了被执行的SQL语句，相关的统计/debug信息（执行时间，thread id等），和相关的状态信息（是否需要auto increment，charset，tz等）。此事件通常记录的语句为：1）事务开始时的Begin操作，2）Statement模式下的DML操作，3）Row模式下的DDL操作。
- `DELETE_ROWS_EVENT` / `UPDATE_ROWS_EVENT `/ `WRITE_ROWS_EVENT`：这三种统称为ROWS_EVENT，分别对应`INSERT`, `UPDATE`和`DELETE`操作，记录在Row模式下所有的DML语句。`INSERT`包括需要插入的所有数据；`UPDATE`包括修改前的值和修改后的值；`DELETE`操作包含被删除的主键。

## 举个例子

当前MySQL版本

```
mysql Ver 14.14 Distrib 5.7.35-38, for debian-linux-gnu (x86_64) using 7.0
Percona Server (GPL), Release '38', Revision '3692a61'
```

设置binlog

```bash
# 查看 / 变更设置 - binlog
vi /etc/mysql/percona-server.conf.d/mysqld.cnf
```

在mysql shell内查看binlog相关事件

```sql
-- 查看mysql版本
show variables like '%version%';
-- 查看当前MySQL服务的binlog相关状态
show variables like '%binlog%';
-- 查看当前所有的binlog文件列表
show binary logs;
-- 查看当前所有的binlog；
show binlog events;
-- 查看当前binlog with paging
show binlog events in 'mysql-bin.000002' from 624 limit 10\G;
-- flush当前binlog文件，rotate到下一个binlog文件
flush logs;
```
使用mysqlbinlog工具查看binlog

```bash
# 进入mysql目录需要有su权限
sudo su
cd /var/log/mysql
# 查看binlog索引文件
cat bin-mysql.index
# 查看binlog日志文件 - statement
mysqlbinlog --no-defaults bin-mysql.000001
# 查看binlog日志文件 - row
mysqlbinlog --no-defaults --base64-output=DECODE-ROWS -v bin-mysql.000002
```

## 应用场景

前面讲了，Binlog的核心卖点就是能让发生在一个MySQL实例上的所有数据更新能够完整的在其他MySQL实例上重放。MySQL 5.0引入Binlog以支持主从复制，以实现灾难恢复、水平扩展、统计分析、远程数据分发等功能。

<figure align="center">
  <img src="{static}/images/6/binlog-rwsep.png" />
  <figcaption>基于Binlog主从复制实现的读写分离</figcaption>
</figure>

MySQL进群的主从复制主要有三步，如上图

1. Master在每次完成提交事务返回之前，记录本次数据变更事件至Binlog
2. Slave基于自身维护的binlog offset，从Master拉取相应的binlog更新。并记录到relay log中。
3. Slave消费relay log去更新自身的数据。

下面简述几种实际工作中会应用到的场景。

- 读写分离：在读多写少的情况下，可使用一个主库接收写流量，准实时地将Binlog同步到多个从库上进行数据同步，以实现读的水平扩展。业务也可以根据需要选择读主库。读多写少的场景在业务toC的业务上非常常见，比如在用户系统中，低频的用户注册 vs. 高频的用户登录行为。
- 数据恢复：需要进行数据恢复的时候，将Binlog进行重放即可恢复数据库的状态。
- 最终一致性：当需要保证MySQL数据库与其他组件/系统中数据一致时，可以通过订阅Binlog消息的方式进行处理，以避免出现不一致的情况。前司的数据迁移组建先同步存量数据，之后再通过binlog数据处理增量改动。
- 异地多活 / 跨DC同步：在异地多活的场景下，存在多主写入，需要互相同步的场景下，需要依赖Binlog进行同步。主要的挑战有数据冲突（主键 / 唯一键）和数据回环问题。前司在亚太区和北美区运营运营app的时候就遇到了用户数据同步的问题，开发了一款同步工具专门用于跨DC数据同步。

## 答疑解惑

1. 并发更新下，Binlog的有序性如何保证？

    在老的版本中，通过`prepare_commit_mutex`锁以串行的方式来保证MySQL数据库上层Binlog和Innodb存储引擎层的事务提交顺序一致。
    MySQL 5.6引入了`BLGC（Binary Log Group Commit）`引入队列机制保证Innodb commit顺序与binlog落盘顺序一致，并将事务分组，组内的binlog刷盘动作交给一个事务进行，以保证顺序性。
    
    - Flush Stage: 将每个事务的二进制日志写入内存中。
    - Sync Stage: 将内存中的二进制日志刷新到磁盘，若队列中有多个事务，那么仅一次fsync操作就完成了二进制日志的写入，这就是BLGC。
    - Commit Stage: 顺序调用存储引擎层事务的提交。

2. 写Binlog磁盘坏了咋办（单机故障）？

    对于业务（mysql server - 机器硬件）来说，无需额外关心这种细节，默认当成是可靠的就行了。一些额外的细节都可以在磁盘层面做屏蔽，如raid。对于数据来说，定期扫描巡检可以预防数据损坏带来的损失。

    以下原因是导致mysql 表毁坏的常见原因： 

    1. 服务器突然断电导致数据文件损坏。 
    2. 强制关机，没有先关闭mysql 服务。 
    3. mysqld 进程在写表时被杀掉。 
    4. 使用myisamchk 的同时，mysqld 也在操作表。 
    5. 磁盘故障。 
    6. 服务器死机。 
    7. mysql 本身的bug 。 

## 参考文献

如果你想变得更强的话，可以延伸看看

1. [Binlog Event, MySQL Source Code Documentation 官方代码注释](https://dev.mysql.com/doc/dev/mysql-server/latest/page_protocol_replication_binlog_event.html)
1. [C. Bell, M. Kindahl and L. Thalmann, MySQL High Availability: Tools for Building Robust Data Centers 高可用MySQL：构建健壮的数据中心](https://www.oreilly.com/library/view/mysql-high-availability/9781449341107/ch04.html)
1. [17.2.1.1 Advantages and Disadvantages of Statement-Based and Row-Based Replication, MySQL 8.0 Reference Manual 官方参考手册](https://dev.mysql.com/doc/refman/8.0/en/replication-sbr-rbr.html)
1. [5.4.4.3 Mixed Binary Logging Format, MySQL 8.0 Reference Manual 官方参考手册](https://dev.mysql.com/doc/refman/8.0/en/binary-log-mixed.html)
1. [17.5.1.1 Replication and AUTO_INCREMENT, MySQL 8.0 Reference Manual 官方参考手册](https://dev.mysql.com/doc/refman/8.0/en/replication-features-auto-increment.html)
1. [Binlog event有序性 - 阿里云RDS-数据库内核组](http://mysql.taobao.org/monthly/2014/12/05/)
1. [MySQL 中Redo与Binlog顺序一致性问题](https://www.cnblogs.com/mao3714/p/8734838.html)