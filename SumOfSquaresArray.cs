using System;

class SumOfSquaresArray {
    static void Main() {
        int[] arr = {1,2,3,4};
        int sum = 0;

        foreach (int i in arr)
            sum += i * i;

        Console.WriteLine(sum);
    }
}