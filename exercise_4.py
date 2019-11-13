#!/usr/bin/env python
# coding: utf-8

# The palindrome problem is a common one in programming. There are many ways to solve it. We decided to use the concept of dynaminc programming which breaks the main problem into a collection of simpler ones. It also stores the solutions of subproblems so they do not have to be computed many times.

# In[2]:


str=input()
n=len(str)

#We create a two dimentional array (size: nxn) filled with zeros. We will fill its cells with the length of the 
#longest palindrome. The i-th row and j-th column denotes all the letters from index i to j of the string
table = [[0 for _ in range(n)] for _ in range(n)]

#The substrings on the diagonal of the table denote simply one letter which always is a palindrome of length 1
for i in range(n):
    table[i][i] = 1

#Now we consider substrings of length>=2    
#We take the penultimate letter, compare it with the last one, then we take the pre-penultimate letter and compare
#it with the penultimate and the ultimate etc. 
#If the two letters are the same, we put into a corresponding cell a value of the "middle" cell (where the length 
#of palindromic substring between first and last considered letters is stored) plus 2 because of the first and 
#last letters in a considered substring. 

#If the two letters are not the same, the maximum length palindorme is just the maximum of two "previous" 
#substrings (one character shorter, for example for characters in indexes 0-5 we consider characters in 
#indexs 0-4 and 1-5)
for i in range(n-1, -1, -1):
    for j in range(i+1, n):                    
        if str[i]==str[j]:
            table[i][j] = table[i+1][j-1]+2
        else:
            table[i][j] = max(table[i][j-1], table[i+1][j])
            
#We do not take into account substrings on the left of the diagonal because it means we consider substrings that
#are read backwords
#The maximum length palindrome will be always the first row and the last column (it results of the code)
print(table[0][-1])

