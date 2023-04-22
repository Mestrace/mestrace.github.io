Title: 解决Foobar挑战（二）
Slug: foobar-iii
Category: MISC
Date: 2023-04-22 22:00:00
Summary: 接上回书，我们来到了Foobar挑战的第三层。每一层都比上一层更加困难。这篇文章给出了Foobar Level 3 的三道题 Queue To Do， Hey, Fuel Injection Perfection 和 Doomsday Fuel 的解题思路和python代码。这一层要求我们掌握一些位运算，贪心算法，线性代数和概率论的知识。

[解决Foobar挑战（一）]({filename}/articles/11-foobar-challenge-ii.md)

接上回书，我们来到了Foobar挑战的第三层。每一层都比上一层更加困难。不多废话了，我们直接来做题。

## Queue To Do

> You're almost ready to make your move to destroy the LAMBCHOP doomsday device, but the security checkpoints that guard the underlying systems of the LAMBCHOP are going to be a problem. You were able to take one down without tripping any alarms, which is great! Except that as Commander Lambda's assistant, you've learned that the checkpoints are about to come under automated review, which means that your sabotage will be discovered and your cover blown -- unless you can trick the automated review system.
> 
> To trick the system, you'll need to write a program to return the same security checksum that the bunny trainers would have after they would have checked all the workers through. Fortunately, Commander Lambda's desire for efficiency won't allow for hours-long lines, so the trainers at the checkpoint have found ways to quicken the pass-through rate. Instead of checking each and every worker coming through, the bunny trainers instead go over everyone in line while noting their worker IDs, then allow the line to fill back up. Once they've done that they go over the line again, this time leaving off the last worker. They continue doing this, leaving off one more worker from the line each time but recording the worker IDs of those they do check, until they skip the entire line, at which point they XOR the IDs of all the workers they noted into a checksum and then take off for lunch. Fortunately, the workers' orderly nature causes them to always line up in numerical order without any gaps.
> 
> For example, if the first worker in line has ID 0 and the security checkpoint line holds three workers, the process would look like this:
> 
> 0 1 2 /
> 
> 3 4 / 5
> 
> 6 / 7 8
> 
> where the trainers' XOR (^) checksum is 0^1^2^3^4^6 == 2.
> 
> Likewise, if the first worker has ID 17 and the checkpoint holds four workers, > the process would look like:
> 
> 17 18 19 20 /
> 
> 21 22 23 / 24
> 
> 25 26 / 27 28
> 
> 29 / 30 31 32
> 
> which produces the checksum 17^18^19^20^21^22^23^25^26^29 == 14.
> 
> All worker IDs (including the first worker) are between 0 and 2000000000 inclusive, and the checkpoint line will always be at least 1 worker long.
> 
> With this information, write a function solution(start, length) that will cover for the missing security checkpoint by outputting the same checksum the trainers would normally submit before lunch. You have just enough time to find out the ID of the first worker to be checked (start) and the length of the line (length) before the automatic review occurs, so your program must generate the proper checksum with just those two values.
> 
> Input: solution.solution(0, 3)
>
> Output: 2
> 
> Input: solution.solution(17, 4)
>
> Output: 14

每个工人有一个数字ID且所有工人的数字ID都为连续的。他们排成长度为`n`的方阵接受安全系统的检查。安全系统的检查的算法是抽查一部分工人的ID进行异或计算校验和：第一行选择前`n`个工人的ID进行异或（XOR），第二行选择前`n - 1`个工人的ID进行异或操作，以此类推直到`n == 0`。给定一个开始的ID`start`，和每一行的长度`length`，求这个方阵的校验和。

虽然可以直接进行模拟，但是实际上这道题是有规律可循的。在[Leetcode 2588题解]({filename}/leetcode/2588-count-the-number-of-beautiful-subarrays.md)我们分析了XOR的一些性质。其中，单位元性质告诉我们任何数字`X XOR X = 0`，`X XOR 0 = X`。如果我们想要求连续数列的异或`XOR([i:j])`的时候，实际上等价于`XOR([1:j]) ^ XOR([1:i - 1])`。而当我们计算一个连续数列的异或的时候，我们可以找到一个规律。就拿`[1,n]`来举个例子：
```
n:      1  2  3  4  5  6  7  8  9  10  11  12 ...
XOR(n): 1  3  0  4  1  7  0  8  1  11  0  12 ...
```
在这里我们发现，`XOR([1:n])`的结果是根据`n % 4`来以一种规律进行循环的，因此可以快速求得所有的校验和。

### 代码

```python
def xor(n):
    rem = n % 4
    if rem == 0:
        return n
    elif rem == 1:
        return 1
    elif rem == 2:
        return n + 1
    else:  # rem == 3
        return 0

def solution(start, length):
    checksum = 0

    for i in range(length):
        first = start + i * length
        last = first + length - i - 1
        checksum ^= xor(last) ^ xor(first - 1)

    return checksum
```

