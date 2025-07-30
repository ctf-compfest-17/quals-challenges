from z3 import *

solver = Optimize()

inp = [BitVec(f'inp_{i}', 8) for i in range(56)]

for i in range(56):
    solver.add(inp[i] >= 49)
    solver.add(inp[i] <= 122)

from string import punctuation

for p in punctuation:
    for i in range(56):
        solver.add(inp[i] != ord(p))

# Add the valid constraints from the input (filtering out syntax errors)
solver.add_soft( ((inp[29] | inp[55]) - (inp[29]  & inp[55])) == 3)
# case 1
solver.add(inp[42] == 89)
solver.add_soft( ((inp[36] & inp[44]) + (inp[36]  | inp[44])) == 236)
# case 1
solver.add(inp[43] == 70)
solver.add_soft( ((inp[33] | inp[49]) - (inp[33]  & inp[49])) == 80)
solver.add_soft( ((inp[18] | inp[23]) - (inp[18]  & inp[23])) == 24)
# case 1
solver.add(inp[46] == 55)
# case 1
solver.add(inp[2] == 69)
solver.add_soft( ((inp[47] | inp[3]) - (inp[47]  & inp[3])) == 19)
# case 2
solver.add(inp[27] == 49)
solver.add(inp[31] == inp[16])
solver.add_soft( ((inp[17] & inp[21]) + (inp[17]  | inp[21])) == 132)
solver.add_soft( ((inp[25] & inp[54]) + (inp[25]  | inp[54])) == 208)
solver.add_soft( ((inp[30] & inp[6]) + (inp[30]  | inp[6])) == 164)
solver.add_soft( ((inp[48] & inp[39]) + (inp[48]  | inp[39])) == 179)
# case 1
solver.add(inp[1] == 74)
# case 1
solver.add(inp[10] == 49)
solver.add_soft( ((inp[40] | inp[38]) - (inp[40]  & inp[38])) == 31)
solver.add_soft( ((inp[35] | inp[11]) - (inp[35]  & inp[11])) == 18)
solver.add_soft( ((inp[37] & inp[24]) + (inp[37]  | inp[24])) == 121)
# case 1
solver.add(inp[15] == 68)
solver.add_soft( ((inp[41] | inp[7]) - (inp[41]  & inp[7])) == 86)
solver.add_soft( ((inp[45] & inp[0]) + (inp[45] | inp[0])) == 166)
# case 1
solver.add(inp[23] == 112)
solver.add_soft( ((inp[38] & inp[8]) + (inp[38]  | inp[8])) == 200)
solver.add_soft( ((inp[40] | inp[30]) - (inp[40]  & inp[30])) == 40)
# case 1
solver.add(inp[38] == 88)
solver.add_soft( ((inp[24] | inp[14]) - (inp[24]  & inp[14])) == 89)
# case 1
solver.add(inp[53] == 81)
# case 1
solver.add(inp[19] == 105)
# case 1
solver.add(inp[55] == 71)
solver.add_soft( ((inp[8] | inp[32]) - (inp[8]  & inp[32])) == 70)
# case 1
solver.add(inp[14] == 109)
solver.add_soft( ((inp[53] & inp[5]) + (inp[53]  | inp[5])) == 157)
solver.add_soft( ((inp[52] & inp[40]) + (inp[52]  | inp[40])) == 137)
solver.add_soft( ((inp[30] & inp[18]) + (inp[30] | inp[18])) == 215)
solver.add_soft( ((inp[25] | inp[51]) - (inp[25]  & inp[51])) == 91)
solver.add_soft( ((inp[30] | inp[8]) - (inp[30]  & inp[8])) == 31)
solver.add_soft( ((inp[53] | inp[34]) - (inp[53]  & inp[34])) == 101)
solver.add_soft( ((inp[43] & inp[11]) + (inp[43]  | inp[11])) == 142)
solver.add_soft( ((inp[0] & inp[14]) + (inp[0]  | inp[14])) == 163)
solver.add_soft( ((inp[48] & inp[44]) + (inp[48]  | inp[44])) == 226)
solver.add_soft( ((inp[5] & inp[45]) + (inp[5]  | inp[45])) == 188)
solver.add_soft( ((inp[13] & inp[40]) + (inp[13]  | inp[40])) == 191)
solver.add_soft( ((inp[21] | inp[45]) - (inp[21]  & inp[45])) == 32)
# case 1
solver.add(inp[7] == 51)
# case 1
solver.add(inp[1] == 74)
solver.add_soft( ((inp[8] & inp[32]) + (inp[8]  | inp[32])) == 166)
# case 1
solver.add(inp[23] == 112)
solver.add_soft( ((inp[26] & inp[1]) + (inp[26]  | inp[1])) == 163)
solver.add_soft( ((inp[30] | inp[9]) - (inp[30]  & inp[9])) == 53)
solver.add_soft( ((inp[55] | inp[28]) - (inp[55] & inp[28])) == 62)
solver.add_soft( ((inp[10] & inp[37]) + (inp[10]  | inp[37])) == 118)
solver.add_soft( ((inp[11] & inp[35]) + (inp[11]  | inp[35])) == 162)
# case 1
solver.add(inp[20] == 116)
solver.add_soft( ((inp[18] | inp[9]) - (inp[18]  & inp[9])) == 50)
# case 1
solver.add(inp[18] == 104)
solver.add_soft( ((inp[37] | inp[52]) - (inp[37]  & inp[52])) == 7)
solver.add_soft( ((inp[35] & inp[43]) + (inp[35]  | inp[43])) == 160)
# case 1
solver.add(inp[17] == 52)
# case 1
solver.add(inp[3] == 100)
# case 1
solver.add(inp[21] == 80)
# case 1
solver.add(inp[44] == 118)
solver.add_soft( ((inp[24] & inp[53]) + (inp[24]  | inp[53])) == 133)
solver.add_soft( ((inp[32] | inp[41]) - (inp[32]  & inp[41])) == 83)
# case 2
solver.add(inp[37] == 69)
solver.add_soft( ((inp[49] & inp[45]) + (inp[49] | inp[45])) == 163)
# case 1
solver.add(inp[50] == 65)
# case 1
solver.add(inp[52] == 66)
solver.add_soft( ((inp[27] & inp[40]) + (inp[27]  | inp[40])) == 120)
solver.add_soft( ((inp[20] & inp[52]) + (inp[20]  | inp[52])) == 182)
solver.add_soft( ((inp[21] & inp[30]) + (inp[21]  | inp[30])) == 191)
solver.add_soft( ((inp[19] | inp[12]) - (inp[19]  & inp[12])) == 44)
# case 2
solver.add(inp[3] == 100)
solver.add_soft( ((inp[6] | inp[32]) - (inp[6] & inp[32])) == 3)
# case 1
solver.add(inp[23] == 112)
solver.add_soft( ((inp[27] | inp[3]) - (inp[27]  & inp[3])) == 85)
# case 1
solver.add(inp[37] == 69)
# case 1
solver.add(inp[37] == 69)
# case 1
solver.add(inp[1] == 74)
solver.add_soft( ((inp[33] & inp[52]) + (inp[33]  | inp[52])) == 165)
solver.add_soft( ((inp[48] & inp[27]) + (inp[48]  | inp[27])) == 157)
# case 1
solver.add(inp[54] == 110)
solver.add_soft( ((inp[43] & inp[29]) + (inp[43]  | inp[29])) == 138)
# case 1
solver.add(inp[23] == 112)
solver.add_soft( ((inp[53] | inp[14]) - (inp[53]  & inp[14])) == 60)
solver.add_soft( ((inp[5] & inp[25]) + (inp[5]  | inp[25])) == 174)
# case 1
solver.add(inp[55] == 71)
solver.add_soft( ((inp[54] & inp[31]) + (inp[54]  | inp[31])) == 163)
solver.add_soft( ((inp[12] | inp[14]) - (inp[12]  & inp[14])) == 40)
solver.add_soft( ((inp[7] & inp[9]) + (inp[7]  | inp[9])) == 141)
solver.add_soft( ((inp[23] & inp[31]) + (inp[23]  | inp[31])) == 165)
# case 1
solver.add(inp[39] == 71)
solver.add_soft( ((inp[33] & inp[39]) + (inp[33]  | inp[39])) == 170)
solver.add_soft( ((inp[25] | inp[16]) - (inp[25]  & inp[16])) == 87)
solver.add_soft( ((inp[22] & inp[39]) + (inp[22]  | inp[39])) == 145)
solver.add_soft( ((inp[22] & inp[26]) + (inp[22]  | inp[26])) == 163)
solver.add_soft( ((inp[1] & inp[38]) + (inp[1]  | inp[38])) == 162)
solver.add_soft( ((inp[12] | inp[35]) - (inp[12]  & inp[35])) == 31)
solver.add_soft( ((inp[32] | inp[3]) - (inp[32]  & inp[3])) == 82)
solver.add_soft( ((inp[8] & inp[0]) + (inp[8]  | inp[0])) == 166)
solver.add_soft( ((inp[21] | inp[41]) - (inp[21]  & inp[41])) == 53)
# case 2
solver.add(inp[10] == 49)
solver.add_soft( ((inp[6] | inp[26]) - (inp[6] & inp[26])) == 108)



result = solver.check()

# print(solver.model())


model = solver.model()


# xor_key dari binary
xor_key = bytes([117,5,8,52,7,9,102,103,65,109,74,33,49,77,50,55,88,0,26,94,43,50,63,71,107,3,53,66,73,27,25,6,68,26,107,62,66,43,63,116,53,85,44,115,41,19,84,21,95,10,113,91,113,101,88,58])
solution = []
for i in range(56):
    val = model[inp[i]]
    if val is not None:
        solution.append(int(str(val)))
    else:
        solution.append(0)  
pwd = ''.join(chr(c) for c in solution)

from pwn import xor
print('pwd : ', pwd.encode())
print('flag: ', xor(xor_key, pwd.encode()))
