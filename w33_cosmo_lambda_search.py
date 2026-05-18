import math

target = math.log(1e-122) # ~ -280.92

V = 40
E = 240
alpha_inv = 137
phi = (1 + math.sqrt(5))/2

print("V + E =", V + E)
print("math.exp(-280) =", math.exp(-280))
print("math.exp(-(V + E)) =", math.exp(-(V + E)))
print("math.exp(- (V + E + 1)) =", math.exp(-(V+E+1)))

# Let's search for combinations around 280 to 281
primitives = [3, 4, 6, 7, 10, 12, 13, 15, 24, 27, 28, 40, 81, 137, 192, 240, 248, 384]
names = ['q','mu','q!','Phi6','Phi4','k','Phi3','g','f','q^q','T7','v','H1','alpha_inv','tom','E','E8','tau_O']

best = []
for i in range(len(primitives)):
    for j in range(len(primitives)):
        val1 = primitives[i] + primitives[j]
        if abs(val1 - 280.9) < 2:
            best.append(f"{names[i]} + {names[j]} = {val1}")
            
        for k in range(len(primitives)):
            val2 = primitives[i] + primitives[j] + primitives[k]
            if abs(val2 - 280.9) < 1:
                best.append(f"{names[i]} + {names[j]} + {names[k]} = {val2}")
                
print(set(best))
