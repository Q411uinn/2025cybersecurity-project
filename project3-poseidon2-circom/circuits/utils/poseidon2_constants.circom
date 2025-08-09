pragma circom 2.1.6;

template Poseidon2Constants(t, totalRounds) {
    signal output constants[totalRounds][t];
    for (var round = 0; round < totalRounds; round++) {
        for (var i = 0; i < t; i++) {
            constants[round][i] <== round + i + 1;
        }
    }
}
