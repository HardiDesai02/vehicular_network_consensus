import pandas as pd
import numpy as np
import os

# Load reputation data
reputation_df = pd.read_csv("../data/reputation_scores.csv")

# Ensure only one reputation row per Vehicle_ID (latest or highest)
reputation_df = reputation_df.sort_values("Reputation", ascending=False).drop_duplicates("Vehicle_ID")

# Select top 4 MCNs (3f+1 nodes for PBFT with f=1)
mcn_set = reputation_df.head(4).copy()
print("Selected MCNs for PBFT:", mcn_set["Vehicle_ID"].tolist())

# Simulate block proposal
proposer = mcn_set.iloc[0]
proposer_id = proposer["Vehicle_ID"]
print(f"\n🧾 Proposer: {proposer_id}")

# Remaining MCNs are validators
validators = mcn_set.iloc[1:]

def validate_block(row):
    # Each MCN votes 'approve' with probability = SoB (success rate)
    return np.random.rand() < row["SoB"]

# Simulate voting
votes = []
for _, node in validators.iterrows():
    vote = validate_block(node)
    votes.append((node["Vehicle_ID"], vote))

# Count approvals
approvals = sum(1 for _, v in votes if v)

# PBFT threshold for 3f+1 nodes with f=1 is at least 3 approvals
approved = approvals >= 2

# Save results
os.makedirs("../results", exist_ok=True)
with open("../results/pbft_log.txt", "w") as f:
    f.write(f"Proposer: {proposer_id}\n")
    f.write("Votes:\n")
    for node_id, v in votes:
        f.write(f"{node_id} -> {'✔️ Approve' if v else '❌ Reject'}\n")
    f.write(f"\n✅ Consensus Reached: {approved}\n" if approved else "\n❌ Consensus Failed\n")

# Output summary
print("\nVotes:")
for vid, vote in votes:
    print(f"{vid} -> {'✔️ Approve' if vote else '❌ Reject'}")

print("\n✅ Consensus Reached!" if approved else "\n❌ Consensus Failed")
