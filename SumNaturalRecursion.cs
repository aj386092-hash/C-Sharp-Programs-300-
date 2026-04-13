using System;

class SumNaturalRecursion {
    static int Sum(int n) {
        if (n == 0) return 0;
        return n + Sum(n - 1);
    }

    static void Main() {
        Console.WriteLine(Sum(10));
    }
}