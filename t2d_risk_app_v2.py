
import streamlit as st
import pandas as pd
import io

# -----------------------------
# SNP Risk Data
# -----------------------------
snp_data = [
    {"rsid": "rs7903146", "gene": "TCF7L2", "risk_allele": "T", "beta": 0.31},
    {"rsid": "rs1801282", "gene": "PPARG", "risk_allele": "G", "beta": 0.22},
    {"rsid": "rs5219", "gene": "KCNJ11", "risk_allele": "A", "beta": 0.21},
    {"rsid": "rs13266634", "gene": "SLC30A8", "risk_allele": "C", "beta": 0.11},
    {"rsid": "rs10811661", "gene": "CDKN2A/B", "risk_allele": "T", "beta": 0.35},
    {"rsid": "rs4402960", "gene": "IGF2BP2", "risk_allele": "T", "beta": 0.18},
    {"rsid": "rs864745", "gene": "JAZF1", "risk_allele": "G", "beta": 0.14},
]

snp_df = pd.DataFrame(snp_data)

# -----------------------------
# Helper: Count risk alleles
# -----------------------------
def count_risk_alleles(genotype, risk_allele):
    return genotype.count(risk_allele)

# -----------------------------
# Title
# -----------------------------
st.title("T2D Polygenic Risk Predictor (v2)")
st.markdown("""Upload your genotype file or manually input your SNPs to calculate your Type 2 Diabetes polygenic risk score (PRS).""")

# -----------------------------
# Upload or Manual Input
# -----------------------------
input_mode = st.radio("Choose input method:", ["Upload Genotype File", "Manual Entry"])

user_genotypes = {}

if input_mode == "Upload Genotype File":
    uploaded_file = st.file_uploader("Upload .txt or 23andMe-style file", type=["txt", "csv"])
    if uploaded_file:
        content = uploaded_file.read().decode("utf-8")
        lines = content.strip().split("\n")
        for line in lines:
            if line.startswith("rsid") or line.startswith("#") or line == "":
                continue
            parts = line.strip().split()
            if len(parts) == 2:
                rsid, genotype = parts
            elif len(parts) >= 4:
                rsid, genotype = parts[0], parts[3]
            else:
                continue
            user_genotypes[rsid] = genotype.upper()

else:
    st.subheader("Manual Genotype Entry")
    for snp in snp_data:
        rsid = snp["rsid"]
        user_input = st.selectbox(
            f"{rsid} ({snp['gene']})", 
            ["", "AA", "AC", "AG", "AT", "CC", "CG", "CT", "GG", "GT", "TT"], 
            key=rsid
        )
        if user_input:
            user_genotypes[rsid] = user_input

# -----------------------------
# Calculate PRS
# -----------------------------
if st.button("Calculate Risk Score") and user_genotypes:
    total_prs = 0.0
    results = []

    for snp in snp_data:
        rsid = snp["rsid"]
        beta = snp["beta"]
        risk_allele = snp["risk_allele"]
        genotype = user_genotypes.get(rsid)

        if genotype:
            num_risk = count_risk_alleles(genotype, risk_allele)
            prs_contribution = beta * num_risk
            total_prs += prs_contribution
            results.append({
                "SNP": rsid,
                "Gene": snp["gene"],
                "Genotype": genotype,
                "Risk Allele": risk_allele,
                "Copies": num_risk,
                "Beta": beta,
                "PRS Contribution": round(prs_contribution, 3)
            })

    # -----------------------------
    # Output Results
    # -----------------------------
    st.subheader("Results Summary")
    st.write(f"**Total Polygenic Risk Score (PRS): {round(total_prs, 3)}**")

    if total_prs >= 1.5:
        level = "High Genetic Risk"
    elif total_prs >= 0.8:
        level = "Moderate Genetic Risk"
    else:
        level = "Low Genetic Risk"

    st.success(f"**Estimated Genetic Risk Level: {level}**")

    st.progress(min(total_prs / 2, 1.0))

    st.subheader("Detailed SNP Breakdown")
    st.dataframe(pd.DataFrame(results))

    st.caption("Note: This is an educational tool. Always consult a professional for clinical decisions.")
