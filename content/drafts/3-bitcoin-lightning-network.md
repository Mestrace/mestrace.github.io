Title: WIP：比特币 & 闪电网络 & 树莓派
Slug: bitcoin-lightning-network
Date: 2023-02-18
Category: Blockchain
Tags: Blockchain, Raspberry Pi
Status: draft

比特币于2009年诞生，至今已有14年的历史。这段时间里，区块链行业发生了许多变化和发展。尽管如此，比特币仍然是市值最大的加密货币之一，其总市值约为417亿美元。比特币社区中的许多人都希望将比特币作为全球货币，用于日常交易，但目前由于潜在的网络拥堵、高交易费用以及需要等待至少十分钟以确保交易被确认等问题，这个愿望尚未实现。


然而，比特币社区正在积极探索解决这些问题的方案。其中最有前途的方案之一就是闪电网络。通过利用闪电网络，用户可以在比特币的二层协议上进行快速、低成本、私密的交易，避免了在主链上进行交易所面临的瓶颈和高昂的交易费用。

闪电网络的一个主要优势是能够提高比特币交易的速度和吞吐量，同时降低交易成本。与传统的比特币交易相比，闪电网络的交易速度可以达到毫秒级别，而且交易费用只占交易金额的极小部分。这使得闪电网络交易成为进行小额支付的理想选择。相较于比特币主网约7笔/秒的交易速度，闪电网络每秒能够处理超过100万笔。此外，闪电网络还提供了更高的交易隐私性。传统比特币交易的交易信息是公开的，所有人都可以查看交易记录，这可能会泄露用户的隐私信息。而闪电网络交易的信息只存储在交易双方之间，无需在主链上公开，从而提高了用户的交易隐私性。因此，闪电网络是比特币生态系统中非常重要的一部分，它的出现可以使得比特币更加适合成为全球货币，同时提供了更快、更便宜、更私密的支付体验。

# 举个简单的例子

如果你想用比特币在咖啡店买一杯5美元的咖啡，你需要创建一笔约200字节的交易，包含1个输入UTXO，1个输出UTXO和1个找零UTXO。此外，为了让你的交易在2个区块内上链（约20分钟），你需要支付大约1美元（20 Sat/Byte，0.00004 BTC）的交易费用给矿工，这对于小额交易来说显然不划算。

相比之下，使用闪电网络进行交易会更便宜且更快捷。还是以上面买咖啡的场景为例，使用闪电网络只需要支付0.0012美元（1 Sat + 0.03%）的手续费，就可以在近实时完成这笔交易。

闪电网络是一个由多个节点组成的网络。每个节点需要主动和其他节点建立微支付通道，并锁定一定数量的比特币，以建立一个支付通道。在支付通道上，交易不需要上链，只需要在双方的通道上记账就可以实现转账，转账的最大数额等于锁定的金钱数额。当支付通道关闭的时候，双方将进行结算，并将对应的转账金额上链。

以咖啡店为例，如果我和闪电网络节点A建立了链接并锁定了100美元的比特币，咖啡店与闪电网络节点B建立了链接。那么当我发起这笔支付的时候，节点A会自动寻找与节点B的路径并发起对应的转账。如果节点A和B有直接的支付通道，那么这笔钱将通过该支付通道进行转账。如果A和B没有直接的支付通道，或者A和B的支付渠道余额不足以支付这笔钱，A将自动寻找其他与B连接的路径进行转账，最终将这笔钱转账到咖啡店的节点上。当咖啡店关闭与B的通道时，B将与咖啡店进行结算并上链，我与节点A的通道同理。

# 闪电网络的渠道的生命周期

在前面两部分，我们自顶向下的介绍了闪电网络的来历以及他要解决的问题。并给出了一个简单的场景来对比比特币和闪电网络是如何工作的。在这一部分，我们将进一步延伸，介绍闪电网络的一些技术原理。

# 支付渠道。

让我们深入探讨闪电网络的技术细节前，先来回顾一下比特币交易的完成过程。在比特币主网中，交易发起方会对交易进行签名以证明其真实有效。接下来，交易将被广播到网络中的节点，由矿工将其上链，最终完成交易。

然而，闪电网络的交易机制与传统网络有所不同。作为由参与者维护的网络，闪电网络采用多个节点之间点对点连接的支付渠道，使得交易金额在节点网络中流动，并最终到达收款人手中。交易只会记录在涉及节点的本地记录上，直到渠道关闭时，双方才会通过链上交易进行结算。这样一来，交易速度得到显著提高，但同时也引发了一个问题：在一个零信任的网络中，如何确保节点双方的资金安全呢？

为解决这一问题，闪电网络采用多签交易。简单来说，多签钱包是由多位用户共同管理的钱包，根据不同设定，可能需要多位用户共同进行签名才可使用其中的资金。每位用户只知道自己的私钥，我们通常用X/Y来表示多签钱包的签名设定，代表发起一笔交易需要Y位用户的X位进行签名（当然，X ≤ Y）。交易渠道需要锁定金额，而闪电网络使用多签的方式与一个多签钱包相似。让我们深入细节，来看看闪电网络如何真正建立支付渠道。

- 初始交易（Funding Transaction / Anchor Transaction）：节点双方创建一个2/2的多签交易，并锁定等量的金额作为保证金。
- 承诺交易（Commitment Transaction）：在交易发生时，双方进行承诺交易以体现资金的流动。承诺交易记录了当前的支付渠道状态，包括节点的余额信息和对应的交易签名。
- 结算交易（Settlement Transaction）：只要将通道最后的承诺交易进行上链，交易通道也随之关闭。

在整个支付渠道的生命周期中，只有初始交易和结算交易会进行上链。在此期间，双方可以进行任意数量的链下转账，并更新承诺交易并进行签名。由于这一步骤无需上链，因此速度非常快。另外，当双方完成新的承诺交易后，之前的承诺将不再有效，这样可以防止其中一方通过将旧的承诺交易上链来进行恶意行为。此外，结算交易既可以由双方共同发起，也可以只由其中一方发起。例如，当其中一个节点离线超时时，与该节点建立支付渠道的节点可以通过发起最后一笔承诺交易来结算并解锁渠道中的资金。

# 惩罚机制

# 匿名信息

# 结论