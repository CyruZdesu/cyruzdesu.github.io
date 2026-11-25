# Computational Complexity
Computational complexity measures the growth trend in the computational resources required to execute an algorithm as the input size $n$ tends to infinity. The concept can be divided into 2 part, **Time Complexity** and **Space Complexity**.
## 1. Asymptotic Notations
To describe the increasement of variable when the independent variable tend to infinity, we use asymptotic notations to capture the limiting behavior. Common asymptotic notations include:
* $O$ Asymptotic Upper Bound\
representing the maximum consumption in the worst cases.
* $\Omega$ Asymptotic Lower Bound\
representing the theoretical minimum minimum barrier required to solve the problem.
* $\Theta$ Asymptotically Tight Bound\
$\Theta$ exists if and only if the upper and lower bounds share the same order of growth i.e.  $f(n) = O(g(n))$ and $f(n) = \Omega(g(n))$ $\iff$ $f(n) = \Theta(g(n))$
* $o\ and \ \omega$ non-tight bounds
    * **$o$**: Strictly slower growth than the bound, meaning $\lim_{n \to \infty} \frac{f(n)}{g(n)} = 0$.
    * **$\omega$**: Strictly faster growth than the bound, meaning $\lim_{n \to \infty} \frac{f(n)}{g(n)} = \infty$.

- 关于上下界：有两个视角，分别针对一个**问题**以及解决它的**具体算法**：
  - **对于算法 $A$：** $O(f(n))$ 表示算法在所有输入下运行消耗的上界（绝不超过，通常由最坏情况决定）；$\Omega(g(n))$ 表示运行消耗的下界（绝不低于，通常由最好情况决定）。
  - **对于问题 $P$：** $O(f(n))$ 表示现有最优算法的上界（即人类目前已能保证在多少消耗内一定能解决它）；$\Omega(g(n))$ 表示理论下界（即无论什么算法，在最坏情况下理论上至少要消耗多少才能保证解决它）。

    若记当前已知的最优算法为 $B$，任意算法为 $A$，则一定存在以下关系（方便理解直接将对象放进括号里，非严格数学写法）：

    $$\Omega(P) \le O(P) = O(B) \le O(A)$$

    同时，对于任意具体算法自身，必有 $\Omega(A) \le O(A)$（注意：当上下界同阶时取等号，如归并排序）。

    对于特定算法，其最好情况下的下界可能极小（例如在有序数组中用二分法找数，最好情况第一次就猜中，耗时为 $\Theta(1)$，最坏情况为 $\Theta(\log n)$，因此其整体耗时落在 $\Omega(1)$ 到 $O(\log n)$ 之间）。
* Which one to choose?



## 2. Common Time Complexity Gradients

Ranked from slowest to fastest growth rate:

| Complexity Class | Terminology | Canonical Algorithms / Scenarios | Operations at $n = 10^6$ |
| --- | --- | --- | --- |
| $O(1)$ | Constant | Array index lookups, collision-free hash map queries | $\approx 1$ |
| $O(\log n)$ | Logarithmic | Binary search, balanced BST operations (AVL / Red-Black) | $\approx 20$ |
| $O(n)$ | Linear | Linear scan, single-pass filtering, counting sort | $\approx 10^6$ |
| $O(n \log n)$ | Linearithmic | Merge Sort, Heap Sort, QuickSort (average case) | $\approx 2 \times 10^7$ |
| $O(n^2)$ | Quadratic | Bubble Sort, Selection Sort, nested double loops | $\approx 10^{12}$ (Impractical on single CPUs) |
| $O(n^3)$ | Cubic | Standard matrix multiplication, Floyd-Warshall algorithm | $\approx 10^{18}$ |
| $O(2^n)$ | Exponential | Enumerating all subsets, Towers of Hanoi recursion | Combinatorial explosion ($n > 50$ is intractable) |
| $O(n!)$ | Factorial | Brute-force Traveling Salesperson Problem (TSP) | Immediate failure ($n > 20$ is intractable) |

> **Cobham's Thesis**: Problems solvable within polynomial time ($O(n^k)$ for some constant $k$) are considered computationally **tractable**. Once an algorithm's complexity enters super-polynomial territory (exponential or factorial), small increases in $n$ trigger combinatorial explosion.

## 3. [To be continued]

## Appendix: Why this chapter?
Everytime I ask AI for help in CS field especially in algorithm design/introduce, I can always find some note like `n(o)`. Seemingly this is a quite common notation in magnitude calculations. So I decide to finish this part before any advanced knowlegde.