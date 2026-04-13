using System;

class ReverseEachWord {
    static void Main() {
        string str = "Hello World";
        string[] words = str.Split(' ');

        foreach (string w in words) {
            char[] c = w.ToCharArray();
            Array.Reverse(c);
            Console.Write(new string(c) + " ");
        }
    }
}