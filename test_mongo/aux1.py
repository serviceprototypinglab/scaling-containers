matrix_1 = [
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
]


matrix_2 = []
for row in matrix_1:
    aux_array = []
    for element in row:
        aux_array.append(element/35.9154654562)
    matrix_2.append(aux_array)

print matrix_2