#!/usr/bin/env python3
from __future__ import annotations
import math
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
VALIDATION = ROOT / "validation"

def close(a,b,t=0.02):
    return math.isclose(float(a),float(b),abs_tol=t,rel_tol=0.0)

def add(results, condition, message):
    results.append((bool(condition), message))

def main():
    r=[]
    b=pd.read_csv(DATA/"bootstrap_containment_summary.csv").iloc[0]
    n=pd.read_csv(DATA/"null_test_summary.csv")
    c=pd.read_csv(DATA/"candidate_comparison.csv")
    g=pd.read_csv(DATA/"grace_mission_geometry_summary.csv")
    v=pd.read_csv(VALIDATION/"validation_summary.csv")

    add(r, close(b["candidate_distance_deg"],18.81), "Candidate-to-center distance is 18.81 degrees.")
    add(r, close(b["radius_99_deg"],3.04), "Empirical 99% radius is 3.04 degrees.")
    add(r, str(b["classification"]).lower()=="unsupported", "Containment classification is unsupported.")
    add(r, int(b["bootstrap_realizations"])==2000, "Family bootstrap used 2,000 realizations.")
    add(r, int(b["unique_centers"])==8, "Family bootstrap contains eight unique centers.")

    expected_p={
      ("depth_permutation","axial_concentration"):0.01060,
      ("depth_permutation","maximum_pairwise_selected_axis_separation_deg"):0.00640,
      ("depth_permutation","mean_pairwise_projector_distance"):0.00100,
      ("independent_model_rotation","axial_concentration"):0.000200,
      ("independent_model_rotation","maximum_pairwise_selected_axis_separation_deg"):0.000100,
      ("independent_model_rotation","mean_pairwise_projector_distance"):0.000100,
      ("shallower_interval_substitution","axial_concentration"):0.000300,
      ("shallower_interval_substitution","maximum_pairwise_selected_axis_separation_deg"):0.00280,
      ("shallower_interval_substitution","mean_pairwise_projector_distance"):0.000100}
    for (nm,st),exp in expected_p.items():
        rows=n[(n.null_model==nm)&(n.statistic==st)]
        add(r,len(rows)==1,f"One result exists for {nm} / {st}.")
        if len(rows)==1:
            row=rows.iloc[0]
            add(r,int(row.realizations)==10000,f"{nm} / {st} used 10,000 realizations.")
            add(r,close(row.empirical_p,exp,0.000002),f"{nm} / {st} p-value matches the paper.")

    expected_d={
      "family_balanced_lowermost_center":18.81,
      "primary_static_gravity_residual":9.45,
      "unica25_absolute_vp_2500_2891_km":2.16,
      "closest_pooled_depth_interval_center":14.85,
      "closest_model_family_center":15.82,
      "solid_lithosphere_maximum_axis":39.09}
    for name,exp in expected_d.items():
        rows=c[c.comparison==name]
        add(r,len(rows)==1,f"One comparison row exists for {name}.")
        if len(rows)==1:
            add(r,close(rows.iloc[0].axial_distance_to_candidate_deg,exp),f"{name} distance matches the paper.")

    expected_g={"named_minimum_role":88.83,"named_intermediate_role":4.59,
                "named_maximum_role":88.78,"optimally_permuted_unordered_frame":4.78}
    for name,exp in expected_g.items():
        rows=g[g.representation==name]
        add(r,len(rows)==1,f"One GRACE summary row exists for {name}.")
        if len(rows)==1:
            add(r,close(rows.iloc[0].median_difference_deg,exp),f"{name} median matches the paper.")
            add(r,int(rows.iloc[0].bootstrap_realizations)==1000,f"{name} uses 1,000 bootstrap realizations.")

    add(r,v.passed.astype(str).str.lower().isin(["true","1"]).all(),"All published validation summaries pass.")
    fails=sum(not ok for ok,_ in r)
    print("Publication verification\n========================")
    for ok,msg in r:
        print(("[PASS] " if ok else "[FAIL] ")+msg)
    print(f"\n{len(r)-fails} passed; {fails} failed.")
    return 1 if fails else 0

if __name__=="__main__":
    raise SystemExit(main())
