# Artificial Intelligence - Report

**Name:** Kars van Velzen

**Student number:** s0223956



## (1) (Un)Informed Search - Discuss heuristics

**Describe your heuristic for question 6:**

- I consider the manhattan distance to corners Pacman didn't yet visit. Then I take the maximum distance to these corners I considered. 

- **Admissibility:** The longest distance to a corner Pacman did not yet visit, is a minimum distance that Pacman would always need to travel to pass by the other corner(s).
- **Consistency:** The heuristic is consistent because the next heuristic value doesn't decrease for the first 3 corner-visits (meaning that h(i) - h(i+1) is negative, thus less than the cost 1). 



**Describe your heuristic for question 7:**

- I take the maximum (manhattan) distance between 2 coins added with the minimum (manhattan) distance from pacman to one of these coins. (2 Edge cases exists when there are less than 2 coins, see code)

- **Admissibility:** It is admissible since Pacman would always at least need to travel this distance to reach the coins.
- **Consistency:** Considering at least 3 coins, the heuristic value doesn't drop too hard when 1 gets eaten.  



## (3) Constraint Satisfaction Problems - Forward Checking

Number of calls for n=50 when...

|          | CSP::selectVariable | CSP::orderDomain | Both       |
|----------|---------------------|------------------|------------|
| Active   | 196                 | 346 - 13 985     | 198        |
| Disabled | 229 - 10k           | 196              | 229 - 60+k |

**Explain why these functions make the algorithm faster/slower:**

selectVariable / MRV is quite obvious that it make the algorithm faster; You're narrowing down the options for each variable very quickly. Thus, you can decide earlier on what is or isn't successful. 

orderDomain / LCV is not so useful. I suspect because choosing random variables (no MRV) has a too high impact. 
LCV seems more useful on bigger problems but requires more computational power. We're explicitly keeping value positions as open as possible, providing more choices so we would have more options in succeeding. However, I suspect that we're opening up too many options so it takes longer to choose.  
