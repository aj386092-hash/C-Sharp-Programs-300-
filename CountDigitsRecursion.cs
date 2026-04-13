using System;

class CountDigitsRecursion {
    static int Count(int n) {
        if (n == 0) return 0;
        return 1 + Count(n / 10);
    }

    static void Main() {
        Console.WriteLine(Count(12345));
    }
}