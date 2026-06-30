#!/usr/bin/env python3
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

fp = os.path.join(os.path.dirname(__file__), 'fin_graph.json')
f = json.load(open(fp, 'r', encoding='utf-8'))
es = f.get('entities', [])

# 只看Bazaar相关
ba = [e for e in es if 'bazaar' in e.get('type','')]
print(f'Bazaar总实体: {len(ba)}')
print(f'有label的: {sum(1 for b in ba if b.get("label",""))}')
# 看几个样本
for t in ['bazaar_daily', 'bazaar_menu_item', 'bazaar_monthly']:
    items = [b for b in ba if b.get('type')==t]
    print(f'\n{t} x{len(items)}')
    # 样本
    for item in items[:3]:
        print(f'  id={item.get("id","")} label="{item.get("label","")}"')
        # 显示所有非empty字段
        for k,v in item.items():
            if k not in ('id','type','label') and v:
                if isinstance(v,(int,float)) and v > 0:
                    print(f'    {k}={v}')
                elif isinstance(v,str) and v.strip():
                    print(f'    {k}="{v[:30]}"')

# 补label需要的数据在哪？
print('\n=== 分析: 补Bazaar label的可行性 ===')
print('bazaar_menu_item: 170个，id包含中文品名')
print('  e.g. BAZAAR_ITEM_生椰拿铁吐司 → label="生椰拿铁吐司"')
print('  可以批量提取，2行代码搞定')
print('bazaar_daily: 183个，id是日期格式')
print('  e.g. BAZAAR_2021_08_10 → label="2021-08-10 美食市集"')
print('  也可以批量')
print('bazaar_monthly: 13个，id也是日期')
print('')
print('但问题: 这些数据没有收入/成本/利润等关键数值字段')
print('补label只解决"好看"问题，不解决"有用"问题')
print('实际价值: 低（除非后续要基于Bazaar做分析）')
