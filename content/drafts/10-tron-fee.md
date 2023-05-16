Title: Tron的手续费模型和质押2.0
Slug: tron-fee-stake-2-0
Date: 2023-03-24
Category: Blockchain
Status: draft

最近我有幸参与了一个有趣的Tron波场网络项目，是关于即将上线的Tron Stake 2.0的一些优化。在研究Tron的手续费模型时，我发现它并不像其他区块链那样简单。不仅有普通的燃烧gas机制，还引入了资源机制。然而，除了官方中文资料外，关于Tron资源模型的讨论并不多。因此，我决定整理一下相关资料和自己的思考，撰写这篇文章，希望能够帮助更多入门用户了解Tron的资源模型。在本文中，我将首先简要介绍Tron的资源模型，然后介绍动态能量机制，接着讲述Stake 2.0新引入的资源授权机制，最后探讨这个资源模型在经济上的意义。与此同时，我也想分享一些我在这个项目中学到的经验和见解。希望这篇文章能够成为Tron开发者们的有用参考资料。

## Tron的资源模型

在一个区块链服务中，一笔交易需要消耗网络资源和存储资源。此外，对于智能合约来说，合约的计算还需消耗相当多的计算资源。如果有人恶意发起大量无用交易进行洪水攻击，势必会影响正常交易的进行。为了保证网络的生态和可持续性，各个区块链采用了不同的实现方式以防止这种情况。比特币采用了矿工费的机制，若矿工费较少，交易就很难被打包上链。在以太坊里面，交易发起方需要燃烧一定数量的以太币作为燃料。而 Tron 采用了一种完全不同的机制，这就是 Tron 的资源模型。Tron 的资源模型在保证交易公平的基础上，还降低了使用者的花费。

Tron网络定义了两种资源：带宽（bandwidth）和能量（energy）。带宽对应网络资源和存储资源，而能量则代表计算资源。交易在计算机里的形式以字节的形式进行传输和存储，因此一个交易需要花费`交易字节数 * 带宽费率`的带宽。此外，对于智能合约交易，不仅需要消耗带宽，还需要消耗能量。能量的使用与合约的复杂度和执行时间有关，复杂度越高、执行时间越长的合约，所需的能量就越多。当然，如果用户没有资源的时候，仍然可以通过燃烧一定数量的Tron本币TRX来进行交易，具体的计算逻辑为`消耗的资源数量 * 资源单价`。资源单价是网络中的一个参数，目前能量`1 Energy = 0.00042 TRX`，而带宽`1 Bandwidth Point = 0.001 TRX`。网络参数可以经由超级代表投票表决后进行修改，所以这两个值并不是永远不会变化的，这点需要注意。但话反过来说就是，如果用户有资源的话，交易完全不需要手续费了！

<p align="center">
  <img src="{static}/images/where_sold.jpg" />
</p>

## 质押以获得资源

