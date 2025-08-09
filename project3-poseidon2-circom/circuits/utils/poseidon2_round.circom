pragma circom 2.1.6;

template Poseidon2Round(t, isFullRound) {
    signal input state[t];
    signal input roundConstant[t];
    signal output out[t];
    
    signal afterConstants[t];
    for (var i = 0; i < t; i++) {
        afterConstants[i] <== state[i] + roundConstant[i];
    }
    
    signal afterSbox[t];
    if (isFullRound) {
        for (var i = 0; i < t; i++) {
            afterSbox[i] <== PowerFive()(afterConstants[i]);
        }
    } else {
        afterSbox[0] <== PowerFive()(afterConstants[0]);
        for (var i = 1; i < t; i++) {
            afterSbox[i] <== afterConstants[i];
        }
    }
    
    if (t == 2) {
        out[0] <== 2 * afterSbox[0] + afterSbox[1];
        out[1] <== afterSbox[0] + 2 * afterSbox[1];
    } else if (t == 3) {
        out[0] <== 2 * afterSbox[0] + afterSbox[1] + afterSbox[2];
        out[1] <== afterSbox[0] + 2 * afterSbox[1] + afterSbox[2];
        out[2] <== afterSbox[0] + afterSbox[1] + 3 * afterSbox[2];
    }
}

template PowerFive() {
    signal input in;
    signal output out;
    
    signal x2 <== in * in;
    signal x4 <== x2 * x2;
    out <== x4 * in;
}