## Fuel Injection Perfection

> Commander Lambda has asked for your help to refine the automatic quantum antimatter fuel injection system for the LAMBCHOP doomsday device. It's a great chance for you to get a closer look at the LAMBCHOP -- and maybe sneak in a bit of sabotage while you're at it -- so you took the job gladly. 
> 
> Quantum antimatter fuel comes in small pellets, which is convenient since the many moving parts of the LAMBCHOP each need to be fed fuel one pellet at a time. However, minions dump pellets in bulk into the fuel intake. You need to figure out the most efficient way to sort and shift the pellets down to a single pellet at a time. 
> 
> The fuel control mechanisms have three operations: 
> 
> 1. Add one fuel pellet
> 2. Remove one fuel pellet
> 3. Divide the entire group of fuel pellets by 2 (due to the destructive energy released when a quantum antimatter pellet is cut in half, the safety controls will only allow this to happen if there is an even number of pellets)
> 
> Write a function called solution(n) which takes a positive integer as a string and returns the minimum number of operations needed to transform the number of pellets to 1. The fuel intake control panel can only display a number up to 309 digits long, so there won't ever be more pellets than you can express in that many digits.
> 
> For example:
>
> solution(4) returns 2: 4 -> 2 -> 1
>
> solution(15) returns 5: 15 -> 16 -> 8 -> 4 -> 2 -> 1


给定`n`个颗粒的量子反物质燃料（？），我们要把他减少到`1`。我们可以有三种操作：增加一个颗粒，减少一个颗粒，和将颗粒总数除`2`（仅当可以整除的时候）。求最少需要多少个操作数才可以完成。

一开始我想的是`DP`来计算最小可能的操作数量，但是一看数据范围`1e308`就疯狂挠头。无论如何我们不能把所有`n`对应的最小操作数量都存下来吧。但是这道题还是有一些`DP`的性质在的，因此我们考虑是否能有某种贪心的方式进行计算。

我们可以观察得到，要尽可能多的进行第三个操作，也就是整除`2`，才能最快将`n`减少到`1`。而前两个操作`+/- 1`都是为了第三个操作服务的。实际上，要想一个数字能够整除2，我们应该看这个数字最后一个比特是否为`0`。而加减操作则能让我们在最后一个比特位为`1`的时候把它变成`0`。我们只用最后几个bit来举个例子：假如一个数字为`...000001`的话，我们应该减`1`才可以让他更快变为`1`；而假如一个数字为`...11111`的话，我们应该加`1`才能让他更快变为`1`。这里我们只要贪心的看最后两位是`01`或者`11`就可以。一个特殊情况是`n = 3 = 0b11`的时候，我们应该减一并位移得到最终结果。

### 代码

```python
def solution(n):
    n = int(n)
    operations = 0

    while n != 1:
        # is even, end is 0
        if n % 2 == 0:
            n //= 2
        # end is 01 or special case is '11'
        elif n == 3 or n % 4 == 1:
            n -= 1
        # end is '11'
        else:
            n += 1
        operations += 1

    return operations
```

## Doomsday Fuel

