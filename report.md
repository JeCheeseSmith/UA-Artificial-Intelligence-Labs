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

|          | CSP::selectVariable | CSP::orderDomain |
| -------- | ------------------- | ---------------- |
| Active   | [number here]       | [number here]    |
| Disabled | [number here]       | [number here]    |



**Explain why these functions make the algorithm faster/slower:**

[short answer here]

