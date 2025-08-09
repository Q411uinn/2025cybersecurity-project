pragma circom 2.1.6;

include "./utils/poseidon2_constants.circom";
include "./utils/poseidon2_round.circom";

template Poseidon2Permutation(t) {
    assert(t == 2 || t == 3);
    
    signal input state[t];
    signal output out[t];
    
    var RF = 8;
    var RP = t == 2 ? 56 : 57;
    var totalRounds = RF + RP;
    
    component rounds[totalRounds];
    component constants = Poseidon2Constants(t, totalRounds);
    
    signal stateRounds[totalRounds + 1][t];
    for (var i = 0; i < t; i++) {
        stateRounds[0][i] <== state[i];
    }
    
    for (var round = 0; round < totalRounds; round++) {
        var isFullRound = (round < RF/2) || (round >= RF/2 + RP);
        rounds[round] = Poseidon2Round(t, isFullRound);
        for (var i = 0; i < t; i++) {
            rounds[round].state[i] <== stateRounds[round][i];
            rounds[round].roundConstant[i] <== constants.constants[round][i];
        }
        for (var i = 0; i < t; i++) {
            stateRounds[round + 1][i] <== rounds[round].out[i];
        }
    }
    
    for (var i = 0; i < t; i++) {
        out[i] <== stateRounds[totalRounds][i];
    }
}

template Poseidon2Hash(t) {
    assert(t == 2 || t == 3);
    
    signal input inputs[t-1];
    signal output out;
    
    component permutation = Poseidon2Permutation(t);
    
    permutation.state[0] <== 0;
    for (var i = 0; i < t-1; i++) {
        permutation.state[i+1] <== inputs[i];
    }
    
    out <== permutation.out[1];
}

template Poseidon2ZK() {
    signal input preimage[2];
    signal output hashOut;

    component hasher = Poseidon2Hash(3);
    hasher.inputs[0] <== preimage[0];
    hasher.inputs[1] <== preimage[1];

    hashOut <== hasher.out;   
}
component main = Poseidon2ZK();
