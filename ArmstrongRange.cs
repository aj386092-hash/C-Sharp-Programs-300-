using System;

class ArmstrongRange {
    static void Main() {
        for (int i = 100; i <= 500; i++) {
            int temp = i, sum = 0;
            while (temp > 0) {
                int d = temp % 10;
                sum += d * d * d;
                temp /= 10;
            }
            if (sum == i) Console.Write(i + " ");
        }
    }
}