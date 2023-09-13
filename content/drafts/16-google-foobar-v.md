Title: 解决Foobar挑战（四）
Slug: foobar-v
Category: MISC
Date: 2023-09-07 21:00
Summary: 接上回书，我们来到了Foobar挑战的第四层，题目越来越困难了。
Status: draft



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

跟之前的套路一样，首先题目先给出了一个冗长的