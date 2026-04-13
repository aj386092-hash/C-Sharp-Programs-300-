using System;

class CountConsonants {
    static void Main() {
        string str = "programming";
        int count = 0;

        foreach (char c in str) {
            if ("aeiou".IndexOf(c) == -1)
                count++;
        }

        Console.WriteLine(count);
    }
}