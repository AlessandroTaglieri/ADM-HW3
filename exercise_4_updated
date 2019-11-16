# The palindrome problem is a common one in programming. There are many ways to solve it. We decided to use the concept of dynaminc programming which breaks the main problem into a collection of simpler ones. It also stores the solutions of subproblems so they do not have to be computed many times.
# Our solution is inspired by the following video: https://www.youtube.com/watch?v=_nCsPn7_OgI

inp=input()
l=len(inp)

#We create a two dimentional array (size: lxl) filled with zeros. We will fill its cells with the length of the 
#longest palindrome. The i-th row and j-th column denotes all the letters from index i to j of the string

table = [[0 for _ in range(l)] for _ in range(l)]

#The substrings on the diagonal of the table denote simply one letter which always is a palindrome of length 1 (The first if line denotes this parts)
#The next elif:
#We consider substrings of length>=2    
#We take the penultimate letter, compare it with the last one, then we take the pre-penultimate letter and compare
#it with the penultimate and the ultimate etc. 
#If the two letters are the same, we put into a corresponding cell a value of the "middle" cell (where the length 
#of palindromic substring between first and last considered letters is stored) plus 2 because of the first and 
#last letters in a considered substring. 
#The next elif:
#If the two letters are not the same, the maximum length palindorme is just the maximum of two "previous" 
#substrings (one character shorter, for example for characters in indexes 0-5 we consider characters in 
#indexs 0-4 and 1-5)
for i in range(l, -1, -1):
    for j in range(i, l):
        if i==j:
             table[i][j] = 1
        elif inp[i]==inp[j]:
            table[i][j] = table[i+1][j-1]+2
        elif inp[i]!=inp[j]:
            table[i][j] = max(table[i][j-1], table[i+1][j])
            
#We do not take into account substrings on the left of the diagonal because it means we consider substrings that
#are read backwords
#The maximum length palindrome will be always the first row and the last column (it results of the code)
maxpalindrome=table[0][-1]
print(maxpalindrome)

