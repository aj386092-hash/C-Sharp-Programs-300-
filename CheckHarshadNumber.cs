using System;

class CheckHarshadNumber {
    static void Main() {
        int n = 18, sum = 0, temp = n;

        while (temp > 0) {
            sum += temp % 10;
            temp /= 10;
        }

        Console.WriteLine(n % sum == 0);
    }
}