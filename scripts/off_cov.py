import json,sys,time,urllib.request,urllib.parse
UA={"User-Agent":"HackathonCheck/0.1 (philip@pinnacleprompts.com)"}
F="code,product_name,brands,packaging_materials_tags,packaging_tags,packagings,origins_tags,manufacturing_places_tags,ingredients_tags,nova_group,categories_tags"
cats=sys.argv[1:]
for cat in cats:
    q=urllib.parse.urlencode({"countries_tags_en":"united-states","categories_tags_en":cat,"page_size":100,"fields":F,"sort_by":"unique_scans_n"})
    for attempt in range(3):
        try:
            r=json.load(urllib.request.urlopen(urllib.request.Request("https://world.openfoodfacts.org/api/v2/search?"+q,headers=UA),timeout=40));break
        except Exception as e:
            r=None; err=e; time.sleep(8)
    if not r: print(cat,"FAIL",err); continue
    ps=r["products"]; n=len(ps) or 1
    has=lambda k: sum(1 for p in ps if p.get(k))
    pk=sum(1 for p in ps if p.get("packaging_materials_tags") or p.get("packagings") or p.get("packaging_tags"))
    print(f"{cat}: total={r['count']} sample={len(ps)} packaging_any={pk/n:.0%} materials={has('packaging_materials_tags')/n:.0%} origins={has('origins_tags')/n:.0%} mfg_place={has('manufacturing_places_tags')/n:.0%} ingredients={has('ingredients_tags')/n:.0%} nova={has('nova_group')/n:.0%}")
    json.dump(ps,open(f"{cat}.json","w"))
    ex=[p for p in ps if p.get("packaging_materials_tags")][:3]
    for p in ex: print("   e.g.",p.get("code"),p.get("brands"),"|",p.get("product_name"),"|",p.get("packaging_materials_tags"))
    time.sleep(7)