早在2018年的时候，Tron就引入了质押机制。通过质押TRX，就可以获得一定数量的能量或者带宽。在获得资源的同时，每质押1TRX也可以获得1TP（Tron Power），用于给代表候选人投票[ref]参考[官方指南 - 超级代表](https://cn.developers.tron.network/docs/super-representatives)[/ref]。质押的TRX可以在一定天数之后解除质押，目前为3天。节点提供了两个API供用户使用

- `/wallet/freezebalance(owner_address, freeze_balance, resource, receiver_address)`
  
    质押`freeze_balance`金额的TRX以获得带宽（`resource="BANDWIDTH"`）或能量（`resource="ENERGY"`）。可选传入一个`receiver_address`以将这部分资源转移给指定的地址，否则的话质押的资源会属于`owner_address`。

- `wallet/unfreezebalance(owner_address, resource, receiver_address)`

    解除对应资源类型的质押的全部金额。可选传入一个`receiver_address`以解除之前转移的资源。

质押的TRX数额和资源的计算比率是一个动态的值，由全网对于资源的数额来决定。对于带宽来说，计算公式为

$$
bandwidth = \frac{\textit{trx_staked_for_bandwidth}}{\textit{network_trx_staked_for_bandwidth}} * 43\,200\,000\,000
$$

此外，每个账号每天都有1500点的免费能量 ---- 毕竟，谁不爱免费的东西呢。对于能量来说，计算公式也是熟悉的造型

$$
energy = \frac{\textit{trx_staked_for_energy}}{\textit{network_trx_staked_for_energy}} * 90\,000\,000\,000 
$$

刚刚我们聊到，两种资源都是动态的。这里的动态意思其实就是，你质押之后获得的资源并不是一个固定的金额，而是随着网络质押总量变化而产生变化的。这里我们用一个例子简单阐述一下。

1. Alice质押了$880$ TRX以获取能量，此时全网总量为$279\,313\,210$，因此Alice获得$283\,551$能量。
2. Bob随后质押了$10\,000$ TRX以获取能量，此时全网总量为$279\,314\,090$，因此Bob获得$3\,222\,063$能量。
3. Alice的能量余额因为全网质押总额发生了变化，变为$283\,541$能量。

这就是资源获得因为全网总质押资源发生改变而改变的一个例子。带宽的动态改变也遵循同样的逻辑。

## 时间让资源恢复

跟爱不一样的是，在用户使用了资源之后，使用过的资源并不会消失。使用过的资源会在24小时之内平滑恢复至0。不考虑上述全网资源变化的逻辑，资源的恢复可以简化为下面的计算公式
$$
U' = (1 - \frac{T_2 - T_1}{24\textit{hours}}) * U + u
$$
在这个公式中，给定两个时间节点$T_2 > T_1$，用户在$T_1$使用$U$资源，在$T_2$使用$u$资源，那么当前的已使用资源为$U'$。假设$T_2 - T_1 = 8 \textit{hours}$的话，那么在这个时间点剩余资源为$U' = \frac{2}{3} * U + u$。

对于开发者来说，一般不需要关注这一段逻辑。可以直接使用API`wallet/getaccountresource`获取指定账号下的资源余量，并返回如下的参数：

 - `freeNetUsed` / `freeNetLimit` 为免费带宽的用量和总量。
 - `NetUsed` / `NetLimit` 为当前用户质押获得的带宽用量和总量。
 - `TotalNetLimit`为全网可通过质押获得的带宽总量。
 - `TotalNetWeight`为全网质押获得带宽的TRX数量。
 - `EnergyUsed` / `EnergyLimit`为当前用户质押获得的能量用量和总量。
 - `TotalEnergyLimit`为全网可通过质押获得的能量总量。
 - `TotalEnergyWeight`为全网质押获得能量的TRX数量。

通过这些参数，就可以判断当前有多少剩余能量可供使用了。

## 这里有一些示例

我选取了几个交易作为案例，以分析这些交易的资源消耗，让大家更好地了解资源的使用方式。

1. TRX: [c671ccfeb0f9c2dc1d2e325993387b41dbf113e89b8ed1d707b9b8960f8fc658](https://tronscan.org/#/transaction/c671ccfeb0f9c2dc1d2e325993387b41dbf113e89b8ed1d707b9b8960f8fc658)

    Alice向Bob的TRX转账使用了268带宽，Alice没有足够的能量，因此这笔交易需燃烧0.274 TRX。

1. TRX：[e99417978d4483205c19dd95c20b12da972cf7fbc5612ed4290c11ad2b70a680](https://tronscan.org/#/transaction/e99417978d4483205c19dd95c20b12da972cf7fbc5612ed4290c11ad2b70a680)
    
    Alice向Bob的TRX转账用掉了265带宽，Alice有足够的能量，因此无需燃烧TRX。

1. TRON_USDT: [442bd653923abc981194972ae2f5ae65cca26a46f88470863e11945cc8b34bc5](https://tronscan.org/#/transaction/442bd653923abc981194972ae2f5ae65cca26a46f88470863e11945cc8b34bc5)

    Alice向Bob的TRON_USDT转账需消耗354带宽。由于TRON_USDT是TRC20代币，还需用掉31,895能量。Alice没有足够的资源，因此这笔交易要燃烧13.39TRX。

1. Unstake: [0f61dcf27b4446d125e2d69cef7c36568f1dea6c3fe8d8505bb8a7be641ceac5](https://tronscan.org/#/transaction/0f61dcf27b4446d125e2d69cef7c36568f1dea6c3fe8d8505bb8a7be641ceac5)

    Alice取消代理给Bob的能量，消耗了274带宽，Alice没有足够的能量，因此这笔交易燃烧了0.274TRX。


## Tron的动态能量机制

在2022年年底，Tron网络通过[TIP-491](https://github.com/tronprotocol/tips/blob/master/tip-491.md)提案开启了动态能量模型。动态能量机制使得部分热门合约的交易消耗能量显著上升，且不会影响到其他合约。[Tronscan](https://tronscan.io/#/data/charts/contracts/top-contracts)的数据显示，TRON_USDT消耗全网超过90%的能量。Tron开发者称，增加热门合约的能量消耗有助于减少低价值交易，并减少拥堵情况，对于Tron上的dApp环境有所提升。

动态能量机制引入了三个新的参数以对能量的增长进行控制

 - `threshold`是对于某个合约的动态能量启用阈值。若在当前维护周期（6小时）内合约总消耗量超过此阈值，下一个维护周期内就会提升动态能量的累加比例。当前网络设定`threshold = 3,000,000,000`。
 - `increase_factor`是对于动态能量的增长比例系数，单位为基点。当前网络设定`increase_factor = 2000`，即每个维护周期增长20%。此外，还有一个联动参数`decrease_factor`为`increase_factor / 4`是对于
 - `max_factor`规定了`increase_factor`累加的最大系数，即动态能量增长的倍率不能超过此参数，单位为基点。当前网络设定为`max_factor = 12,000`，即最大增长系数为120%。


## Stake 2.0的资源授权机制

## 资源模型的意义

## 小结


1. tip157 freeze in tvm https://github.com/tronprotocol/tips/blob/master/tip-157.md
1. tip467 stake 2.0 https://github.com/tronprotocol/tips/issues/467
1. enable stake 2.0 https://github.com/tronprotocol/tips/issues/519
1. 波场动态能量模型分析 https://zhuanlan.zhihu.com/p/112148935
1. 波场费用模型 https://github.com/tronprotocol/documentation/blob/master/中文文档/波场协议/波场费用模型.md


. 简介

Tron波场网络的介绍
本文的目的和结构
II. Tron的资源模型

资源的定义和种类
资源的获取方式
资源的使用方式
资源的限制和管理
III. 动态能量机制

能量和带宽的概念和作用
能量和带宽的交换规则
能量和带宽的消耗和恢复
IV. Stake 2.0的资源授权机制

节点和账户的角色和权限
节点和账户的资源授权方式
节点和账户的资源使用和管理
V. 经济意义的探讨

Tron资源模型对经济的影响
节点和用户的收益和成本
资源的分配和平衡
VI. 项目实践中的经验和建议

Tron Stake 2.0项目的背景和挑战
优化方案的设计和实现
涉及的技术和工具
VII. 总结

Tron资源模型的特点和优劣
未来的发展和前景
对Tron开发者和用户的建议和展望