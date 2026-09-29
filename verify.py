"""verify.py — Quick smoke test for graph queries (no LLM/API key required)"""
from src.graph_builder import build_knowledge_graph
from src.query_engine import (
    get_products_by_brand_and_vendor,
    get_products_by_category,
    get_orders_by_customer,
    search_banana,
    get_products_under_price_in_category,
)

G = build_knowledge_graph()

print("=" * 60)
print("Q1: TechNova products supplied by FastShip Logistics")
print("=" * 60)
r1 = get_products_by_brand_and_vendor(G, "TechNova", "FastShip")
for p in r1:
    print(f"  - {p['name']} | Rs {p['price']} | Vendors: {p['vendors']}")

print()
print("=" * 60)
print("Q2: Electronics category products & vendors")
print("=" * 60)
r2 = get_products_by_category(G, "Electronics")
for p in r2:
    print(f"  - {p['name']} | Rs {p['price']} | Vendors: {p['vendors']}")

print()
print("=" * 60)
print("Q3: Orders placed by Alice")
print("=" * 60)
r3 = get_orders_by_customer(G, "Alice")
for o in r3:
    prod_names = [pr["name"] for pr in o["products"]]
    print(f"  - Order {o['id']} | {o['date']} | Rs {o['total']} | Status: {o['status']}")
    print(f"    Products: {prod_names}")

print()
print("=" * 60)
print("Q4: Search for 'banana' in the graph")
print("=" * 60)
r4 = search_banana(G)
print(f"  Total banana nodes: {r4['total_occurrences']}")
for node in r4["banana_nodes"]:
    print(f"  - [{node['node_type']}] {node['node_id']}: {node['matched_fields'][0]['value']}")

print()
print("=" * 60)
print("Q5: Fashion products under Rs 1500")
print("=" * 60)
r5 = get_products_under_price_in_category(G, 1500, "Fashion")
if r5:
    for p in r5:
        print(f"  - {p['name']} | Rs {p['price']} | Vendors: {p['vendors']}")
else:
    print("  No products found under Rs 1500 in Fashion category.")

print()
print("All graph queries completed successfully!")
