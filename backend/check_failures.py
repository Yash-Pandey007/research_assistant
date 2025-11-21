import json

with open('test_results_comprehensive.json') as f:
    data = json.load(f)

print("TEST RESULTS SUMMARY\n" + "="*80)
for i, r in enumerate(data, 1):
    status = "✅ PASS" if r["success"] else "❌ FAIL"
    print(f"{i:2}. {status} - [{r['category']:15}] {r['question']}")

print("\n" + "="*80)
failures = [r for r in data if not r["success"]]
print(f"\nTotal: {len(data)}, Passed: {len(data)-len(failures)}, Failed: {len(failures)}")

if failures:
    print("\nFAILED TESTS DETAILS:\n" + "-"*80)
    for r in failures:
        print(f"❌ [{r['category']}] {r['question']}")
        print(f"   answer_length: {r.get('answer_length', 0)}")
        print(f"   source_count: {r.get('source_count', 0)}")
        print(f"   elapsed: {r.get('elapsed_seconds', 0)}s")
        if 'error' in r:
            print(f"   ERROR: {r['error']}")
        print()