> Making fuel for the LAMBCHOP's reactor core is a tricky process because of the exotic matter involved. It starts as raw ore, then during processing, begins randomly changing between forms, eventually reaching a stable form. There may be multiple stable forms that a sample could ultimately reach, not all of which are useful as fuel. 
>
> Commander Lambda has tasked you to help the scientists increase fuel creation efficiency by predicting the end state of a given ore sample. You have carefully studied the different structures that the ore can take and which transitions it undergoes. It appears that, while random, the probability of each structure transforming is fixed. That is, each time the ore is in 1 state, it has the same probabilities of entering the next state (which might be the same state).  You have recorded the observed transitions in a matrix. The others in the lab have hypothesized more exotic forms that the ore can become, but you haven't seen all of them.
> 
> Write a function solution(m) that takes an array of array of nonnegative ints representing how many times that state has gone to the next state and return an array of ints for each terminal state giving the exact probabilities of each terminal state, represented as the numerator for each state, then the denominator for all of them at the end and in simplest form. The matrix is at most 10 by 10. It is guaranteed that no matter which state the ore is in, there is a path from that state to a terminal state. That is, the processing will always eventually end in a stable state. The ore starts in state 0. The denominator will fit within a signed 32-bit integer during the calculation, as long as the fraction is simplified regularly. 
> 
> For example, consider the matrix m:
> 
> [
> 
>   [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
>
>   [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
>
>   [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
>
>   [0,0,0,0,0,0],  # s3 is terminal
>
>   [0,0,0,0,0,0],  # s4 is terminal
>
>   [0,0,0,0,0,0],  # s5 is terminal
>
> ]
>
> So, we can consider different paths to terminal states, such as:
> 
> s0 -> s1 -> s3
> 
> s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
> 
> s0 -> s1 -> s0 -> s5
> 
> Tracing the probabilities of each, we find that
> 
> s2 has probability 0
> 
> s3 has probability 3/14
> 
> s4 has probability 1/7
> 
> s5 has probability 9/14
> 
> So, putting that together, and making a common denominator, gives an answer in the form of
> 
> [s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is
> 
> [0, 3, 2, 9, 14].
>
> Input: solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]])
> 
> Output: [7, 6, 8, 21]
> 
> Input: solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
> 
> Output: [0, 3, 2, 9, 14]

给定一个`n x n`的矩阵`m`。其中，`m[i][j]`是矿石由状态`s_i`变到`s_j`的实验观察次数。矿石永远从状态`s_0`开始并在有限时间内最终变化到某个稳定态`s_t`上。要求最终转移到某个稳定态的概率。此外还要处理分母和分子的问题。

看到题目的时候我的心态是崩溃的。如果用DFS来做，状态可能有循环。此外我们不确定他什么时候收敛到最终态。但是看到概率和状态转移，感觉好像有一些熟悉的感觉。此外，题目还提到状态转移虽然是一个随机的过程，但是从一个状态转移到另一个状态的概率是固定的。这意味着，每个状态转移都是一个独立的过程，即转移到某个状态的概率只取决于上一个状态。借这些关键词，我很快搜索到了一个相关的东西：马尔科夫链。。。Google真有你的。。。

马尔科夫链（Markov chain）描述了一个独立的状态转移过程。即我们刚刚所说的，给定一系列状态，在状态和状态之间的随机过程的发生概率只取决于当前所处的状态。此外，它还有个儿子，吸收马尔科夫链（Absorbing Markov chain）。指的是在马尔科夫链的基础上，存在一些吸收状态（Absorbing state）。一旦状态转移进入了吸收状态，就会一直保持在吸收状态中。而对于在有限时间收敛的吸收马尔科夫链的各个状态转移到吸收状态的期望概率，可以通过一系列矩阵计算得出。

首先，我们通过给定的实验观察记录`m`可以计算出一个标准的马尔科夫链的状态转移概率矩阵。简单可知，`s_i -> s_j`的概率为`m[i][j] / sum(m[i])`。此外，对于`sum(m[i]) == 0`的情况，`i`则是一个吸收状态。因为在这个状态下，`s_i`不会移动到任何其他状态去，也自然没有实验观察现象。

接下来，我们要把概率矩阵转换成一个吸收马尔科夫链的标准转移矩阵，假设我们有`n`个吸收状态和`m`个非吸收状态，我们可以把状态转移矩阵的索引重写以变成下面的形式。

$$
P = \begin{bmatrix}
I_n & 0_{n \times m} \\
R_{m \times n} & Q_m
\end{bmatrix}
$$

其中

- 单位矩阵$I_n$代表了`n`个吸收状态互相转移的概率。
- 0矩阵$0_{n \times m}$代表了`n`个吸收状态转移到`m`个非吸收状态的概率。
- $R_{m \times n}$代表了`m`个非吸收状态转移到`n`个吸收状态的概率。
- $Q_m$代表了`m`个非吸收状态互相转移的概率。

经过有限次数的转移，我们最终可以转移到一个终态，可以表示为

$$
\bar{P} = \begin{bmatrix}
I_n & 0_{n\times m} \\
F_m R_{m \times n} & 0_m
\end{bmatrix}
$$

其中基本矩阵代表了由非吸收状态收敛到转移吸收状态的概率的乘数，可表示为

$$
F = (I - Q)^{-1}
$$

最后左下角的部分找到`s_0`所在的行，就是`s_0`转移到吸收状态的期望概率了。

等下，还没完。我们还要把结果转换为分数形式并输出。这里我们简单用`fractions`进行处理。计算所有分母的最小公倍数即可。

### 代码

```python
{!content/articles/code/foobar-iii-doomsday-fuel.py!}
```

## 小结

总的来说，第三层的难度提升得很快。特别是最后一题要求我们掌握马尔科夫链的相关计算和一些矩阵乘法的计算。还是相当的有挑战性的。完成这一章节之后，我还填入了自己的个人联系方式和LinkedIn页面。据网上说，可能会有recruiter直接联系我。不过目前看这个大环境，估计也只是遥不可及的梦想罢了（笑）。接下来还有两层挑战，让我们看看我到底能走多远把。

在研究第三题的过程中，这些资料对我有很大的帮助，你也可以看看：

- [Youtube - Markov Chains - Part 8 - Standard Form for Absorbing Markov Chains](https://youtu.be/BsOkOaB8SFk) 强烈建议看完Part 7，8 和 9，这会是你人生中花的最值的45分钟。
- [Lei Blog - 吸收马尔可夫链](https://www.cnblogs.com/guolei/p/3504931.html)