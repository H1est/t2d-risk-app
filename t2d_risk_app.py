
import streamlit as st

# Title
st.title("Type 2 Diabetes Risk Predictor")
st.write("Select your genotype for each SNP below. Your estimated genetic risk will be calculated based on known associations with T2D.")

# SNP data
snps = [
    {"id": "rs7903146", "gene": "TCF7L2", "risk_allele": "T", "risk_genotypes": ["TT", "CT"], "odds_ratio": 1.37},
    {"id": "rs1801282", "gene": "PPARG", "risk_allele": "G", "risk_genotypes": ["GG", "CG"], "odds_ratio": 1.25},
    {"id": "rs5219", "gene": "KCNJ11", "risk_allele": "A", "risk_genotypes": ["AA", "GA"], "odds_ratio": 1.23},
    {"id": "rs13266634", "gene": "SLC30A8", "risk_allele": "C", "risk_genotypes": ["CC", "TC"], "odds_ratio": 1.12},
    {"id": "rs10811661", "gene": "CDKN2A/B", "risk_allele": "T", "risk_genotypes": ["TT", "CT"], "odds_ratio": 1.40},
    {"id": "rs4402960", "gene": "IGF2BP2", "risk_allele": "T", "risk_genotypes": ["TT", "GT"], "odds_ratio": 1.20},
    {"id": "rs864745", "gene": "JAZF1", "risk_allele": "G", "risk_genotypes": ["GG", "AG"], "odds_ratio": 1.15},
]

# User genotype input
total_risk_score = 0.0
risk_factors = []
st.subheader("Your Genotypes")
for snp in snps:
    genotype = st.selectbox(
        f"{snp['id']} ({snp['gene']})",
        ["", "AA", "AC", "AG", "AT", "CC", "CG", "CT", "GG", "GT", "TT"],
        key=snp['id']
    )
    if genotype in snp['risk_genotypes']:
        total_risk_score += snp['odds_ratio']
        risk_factors.append((snp['id'], snp['gene'], genotype, snp['odds_ratio']))

# Display result
if st.button("Calculate Risk"):
    st.subheader("Results")
    if risk_factors:
        st.write("You have risk genotypes for the following SNPs:")
        for snp_id, gene, geno, oratio in risk_factors:
            st.markdown(f"- **{snp_id}** ({gene}): {geno} (Odds Ratio: {oratio})")

        # Interpret score
        if total_risk_score > 8:
            risk_level = "High Risk"
        elif total_risk_score > 4:
            risk_level = "Moderate Risk"
        else:
            risk_level = "Low Risk"

        st.success(f"Estimated Genetic Risk Level: **{risk_level}**")
        st.caption("Note: This is a simplified interpretation. Consult a healthcare provider for clinical insights.")
    else:
        st.info("You did not select any known risk genotypes. Estimated risk level is Low.")
