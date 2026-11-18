# Method notes

- **Weights:** W_i = mapped area of class i / total area.
- **Estimated area proportions:** p_ij = W_i · n_ij / n_i.
- **Overall accuracy:** Σ p_jj; V = Σ W_i² U_i(1−U_i)/(n_i−1).
- **User's accuracy:** U_i = n_ii / n_i; V = U_i(1−U_i)/(n_i−1).
- **Producer's accuracy:** P_j = p_jj / p_·j; variance per Olofsson et al. (2014) eq. 7.
- **Area:** Â_j = A · p_·j; SE(p_·j) = sqrt(Σ_i (W_i p_ij − p_ij²)/(n_i−1)).

**Sample size (rule of thumb, Olofsson 2014 §5.1.1):** n ≈ (Σ W_i S_i / S(Ô))², S_i = sqrt(U_i(1−U_i)), with a target SE of overall accuracy around 0.01; then allocate ≥ 50–100 samples to rare classes and the rest roughly proportionally.

**Non-stratified designs:** if samples were simple random, labelling each by its map class and using strata = map classes is still unbiased (post-stratification); state this in Limitations.
