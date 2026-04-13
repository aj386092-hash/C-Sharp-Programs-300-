using System;

class SwapWithoutTemp {
    static void Main() {
        int a = 5, b = 10;

        a = a + b;
        b = a - b;
        a = a - b;

        Console.WriteLine(a + " " + b);
    }
}