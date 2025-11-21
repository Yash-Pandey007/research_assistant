import json

with open('test_results_comprehensive.json') as f:
    data = json.load(f)

failures = [r for r in data if not r["success"]]

print(f"FOUND {len(failures)} FAILURES:\n")
print("="*80)

for i, r in enumerate(failures, 1):
    print(f"\n{i}. [{r['category'].upper()}] {r['question']}")
    print("-"*80)
    print(f"   Elapsed Time: {r.get('elapsed_seconds', 0)}s")
    print(f"   Source Count: {r.get('source_count', 0)}")
    print(f"   Answer Length: {r.get('answer_length', 0)} chars")
    
    if 'error' in r:
        print(f"   Error Message: {r['error']}")
    
    if r.get('source_count', 0) > 0:
        print(f"\n   ⚠️ Has sources but failed (likely synthesis issue)")
    else:
        print(f"\n   ⚠️ No sources found (search issue)")
    
    # Show sources if any
    if r.get('sources'):
        print(f"\n   Sources Found:")
        for j, src in enumerate(r['sources'][:3], 1):
            print(f"     {j}. {src['title'][:70]}...")
    
    print()
