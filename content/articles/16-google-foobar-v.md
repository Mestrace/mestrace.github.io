Title: 解决Foobar挑战（四）- 终篇
Slug: foobar-v
Category: Computer Science
Date: 2023-09-30 21:00
Modified: 2023-10-09 22:00
Tags: Google Foobar
Summary: 接上回书，我们来到了Foobar挑战的第五层，题目越来越困难了。本题主要涉及一些数论和组合数学的知识点。

Foobar系列已经全部完成了，你可以通过以下目录访问！

- [解决Foobar挑战（一）]({filename}/articles/11-foobar-challenge-ii.md)
- [解决Foobar挑战（二）]({filename}/articles/12-foobar-challenge-iii.md)
- [解决Foobar挑战（三）]({filename}/articles/13-foobar-challenge-iv.md)
- 解决Foobar挑战（四）- 终篇

## Dodge the Lasers!
```
foobar:~/ mestrace$ request
Requesting challenge...
Huzzah! The famous pilots Luke Skybunny and Jyn Erbun managed to hijack a pair of Commander Lambda's starfighters and are laying down cover fire for the bunnies' escape pods. You give them a wing salute on your way past.

New challenge "Dodge the Lasers!" added to your home folder.
Time to solve: 528 hours.
```

看到这个528小时（22天）的限时我就觉得隐隐约约有些不对劲……


<details markdown="1">
  <summary>题目</summary>
Oh no! You've managed to escape Commander Lambda's collapsing space station in an escape pod with the rescued bunny workers - but Commander Lambda isnt about to let you get away that easily. Lambda sent an elite fighter pilot squadron after you -- and they've opened fire!

Fortunately, you know something important about the ships trying to shoot you down. Back when you were still Lambda's assistant, the Commander asked you to help program the aiming mechanisms for the starfighters. They undergo rigorous testing procedures, but you were still able to slip in a subtle bug. The software works as a time step simulation: if it is tracking a target that is accelerating away at 45 degrees, the software will consider the targets acceleration to be equal to the square root of 2, adding the calculated result to the targets end velocity at each timestep. However, thanks to your bug, instead of storing the result with proper precision, it will be truncated to an integer before adding the new velocity to your current position.  This means that instead of having your correct position, the targeting software will erringly report your position as sum(i=1..n, floor(i*sqrt(2))) - not far enough off to fail Commander Lambdas testing, but enough that it might just save your life.

If you can quickly calculate the target of the starfighters' laser beams to know how far off they'll be, you can trick them into shooting an asteroid,
releasing dust, and concealing the rest of your escape.  Write a function solution(str_n) which, given the string representation of an integer n, returns the
sum of (floor(1*sqrt(2)) + floor(2*sqrt(2)) + ... + floor(n*sqrt(2))) as a string. That is, for every number i in the range 1 to n, it adds up all of the
integer portions of i*sqrt(2).

For example, if str_n was "5", the solution would be calculated as
floor(1*sqrt(2)) +
floor(2*sqrt(2)) +
floor(3*sqrt(2)) +
floor(4*sqrt(2)) +
floor(5*sqrt(2))
= 1+2+4+5+7 = 19
so the function would return "19".


str_n will be a positive integer between 1 and 10^100, inclusive. Since n can be very large (up to 101 digits!), using just sqrt(2) and a loop won't work. Sometimes, it's easier to take a step back and concentrate not on what you have in front of you, but on what you don't.
</details>

跟之前的套路一样，首先题目先给出了一个冗长的描述。其实主要意思是说计算 $S(n) = \sum_{i=1}^{n} \lfloor i\sqrt{2} \rfloor$。再搂一眼数据范围…… 嚯，好家伙，直接给了`1 <= n <= 10^100`的数据范围。明摆着用`for`循环解决不了。但我们还是可以用这个朴素方法来作为标准答案。

```python
def solution(s: str):
    n = int(s)
    s = 0
    for i in range(1, n + 1):
        s += int(i * sqrt(2))
    return str(s)
```

