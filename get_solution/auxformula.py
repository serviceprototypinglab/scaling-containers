from numpy import array, ndenumerate

matrix_2 = array([
    [
        [
            89.16724374,
            45.5318765193,
            43.7904612511,
            41.8832055032,
            42.0507290155,
            40.4489257663
        ],
        [
            71.6993230659,
            48.1122723985,
            40.0736481696,
            35.9154654562,
            36.0452770233,
            36.3544942796
        ]
    ],
    [
        [
            189.16724374,
            145.5318765193,
            143.7904612511,
            141.8832055032,
            142.0507290155,
            140.4489257663
        ],
        [
            171.6993230659,
            148.1122723985,
            140.0736481696,
            135.9154654562,
            136.0452770233,
            136.3544942796
        ]
    ]
])


# for a in matrix_2.flat:
#    print a

i = len(matrix_2.shape) - 1
print i
# for index, elem in enumerate(matrix_2.flat):
#     print index, elem

index_aux = []
for s in matrix_2.shape:
    index_aux.append(0)
print index_aux


a = [1,2]

for index, value in enumerate(a):
    print index, value

print "---"
for index, value in ndenumerate(matrix_2):
    print index, value