那么，接下来有没有什么办法能够让我大幅度减少以上算法的复杂度呢？经过一番搜索，我找到了这个[Beatty 序列](https://en.wikipedia.org/wiki/Beatty_sequence)！

Beatty-Rayleigh定理：若 $\alpha, \beta \in \mathbb{R}^+$，且 $\alpha, \beta \notin \mathbb{Q}$，使得
$\frac{1}{\alpha} + \frac{1}{\beta} = 1$，则有两个集合
$P = \left\{ \lfloor \alpha n \rfloor : n \in \mathbb{Z}^+ \right\}$ 和 $ Q = \left\{ \lfloor \beta n \rfloor : n \in \mathbb{Z}^+ \right\}$，且 $P$ 和 $Q$ 完整划分整个自然数集合
$P \cap Q = \emptyset$，以及 $P \cup Q = \mathbb{Z}^+$。

当$\alpha = \sqrt{2}$，$\beta=2 + \sqrt{2}$时，我们有

| i | 1 | 2 | 3  | 4  | 5  | 6  | 7  |
|---|---|---|----|----|----|----|----|
| $\lfloor \alpha i \rfloor$[ref][OEIS A001951](https://oeis.org/A001951)[/ref]| 0 | 1 | 2  | 4  | 5  | 7  | 8  |
| $\lfloor \beta i \rfloor$[ref][OEIS A001952](https://oeis.org/A001952)[/ref] | 3 | 6 | 10 | 13 | 17 | 20 | 23 |


<p align="center">
  <img src="{static}/images/where_sold.jpg" />
</p>

通过Beatty-Rayleigh定理反推，给定一个正整数 $n$，我们想要计算 $P_n$，则可以表示为 $\sum{P_n} = \sum{\mathcal{Z}} - \sum{Q_m}$。其中，$P_n$ 和 $Q_m$ 共同组成了自然数集合 ${1,2,3,...,\lfloor \alpha i \rfloor}$ 。需要注意的是，我们使用变量 $m$ 和 $n$ 分别代表前述两个集合的最大值。从上面的例子我们可以观察到，当`i`相同时，集合 $P$ 和 $Q$ 的最大值范围是不一样的，因此他们所圈选的自然数空间也不一样。我们可以通过计算 $m = \lfloor \alpha i \rfloor / \beta$ 来限制 $Q$ 的取值范围。接着我们就可以递归计算 $Q_m$。因为 $m$ 每次都会变小，我们期望他能够收敛到这个递归方程的基线条件，即 $m = 0$ 或者 $m = 1$ 。以下为代码实现。

```python
from math import sqrt

def sum_beatty_v2(n, alpha):
    if n == 0:
        return 0
    if n == 1:
        return int(alpha)
    
    beta = 1/(1 - 1/alpha)
    m = int(n * alpha)
    
    return m * (m + 1) // 2 - sum_beatty_v2(int(m / beta), beta)

def solution_v2(n):
    return str(sum_beatty_v2(int(n), sqrt(alpha)))
```

实现完成，现在让我们debug一下，打印出来每次递归的值看看吧！
```
> solution_v2("10")

10 1.4142135623730951
4 3.4142135623730945
9 1.4142135623730951
3 3.4142135623730945
7 1.4142135623730951
2 3.4142135623730945
4 1.4142135623730951
1 3.4142135623730945

'73'
```

每次递归的`n`是减小了，但数量级没变小，那么时间复杂度还是没有变化啊！不过，我们可以观察到，每次都是 $\alpha$ 和 $\beta$ 不停的在 $\sqrt 2$ 和 $2 + \sqrt 2$ 之间互换。每次在 $\alpha = \sqrt 2$ 的时候，`n`都会减半，如果我们能让 $\alpha = 2 + \sqrt 2$ 的量级变小就好了……

<p align="center">
  <img src="{static}/images/cong-tian-er-jiang.jpg" />
</p>

我们直接做一个展开，当 $\alpha = 2 + \sqrt 2$ 时，$P_n = {\lfloor 2 + \sqrt 2\rfloor, \lfloor 4 + 2\sqrt 2 \rfloor ,...,\lfloor n (2 + \sqrt 2)}$。如果我们把其中的整数项提出来，其实是不影响向下取整的结果的。

定理2: 若 $\alpha, \in \mathbb{R}^+$，$\alpha, \notin \mathbb{Q}$ ，且 $\alpha > 1$ ， $\beta = \alpha - 1$，则有两个集合
$P = \left\{ \lfloor \alpha n \rfloor : n \in \mathbb{Z}^+ \right\}$ 和 $ Q = \left\{ \lfloor \beta n \rfloor : n \in \mathbb{Z}^+ \right\}$，使得 $\sum_{P} = \sum_{i = 1}^n{i} + \sum_{Q}$。

我们可以利用这个定理来进一步化简我们的算法。

```python
from math import sqrt

def nsum(n):
    return n * (n + 1) // 2

def sum_beatty_v3(n, alpha):
    print(n)
    assert alpha >= 1
    if n < 1:
        return 0
    if n == 1:
        return 1
    
    n1 = int((alpha - 1) * n)
    result = nsum(n + n1) - 2 * nsum(n1) - sum_beatty_v3(n1, alpha)

    return result

def solution_v3(n):
    return str(sum_beatty_v3(int(n), sqrt(2)))
```

```
> solution_v3("1000")

1000
414
171
70
28
11
4
1

'707314'
```

从数学上的定义来说，我们似乎已经有一个完备的程序来计算这道题目的结果了。但我们可能忽略了一个重要的问题 ---- 浮点数精度问题。我们可以注意到，在上述程序中，我们一直使用一个`sqrt(2)`的浮点数来计算，但是当数据大小扩大到`10^100`的级别，使用浮点数会引起两个问题：随着数据范围的增大，浮点数的表示精度会下降，且乘法的算数精度会下降。最终这两者结合起来会引起我们算出来的结果不对。因此，我们要用精确的`sqrt(2)`表示。这里我用`decimal`和基本的浮点数生成了结果对比。

```python
import decimal

# Set the precision to a sufficiently high value
decimal.getcontext().prec = 200  # You can adjust the precision as needed

# Calculate sqrt(2)
sqrt_2 = decimal.Decimal(2).sqrt()

# Set the value of n
n = 100  # You can replace this with the desired value of n

# Calculate sqrt(2) * 10^n
result = sqrt_2 * (decimal.Decimal(10) ** n)

print(int(result))
```

```python
> print(sqrt_2_integer)
14142135623730950488016887242096980785696718753769480731766797379907324784621070388503875343276415727
> int((sqrt(2)) * (1e100))
14142135623730952214093017858547657902953555641438782124185842940740828094528952769132495248707026944
```

可以观察到，在第`15`位的时候已经有差别了。

考虑到我们其实只需要计算`sqrt(2) - 1`因此我们截取小数部分，并预计算到100位，最后使用整数乘法和除法计算以保存精度。

此外，别忘了Foobar采用的是Python2，因此一些语法需要额外处理。这里给出我的最终版本。

```python
msqrt = 4142135623730950488016887242096980785696718753769480731766797379907324784621070388503875343276415727

def get_n1(n):
    return msqrt * n // 10**100

def solution_v4(s):
    return str(sum_beatty_v4(long(s)))

def nsum(n):
    return n * (n + 1) // 2

def sum_beatty_v4(n):
    if n < 1:
        return 0
    if n == 1:
        return 1
    
    n1 = get_n1(n)
    
    return nsum(n + n1) - 2 * nsum(n1) - sum_beatty_v4(n1)
```

如果你对Beatty数列及相关概念感兴趣，我非常推荐阅读以下两篇文章：

- [Beatty序列与Wythoff博弈 ](https://www.cnblogs.com/emofunc/p/14892665.html)
- [捡石子游戏、 Wythoff 数表和一切的 Fibonacci 数列](http://www.matrix67.com/blog/archives/6784)

## Fin

提交完最后一题，我长舒了一口气。在熟悉的命令行里输入了`status`，却出现了新的谜题……

```

foobar:~/ mestrace$ status
You've completed all the levels!!

<encrypted>b'FkIAARECBhYeQlNOUkYEFwgEB1NeQUQGAgkfERMGFgBKRUlUVQQQEQgAHhEWRk9FSgAVEh0TFxZK\nRUlUVQgNBh8AFx0QDQZCQUVUFREJCgAbAB4RHBVERVdFVAEcDQwGBgAXU15BRBcMBxEdBhJERVdF\nVAcTBwZCQUVUEh0OREVXRVQDGw9CQhA='</encrypted>

For your *eyes* only!

Use the status command to repeat this message.
```
